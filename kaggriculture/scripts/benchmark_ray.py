"""Compare a private Ray cluster with the fastest per-node forkserver baseline."""
import argparse
import atexit
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from arena.batch import batched_runner, make_batch, percentile  # noqa: E402
from arena.jobs import plan  # noqa: E402
from arena.ray_transport import connect  # noqa: E402


def metrics(rows, seconds, batches=(), *, cpu_utilization=None):
    match_seconds = [row['wall_seconds'] for row in rows]
    batches = list(batches)
    if batches:
        weighted = [(batch.get('cpu_utilization'), batch['wall_seconds']) for batch in batches
                    if batch.get('cpu_utilization') is not None]
        cpu_utilization = (None if not weighted else
                           sum(value * weight for value, weight in weighted) /
                           sum(weight for _, weight in weighted))
    return {'seconds': seconds, 'jobs_per_second': len(rows) / seconds,
            'p50_match_seconds': percentile(match_seconds, .5),
            'p95_match_seconds': percentile(match_seconds, .95),
            'batch_tail_seconds': max((batch['wall_seconds'] for batch in batches), default=None),
            'cpu_utilization': cpu_utilization}


def game_result(row):
    return json.dumps({key: value for key, value in row.items()
                       if key not in {'runtime_ms', 'wall_seconds', 'hostname', 'git_commit',
                                      'git_dirty', 'job_id', 'batch_id'}},
                      sort_keys=True, separators=(',', ':'), allow_nan=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--address', default='auto')
    parser.add_argument('--jobs', default='32,256,1024,8000')
    parser.add_argument('--candidate', default='versions/v004/main.py')
    parser.add_argument('--opponent', default='opponents/public/thomas_t95/main.py')
    parser.add_argument('--seed', type=int, default=1700)
    parser.add_argument('--local-workers', type=int,
                        help='optional per-node cap; default uses every CPU each node advertises')
    parser.add_argument('--cpus-per-worker', type=int, default=1)
    parser.add_argument('--batch-size', type=int,
                        help='omit to keep at least eight waves queued per cluster slot')
    parser.add_argument('--minimum-representative-speedup', type=float, default=1.10,
                        help='required speedup for the 8000-job workload (default: 1.10)')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    if args.minimum_representative_speedup <= 1:
        parser.error('--minimum-representative-speedup must be greater than 1')
    try:
        counts = [int(value) for value in args.jobs.split(',')]
    except ValueError:
        parser.error('--jobs must be a comma-separated list of integers')
    if not counts or any(count < 1 for count in counts):
        parser.error('--jobs values must be positive')

    mapper = connect(args.address, cpus_per_worker=args.cpus_per_worker)
    atexit.register(mapper.ray.shutdown)
    report = {'schema_version': 2, 'local_workers_cap': args.local_workers,
              'cluster_slots': mapper.available_slots,
              'cpus_per_worker': args.cpus_per_worker,
              'cluster_hostnames': None, 'workloads': []}
    for count in counts:
        seeds = range(args.seed, args.seed + (count + 1) // 2)
        jobs = plan(args.candidate, [args.opponent], seeds, split='diagnostic')[:count]
        for job in jobs:
            job['telemetry_enabled'] = False

        whole = make_batch(jobs)
        environments = mapper.verify_cluster([whole])
        hostnames = sorted({item['hostname'] for item in environments})
        if report['cluster_hostnames'] is None:
            report['cluster_hostnames'] = hostnames
            if 8000 in counts and len(hostnames) < 2:
                raise SystemExit('The representative benchmark requires two distinct hostnames')
        elif hostnames != report['cluster_hostnames']:
            raise SystemExit('Ray cluster membership changed during the benchmark')
        local_runs = mapper.local_baseline_on_every_node(
            whole, maximum_workers=args.local_workers)
        local_nodes = []
        for node, envelope, workers in local_runs:
            local_nodes.append({'node_id': node['NodeID'],
                                'hostname': envelope['hostname'], 'workers': workers,
                                **metrics(envelope['rows'], envelope['wall_seconds'], [envelope])})
        fastest = min(local_nodes, key=lambda item: item['seconds'])

        envelopes = []
        runner = batched_runner(size=args.batch_size, map_batches=mapper,
                                on_batch=envelopes.append,
                                available_slots=mapper.available_slots)
        started = time.monotonic()
        distributed = list(runner(jobs, args.cpus_per_worker))
        distributed_seconds = time.monotonic() - started
        fastest_rows = min(local_runs, key=lambda item: item[1]['wall_seconds'])[1]['rows']
        if [game_result(row) for row in fastest_rows] != [game_result(row) for row in distributed]:
            raise SystemExit(f'Distributed results differ for the {count}-job workload')

        ray_metrics = metrics(distributed, distributed_seconds, envelopes)
        speedup = fastest['seconds'] / distributed_seconds
        capacity_ratio = ((mapper.available_slots * args.cpus_per_worker) /
                          fastest['workers'])
        report['workloads'].append({'jobs': count, 'local_nodes': local_nodes,
            'fastest_local_hostname': fastest['hostname'],
            'fastest_local_workers': fastest['workers'], 'direct': {
                key: value for key, value in fastest.items()
                if key not in {'node_id', 'hostname', 'workers'}},
            'ray': ray_metrics, 'speedup': speedup,
            'parallel_efficiency': speedup / capacity_ratio,
            'batch_size': len(envelopes[0]['rows']) if envelopes else None,
            'batches': len(envelopes)})
        print(json.dumps(report['workloads'][-1], indent=2), flush=True)
    representative = next((row for row in report['workloads'] if row['jobs'] == 8000), None)
    report['throughput_gate'] = {
        'representative_jobs': 8000,
        'minimum_speedup': args.minimum_representative_speedup,
        'observed_speedup': None if representative is None else representative['speedup'],
        'passed': (None if representative is None else
                   representative['speedup'] >= args.minimum_representative_speedup),
    }
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    if representative is not None and not report['throughput_gate']['passed']:
        raise SystemExit('Distributed 8000-job throughput did not beat the fastest local '
                         f'node by {args.minimum_representative_speedup:.2f}x')
    mapper.ray.shutdown()


if __name__ == '__main__':
    main()
