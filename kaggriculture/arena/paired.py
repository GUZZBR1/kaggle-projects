"""Run both declared comparison legs and emit frozen wins-only evidence in one command."""
import argparse
import ast
from datetime import date
import json
from pathlib import Path
import time

from .agents import VARIANTS, agent_hash
from .engine import fingerprint
from .league import run_league
from .seeds import REGISTRY, SPLITS, parse_seeds, validate_seeds
from eval.comparison import build_comparison, digest, load_families
from eval.ladder import cohort, load_ratings, opponent_id, STRONG_CUT, MAX_RATING_AGE_DAYS
from eval.submit_gate import decide
from eval.pairing import paired_rows


def check_spec(spec):
    base = spec
    while '::' in base:
        wrapper, base = base.split('::', 1)
        if wrapper not in ('clock', 'xliq'):
            raise ValueError(f'Unknown adapter: {wrapper}')
    if base not in (*VARIANTS, 'champion', 'challenger', 'starter', 'pass', 'random'):
        path = Path(base)
        if not path.is_file():
            raise ValueError(f'Unknown agent: {spec}')
        ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    return agent_hash(spec)


def run_pair(baseline, candidate, opponents, seeds, output, *, workers=4, backend='fast',
             split='dev', min_blocks=100, strong_only=False, ratings=None, families=None,
             mirrors=(), cut=STRONG_CUT, max_age_days=MAX_RATING_AGE_DAYS,
             registry_path=REGISTRY):
    started = time.perf_counter()
    seeds, opponents = list(seeds), list(opponents)
    if (workers < 1 or backend not in ('fast', 'official') or min_blocks < 2
            or len(seeds) < min_blocks or not opponents or len(opponents) != len(set(opponents))):
        raise ValueError('Require positive workers, valid backend, unique opponents and enough seed blocks')
    if len({opponent_id(name) for name in opponents}) != len(opponents):
        raise ValueError('Ambiguous opponent IDs')
    today = date.today()
    ratings = json.loads(json.dumps(load_ratings() if ratings is None else ratings))
    families = dict(load_families() if families is None else families)
    if strong_only:
        opponents = [name for name in opponents if cohort(name, ratings, cut=cut,
                     max_age_days=max_age_days, today=today) == 'strong']
        if not opponents:
            raise ValueError('No current strong opponents in the requested panel')
    if not set(mirrors) <= {opponent_id(name) for name in opponents}:
        raise ValueError('Declared mirror must belong to the selected panel')
    hashes = {name: check_spec(name) for name in (baseline, candidate, *opponents)}
    environment = fingerprint()
    # Read-only prechecks precede any consumption. The league admits both hashes
    # atomically before its first callback and readmits the second leg.
    registry_before = validate_seeds(seeds, split, path=registry_path)
    target = Path(output)
    target.mkdir(parents=True, exist_ok=False)
    plan = dict(baseline=baseline, candidate=candidate, opponents=opponents, seeds=seeds,
                hashes=hashes, backend=backend, environment=environment, split=split,
                ratings=ratings, ratings_sha256=digest(ratings), families=families,
                as_of=today.isoformat(), cut=cut, max_rating_age_days=max_age_days,
                registry_before=registry_before, strong_only=strong_only)
    (target / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    results, timings = [], {}
    try:
        for label, agent, other in [('baseline', baseline, candidate), ('candidate', candidate, baseline)]:
            if {name: check_spec(name) for name in hashes} != hashes or fingerprint() != environment:
                raise ValueError('Agent or environment changed after the paired batch was declared')
            leg_started = time.perf_counter()
            rows, _, _ = run_league(agent, opponents, seeds, workers=workers, backend=backend,
                                   output=target / label, split=split, paired_with=(other,),
                                   registry_path=registry_path)
            timings[label] = time.perf_counter() - leg_started
            if len(rows) != len(seeds) * len(opponents) * 2:
                raise ValueError('Incomplete comparison leg')
            for row in rows:
                if (row['candidate_hash'] != hashes[agent]
                        or row['opponent_hash'] != hashes.get(row['opponent'])
                        or row['environment'] != environment or row['backend'] != backend
                        or row['seed'] not in seeds or row['seat'] not in (0, 1)):
                    raise ValueError('Match evidence differs from the declared batch')
            paired_rows(rows, rows)
            results.append(rows)
        comparison = build_comparison(*results, ratings=ratings, families=families, mirrors=mirrors,
                                      today=today, cut=cut, max_age_days=max_age_days, split=split)
        comparison['execution'] = dict(wall_seconds=time.perf_counter() - started,
                                       leg_wall_seconds=timings, split=split,
                                       strong_only=strong_only, plan_sha256=digest(plan))
        gate = decide(comparison)
        (target / 'comparison.json').write_text(json.dumps(comparison, indent=2) + '\n')
        (target / 'gate.json').write_text(json.dumps(gate, indent=2) + '\n')
        (target / 'report.md').write_text(gate['verdict'] + '\n\n' +
            '\n'.join('- ' + reason for reason in gate['reasons']) + '\n\n' +
            f"Wall time: {comparison['execution']['wall_seconds']:.2f}s.\n")
        return comparison, gate
    except Exception as exc:
        (target / 'failure.json').write_text(json.dumps(dict(error=str(exc),
            completed_legs=len(results), wall_seconds=time.perf_counter() - started), indent=2) + '\n')
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', required=True)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--opponents', required=True)
    parser.add_argument('--seeds', default='1000:1100')
    parser.add_argument('--split', choices=SPLITS, default='dev')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--backend', choices=('fast', 'official'), default='fast')
    parser.add_argument('--min-blocks', type=int, default=100, help='lower only for development or smoke runs')
    parser.add_argument('--strong-only', action='store_true')
    parser.add_argument('--cut', type=float, default=STRONG_CUT)
    parser.add_argument('--max-rating-age-days', dest='max_age_days', type=int, default=MAX_RATING_AGE_DAYS)
    parser.add_argument('--mirrors', default='')
    parser.add_argument('--output', required=True)
    args = vars(parser.parse_args())
    args['seeds'] = parse_seeds(args['seeds'])
    args['opponents'] = args['opponents'].split(',')
    args['mirrors'] = [name for name in args['mirrors'].split(',') if name]
    comparison, gate = run_pair(**args)
    print(json.dumps(dict(**gate, wall_seconds=comparison['execution']['wall_seconds']), indent=2))


if __name__ == '__main__':
    main()
