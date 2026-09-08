"""Conservative local submission recommendation; never sends an artifact.

The gate answers one question: is the candidate better than **the agent currently
occupying our active submission slot**? That agent is the incumbent, and it must be
declared, because the baseline leg of a paired comparison is frequently *not* it. A
comparison against the strongest artifact in the panel measures how far we are from
the public ceiling, which is informative and is reported, but it cannot authorize a
release: the panel is built from the public top precisely because it is stronger than
us, so treating it as the incumbent blocks every genuinely score-raising submission.
See docs/INCUMBENT_GATE.md for the measurement that forced this distinction.
"""
import math

# Declaring the incumbent is also the moment the operator states which active
# submission the release destroys, which docs/FINAL_SUBMISSION_POLICY.md requires
# before any send and which no downstream step can reconstruct.
INCUMBENT_FIELDS = ('id', 'hash', 'displaces')


def positive_interval(row):
    if not isinstance(row, dict):
        return False
    delta, ci = row.get('delta_win'), row.get('ci95')
    return (isinstance(delta, (int, float)) and math.isfinite(delta) and delta > 0
            and isinstance(ci, list) and len(ci) == 2
            and all(isinstance(v, (int, float)) and math.isfinite(v) for v in ci)
            and 0 < ci[0] <= ci[1] <= 1)


def _summary(comparison):
    """The two deltas, named by what each one is evidence of."""
    out = {}
    for key in ('strong', 'all'):
        row = comparison.get(key)
        if isinstance(row, dict):
            out[key] = {'delta_win': row.get('delta_win'), 'ci95': row.get('ci95')}
    return out


def refusals(comparison, incumbent):
    """Why this comparison cannot be read as a release decision, if it cannot.

    Kept separate from the criteria: a refusal says the wrong question was asked,
    while a criteria failure says the answer to the right question was no.
    """
    baseline = comparison.get('snapshot', {}).get('baseline_hash')
    if incumbent is None:
        return ['No incumbent declared. A paired comparison is a measurement; only a '
                'comparison whose baseline leg is the agent holding our active slot can '
                'authorize a release.']
    if not isinstance(incumbent, dict) or any(
            not isinstance(incumbent.get(field), str) or not incumbent.get(field)
            for field in INCUMBENT_FIELDS):
        return ['The incumbent declaration must name ' + ', '.join(INCUMBENT_FIELDS)
                + ' as non-empty strings; `displaces` records which active submission '
                  'the release destroys.']
    if not isinstance(baseline, str) or not baseline:
        return ['The comparison carries no baseline hash, so the declared incumbent '
                'cannot be checked against the leg that was actually run.']
    if baseline != incumbent['hash']:
        return [f"The baseline leg is {baseline}, not the declared incumbent "
                f"{incumbent['id']} ({incumbent['hash']}). This comparison measures "
                f"distance to a panel artifact, not a release decision."]
    return []


def criteria(comparison):
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
    return reasons


def decide(comparison, incumbent=None, ceiling=None):
    """Verdict over `comparison`, whose baseline leg must be the declared incumbent.

    `ceiling` is an optional second comparison against the strongest panel artifact.
    It is reported beside the decision and never changes it: it says how far we still
    are from the public top, which is a different question from whether to submit.
    """
    refused = refusals(comparison, incumbent)
    failures = criteria(comparison)
    # A failing measurement stays NO SUBMIT whoever the baseline was: nothing is
    # authorized either way, and softening it to NO DECISION would lose the finding.
    # A *passing* measurement against a non-incumbent is the case the gate must refuse.
    if refused and not failures:
        verdict, reasons = 'NO DECISION', refused
    elif refused:
        verdict, reasons = 'NO SUBMIT', failures + refused
    else:
        verdict = 'NO SUBMIT' if failures else 'SUBMIT'
        reasons = failures or [
            'Positive strong-cohort CI95 over at least 100 paired blocks against the '
            f"declared incumbent {incumbent['id']}, no strong-opponent regression, and "
            'improvement survives each strong opponent and family removal. Sending it '
            f"destroys the accumulated episodes of {incumbent['displaces']}."]
    result = {'verdict': verdict, 'policy_version': 2, 'reasons': reasons,
              'candidate_hash': comparison.get('snapshot', {}).get('candidate_hash'),
              'baseline_hash': comparison.get('snapshot', {}).get('baseline_hash'),
              'incumbent': incumbent,
              'comparison_role': 'incumbent' if not refused else 'measurement',
              'delta_over_baseline': _summary(comparison),
              'note': 'Local competitive gate only. Artifact preflight and '
                      'docs/FINAL_SUBMISSION_POLICY.md must also be satisfied.'}
    if ceiling is not None:
        result['delta_over_panel_ceiling'] = {
            'baseline_hash': ceiling.get('snapshot', {}).get('baseline_hash'),
            'diagnostic_only': True, **_summary(ceiling)}
    return result


def main():
    import argparse
    import json
    from pathlib import Path
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comparison', help='comparison JSON emitted by eval.ladder or arena.paired')
    parser.add_argument('--incumbent-id', help='id of the agent holding our active submission slot')
    parser.add_argument('--incumbent-hash', help='its agent hash; must equal the comparison baseline')
    parser.add_argument('--displaces', help='which active submission this release destroys')
    parser.add_argument('--ceiling', help='optional comparison against the strongest panel artifact')
    parser.add_argument('--output')
    args = parser.parse_args()
    declared = {'id': args.incumbent_id, 'hash': args.incumbent_hash, 'displaces': args.displaces}
    incumbent = declared if any(declared.values()) else None
    ceiling = json.loads(Path(args.ceiling).read_text()) if args.ceiling else None
    result = decide(json.loads(Path(args.comparison).read_text()), incumbent, ceiling)
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        Path(args.output).write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
