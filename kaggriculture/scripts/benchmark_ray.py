"""Compare a private Ray cluster with the current head-node forkserver baseline."""
import argparse
import atexit
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from arena.batch import (batched_runner, host_cpu_times, host_cpu_utilization,
                         percentile, worker_budget)  # noqa: E402
from arena.jobs import plan  # noqa: E402
from arena.parallel import matches  # noqa: E402
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
    parser.add_argument('--local-workers', type=int, default=worker_budget())
    parser.add_argument('--cpus-per-worker', type=int, default=1)
    parser.add_argument('--batch-size', type=int,
                        help='omit to keep at least eight waves queued per cluster slot')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    mapper = connect(args.address, cpus_per_worker=args.cpus_per_worker)
    atexit.register(mapper.ray.shutdown)
    report = {'schema_version': 1, 'head_local_workers': args.local_workers,
              'cluster_slots': mapper.available_slots,
              'cpus_per_worker': args.cpus_per_worker, 'workloads': []}
    for count in [int(value) for value in args.jobs.split(',')]:
        seeds = range(args.seed, args.seed + (count + 1) // 2)
        jobs = plan(args.candidate, [args.opponent], seeds, split='diagnostic')[:count]
        for job in jobs:
            job['telemetry_enabled'] = False

        started, cpu_started = time.monotonic(), host_cpu_times()
        direct = list(matches(jobs, workers=args.local_workers))
        direct_seconds = time.monotonic() - started
        direct_cpu = host_cpu_utilization(cpu_started, host_cpu_times())

        envelopes = []
        runner = batched_runner(size=args.batch_size, map_batches=mapper,
                                on_batch=envelopes.append,
                                available_slots=mapper.available_slots)
        started = time.monotonic()
        distributed = list(runner(jobs, args.cpus_per_worker))
        distributed_seconds = time.monotonic() - started
        if [game_result(row) for row in direct] != [game_result(row) for row in distributed]:
            raise SystemExit(f'Distributed results differ for the {count}-job workload')

        direct_metrics = metrics(direct, direct_seconds, cpu_utilization=direct_cpu)
        ray_metrics = metrics(distributed, distributed_seconds, envelopes)
        speedup = direct_seconds / distributed_seconds
        capacity_ratio = ((mapper.available_slots * args.cpus_per_worker) /
                          args.local_workers)
        report['workloads'].append({'jobs': count, 'direct': direct_metrics,
            'ray': ray_metrics, 'speedup': speedup,
            'parallel_efficiency': speedup / capacity_ratio,
            'batch_size': len(envelopes[0]['rows']) if envelopes else None,
            'batches': len(envelopes)})
        print(json.dumps(report['workloads'][-1], indent=2), flush=True)
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    mapper.ray.shutdown()


if __name__ == '__main__':
    main()
