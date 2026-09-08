"""Prove exact cross-node determinism and the remote deadline barrier.

This deliberately refuses a one-node cluster.  A local Ray smoke test is useful for the
transport implementation, but it is not evidence for issue #43's release gates.
"""
import argparse
import atexit
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from arena.batch import make_batch  # noqa: E402
from arena.jobs import plan  # noqa: E402
from arena.ray_transport import connect  # noqa: E402

NONDETERMINISTIC = {'runtime_ms', 'wall_seconds', 'hostname', 'git_commit', 'git_dirty'}


def exact_result(row):
    relevant = {key: value for key, value in row.items() if key not in NONDETERMINISTIC}
    return json.dumps(relevant, sort_keys=True, separators=(',', ':'), allow_nan=False)


def assert_identical(results):
    baseline_node, baseline = results[0]
    baseline_rows = [exact_result(row) for row in baseline['rows']]
    for node, result in results[1:]:
        rows = [exact_result(row) for row in result['rows']]
        if len(rows) != len(baseline_rows):
            raise SystemExit(f'Node {node["NodeID"]} returned a different row count')
        for index, (expected, actual) in enumerate(zip(baseline_rows, rows)):
            if actual != expected:
                job_id = baseline['rows'][index]['job_id']
                raise SystemExit(f'Bit-exact result mismatch at job {job_id}: '
                                 f'{baseline_node["NodeID"]} != {node["NodeID"]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--address', default='auto')
    parser.add_argument('--candidate', default='versions/v004/main.py')
    parser.add_argument('--opponent', default='opponents/public/thomas_t95/main.py')
    parser.add_argument('--seed', type=int, default=200)
    parser.add_argument('--pairs', type=int, default=200,
                        help='seed pairs; each produces one match in each seat on every node')
    parser.add_argument('--cpus-per-worker', type=int, default=1)
    parser.add_argument('--deadline', type=float, default=4.)
    parser.add_argument('--deadline-overhead', type=float, default=15.)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    mapper = connect(args.address, cpus_per_worker=args.cpus_per_worker,
                     attempts=3, timeout=-1)
    atexit.register(mapper.ray.shutdown)
    work = plan(args.candidate, [args.opponent],
                range(args.seed, args.seed + args.pairs), split='diagnostic')
    for job in work:
        job['telemetry_enabled'] = False
    batch = make_batch(work)
    environments = mapper.verify_cluster([batch])
    hostnames = {node['hostname'] for node in environments}
    if len(hostnames) < 2:
        raise SystemExit('Cross-node proof requires at least two distinct hostnames')
    results = mapper.run_on_every_node(batch)
    assert_identical(results)

    hang = plan('arena/probes/hang_agent.py', ['pass'], [args.seed - 1],
                split='diagnostic')[0]
    hang['telemetry_enabled'] = False
    hang_results = mapper.run_on_every_node(make_batch([hang]), timeout=args.deadline)
    deadline_limit = args.deadline + args.deadline_overhead
    for node, result in hang_results:
        row = result['rows'][0]
        if row.get('timed_out') is not True or result['wall_seconds'] > deadline_limit:
            raise SystemExit(f'Deadline barrier failed on node {node["NodeID"]}')

    report = {'schema_version': 1, 'nodes': environments, 'hostnames': sorted(hostnames),
              'jobs_per_node': len(work), 'candidate': args.candidate,
              'opponent': args.opponent, 'seed_start': args.seed,
              'seed_pairs': args.pairs, 'bit_exact': True,
              'deadline_seconds': args.deadline,
              'deadline_limit_seconds': deadline_limit,
              'deadline_passed_on_every_node': True}
    Path(args.output).write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    mapper.ray.shutdown()


if __name__ == '__main__':
    main()
