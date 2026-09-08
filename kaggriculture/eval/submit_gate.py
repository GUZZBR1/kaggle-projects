"""Conservative local submission recommendation; never sends an artifact."""
import math


def positive_interval(row):
    if not isinstance(row, dict):
        return False
    delta, ci = row.get('delta_win'), row.get('ci95')
    return (isinstance(delta, (int, float)) and math.isfinite(delta) and delta > 0
            and isinstance(ci, list) and len(ci) == 2
            and all(isinstance(v, (int, float)) and math.isfinite(v) for v in ci)
            and 0 < ci[0] <= ci[1] <= 1)


def decide(comparison):
    reasons = []
    if comparison.get('schema_version') != 1 or comparison.get('evidence_validated') is not True:
        reasons.append('Missing validated paired evidence; generate it with eval.ladder or arena.paired.')
    if comparison.get('evaluation_split') != 'validation':
        reasons.append('Independent validation provenance is missing; development/seen/diagnostic runs cannot authorize a release.')
    if comparison.get('seed_blocks', 0) < 100:
        reasons.append('Fewer than 100 paired seed blocks; insufficient release evidence.')
    if not positive_interval(comparison.get('strong')):
        reasons.append('The strong-cohort win delta lacks a strictly positive CI95; coin margin and weak-opponent gains do not qualify.')
    strong = {name for name, row in comparison.get('per_opponent', {}).items()
              if row.get('cohort') == 'strong'}
    families = comparison.get('families', {})
    if len({families.get(name, name) for name in strong}) < 2:
        reasons.append('Fewer than two strong families; breadth of improvement is unmeasured.')
    regressions = sorted(name for name in strong
                         if comparison['per_opponent'][name].get('delta_win', 0) < 0)
    if regressions:
        reasons.append('Regression against strong opponents: ' + ', '.join(regressions) + '.')
    secondary = comparison.get('all', {}).get('delta_win')
    if secondary is None or not math.isfinite(secondary) or secondary < 0:
        reasons.append('The full-panel win delta is missing or negative.')
    loo = comparison.get('leave_one_out', {})
    if set(loo) != strong:
        reasons.append('Incomplete leave-one-opponent-out evidence.')
    for name in sorted(strong):
        if not positive_interval(loo.get(name)):
            label = 'mirror / shared-tape opponent' if name in comparison.get('mirrors', []) else 'opponent'
            reasons.append(f'Without {label} {name}, a positive strong-cohort effect is not established.')
    family_loo = comparison.get('leave_family_out', {})
    if set(family_loo) != {families.get(name, name) for name in strong}:
        reasons.append('Incomplete leave-one-family-out evidence.')
    for family, row in sorted(family_loo.items()):
        if not positive_interval(row):
            reasons.append(f'Without family {family}, a positive strong-cohort effect is not established.')
    verdict = 'NO SUBMIT' if reasons else 'SUBMIT'
    if not reasons:
        reasons.append('Positive strong-cohort CI95 over at least 100 paired blocks, no strong-opponent regression, and improvement survives each strong opponent and family removal.')
    return {'verdict': verdict, 'policy_version': 1, 'reasons': reasons,
            'candidate_hash': comparison.get('snapshot', {}).get('candidate_hash'),
            'note': 'Local competitive gate only. Artifact preflight and docs/FINAL_SUBMISSION_POLICY.md must also be satisfied.'}


def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comparison', help='comparison JSON emitted by eval.ladder or arena.paired')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = decide(json.loads(Path(args.comparison).read_text()))
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        Path(args.output).write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
