import argparse
from datetime import datetime, timezone
import json
import time

from .agents import agent_hash
from .parallel import matches
from .seeds import parse_seeds
from eval.metrics import summarize
from eval.reports import write_report


def run_league(candidate, opponents, seeds, workers=4, backend='fast', output=None, split='dev'):
    if len(set(opponents)) != len(opponents) or not opponents or len(set(seeds)) != len(seeds) or not seeds:
        raise ValueError('Require unique, nonempty opponents and seeds')
    started = time.perf_counter()
    jobs = [dict(candidate=candidate, opponent=opponent, seed=seed, seat=seat, backend=backend)
            for seed in seeds for opponent in opponents for seat in (0, 1)]
    rows = []
    for row in matches(jobs, workers):
        rows.append(row)
        if len(rows) % 20 == 0:
            print(f'{len(rows)}/{len(jobs)} games; {time.perf_counter()-started:.1f}s', flush=True)
    summary = summarize(rows)
    metadata = {'candidate': candidate, 'candidate_hash': agent_hash(candidate), 'opponents': opponents,
                'opponent_hashes': {name: agent_hash(name) for name in opponents},
                'split': split, 'seeds': seeds, 'backend': backend,
                'created_at': datetime.now(timezone.utc).isoformat(),
                'wall_seconds': time.perf_counter() - started}
    if output:
        write_report(output, rows, summary, metadata)
    return rows, summary, metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', default='challenger')
    parser.add_argument('--opponents', default='starter,crop,animal,diversified')
    parser.add_argument('--seeds', default='1000:1010')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--backend', choices=['fast', 'official'], default='fast')
    parser.add_argument('--split', choices=['dev', 'validation'], default='dev')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    args.opponents = args.opponents.split(',')
    args.seeds = parse_seeds(args.seeds)
    _, summary, _ = run_league(**vars(args))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
