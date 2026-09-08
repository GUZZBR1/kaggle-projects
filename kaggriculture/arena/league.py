import argparse
from datetime import datetime, timezone
import json
import time

from .agents import agent_hash
from .parallel import matches
from .seeds import REGISTRY, SPLITS, admit_run, parse_seeds
from eval.metrics import summarize
from eval.reports import write_report


def run_league(candidate, opponents, seeds, workers=4, backend='fast', output=None, split='dev',
               paired_with=(), registry_path=REGISTRY):
    if len(set(opponents)) != len(opponents) or not opponents or len(set(seeds)) != len(seeds) or not seeds:
        raise ValueError('Require unique, nonempty opponents and seeds')
    started = time.perf_counter()
    # Declare the whole paired batch, then burn reserved validation seeds before
    # the first callback runs. An interrupted run must not free them again.
    hashes = {name: agent_hash(name) for name in opponents}
    # A paired comparison is two legs over the same seeds. Both legs must name
    # every candidate in the batch, so the batch identity is fixed before the
    # first game and the second leg is readmitted rather than refused.
    members = sorted({agent_hash(name) for name in (candidate, *paired_with)})
    provenance = {'candidate': candidate, 'candidate_hash': agent_hash(candidate),
                  'paired_with': list(paired_with), 'batch_members': members,
                  'opponents': opponents, 'opponent_hashes': hashes, 'backend': backend,
                  'seeds': list(seeds), 'seats': [0, 1],
                  'requested_at': datetime.now(timezone.utc).isoformat()}
    registry = admit_run(seeds, split, provenance, path=registry_path)
    jobs = [dict(candidate=candidate, opponent=opponent, seed=seed, seat=seat, backend=backend)
            for seed in seeds for opponent in opponents for seat in (0, 1)]
    rows = []
    for row in matches(jobs, workers):
        rows.append(row)
        if len(rows) % 20 == 0:
            print(f'{len(rows)}/{len(jobs)} games; {time.perf_counter()-started:.1f}s', flush=True)
    summary = summarize(rows)
    metadata = {'candidate': candidate, 'candidate_hash': provenance['candidate_hash'],
                'opponents': opponents, 'opponent_hashes': hashes,
                'split': split, 'seeds': seeds, 'backend': backend, 'registry': registry,
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
    parser.add_argument('--split', choices=list(SPLITS), default='dev')
    parser.add_argument('--paired-with', dest='paired_with', default='',
                        help='other candidates in the same declared validation batch')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    args.opponents = args.opponents.split(',')
    args.paired_with = [n for n in args.paired_with.split(',') if n]
    args.seeds = parse_seeds(args.seeds)
    _, summary, _ = run_league(**vars(args))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
