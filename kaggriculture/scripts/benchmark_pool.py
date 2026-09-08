"""Measure games per second on this host, so a distributed claim has a local baseline.

Issue #43 asks for the benchmark against the current `forkserver` pool rather than the
`spawn` one it replaced, and for the batch layer to be measured next to the direct pool:
batching is what a second machine would distribute, and if it costs throughput here it
would cost it there too.

    python scripts/benchmark_pool.py --games 32 --workers 1,2,4,8,14
"""
import argparse
import json
import os
from pathlib import Path
import statistics
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from arena.batch import batched_runner, worker_budget  # noqa: E402
from arena.parallel import matches, start_method  # noqa: E402


def run(jobs, workers, batch_size=None):
    started = time.monotonic()
    if batch_size is None:
        rows = list(matches(jobs, workers=workers))
    else:
        rows = list(batched_runner(size=batch_size)(jobs, workers))
    elapsed = time.monotonic() - started
    return rows, elapsed


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--games', type=int, default=32)
    parser.add_argument('--workers', default='1,2,4,8')
    parser.add_argument('--batch-size', type=int, default=8)
    parser.add_argument('--candidate', default='clock::versions/v004/main.py')
    parser.add_argument('--opponent', default='clock::opponents/public/thomas_t95/main.py')
    parser.add_argument('--seed', type=int, default=1700)
    parser.add_argument('--output')
    args = parser.parse_args()

    jobs = [dict(candidate=args.candidate, opponent=args.opponent, seed=args.seed + index,
                 seat=index % 2, backend='fast', telemetry_enabled=False)
            for index in range(args.games)]
    report = {'host': os.uname().nodename if hasattr(os, 'uname') else '',
              'cpus': os.cpu_count(), 'start_method': start_method(),
              'default_workers': worker_budget(), 'games': args.games,
              'batch_size': args.batch_size, 'rows': []}
    reference = None
    for workers in [int(value) for value in args.workers.split(',')]:
        for label, size in (('direct', None), ('batched', args.batch_size)):
            rows, elapsed = run(jobs, workers, size)
            signature = [(row['seed'], row['seat'], row['score'], row['money']) for row in rows]
            if reference is None:
                reference = signature
            elif signature != reference:
                raise SystemExit('Throughput measured on results that disagree; refusing')
            entry = {'workers': workers, 'mode': label, 'seconds': elapsed,
                     'seconds_per_game': elapsed / len(rows), 'games_per_second': len(rows) / elapsed}
            report['rows'].append(entry)
            print(f"{label:8s} workers={workers:3d}  {entry['seconds_per_game']:.3f} s/game  "
                  f"{entry['games_per_second']:.2f} games/s", flush=True)
    base = min(row['seconds'] for row in report['rows'] if row['workers'] == 1)
    for row in report['rows']:
        row['speedup_vs_one_worker'] = base / row['seconds']
    report['result_signature_stable'] = True
    report['median_games_per_second'] = statistics.median(r['games_per_second'] for r in report['rows'])
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'default_workers': report['default_workers'],
                      'best': max(report['rows'], key=lambda r: r['games_per_second'])}, indent=2))


if __name__ == '__main__':
    main()
