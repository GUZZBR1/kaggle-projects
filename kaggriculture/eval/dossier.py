"""One verdict over one release decision, from evidence that has to agree with itself.

Every piece already exists, and each answers a different question. `arena.paired` and
`eval.submit_gate` say whether the candidate beats the agent holding our slot.
`eval.standing` says whether it is strong in absolute terms against the meta panel.
`submission.preflight` says the exact file we would upload plays a whole season.
`docs/FINAL_SUBMISSION_POLICY.md` says what a send costs, because the two active slots
work by recency and an upload destroys the accumulated episodes of whatever it displaces.

A candidate can pass one of those and fail another, and that is not where the risk is.
The risk is the hand-carry between them: a comparison about one artifact quoted beside a
standing about another, or beside a preflight of a file that was never the thing that was
evaluated. Reading three correct reports as one decision is the one step no report checks.

So the dossier refuses before it grades, reusing the split `eval/submit_gate.py` draws. A
binding failure says these reports are not about one artifact under one engine, and yields
NO DECISION. A criteria failure says they are, and the answer is no. Only a candidate that
survives both is a SUBMIT, and the verdict still names the submission the send destroys.

Nothing here uploads anything, and nothing here can see the Kaggle account: the state of
the two active slots is declared by the operator and checked for internal consistency
only. See docs/RELEASE_DOSSIER.md.
"""
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import statistics

from arena.seeds import REGISTRY, SPLITS, validate_seeds
from .comparison import digest
from .standing import LINEAGE_FLOOR, TOP20_BANDS
from .submit_gate import decide

# docs/FINAL_SUBMISSION_POLICY.md, items 3 and 5. The margin before the deadline is an
# operational reserve for recovering a failed upload, not a statistical optimum.
DEADLINE = datetime(2026, 9, 30, 23, 59, tzinfo=timezone.utc)
LAST_PLANNED_SWAP = datetime(2026, 9, 29, 23, 59, tzinfo=timezone.utc)
DAILY_QUOTA, RECOVERY_RESERVE, ACTIVE_SLOTS = 5, 2, 2
# A declared account state is a snapshot of something this process cannot read. Past a
# day it is a memory, and the slots may have rotated under it.
MAX_DECLARATION_AGE_HOURS = 24
SLOT_FIELDS = ('slot', 'id', 'hash')


def split_of(seeds, registry=None):
    """Which registered split these seeds are, asked of the authority that enforces it.

    `seed_registry.json` classifies every seed and `arena/seeds.py` is what refuses a
    run that mixes them. A `split` field copied into a report is a claim about that
    classification; this is the classification.
    """
    seeds = [seed for seed in (seeds or []) if type(seed) is int]
    if not seeds:
        return None
    for split in SPLITS:
        try:
            validate_seeds(seeds, split, registry or REGISTRY)
        except (ValueError, OSError):
            continue
        return split
    return None


def _disagree(label, claims):
    """One refusal when the sources that carry `label` do not carry the same value."""
    known = {name: value for name, value in claims.items() if value not in (None, '', {})}
    if len({digest(value) for value in known.values()}) <= 1:
        return []
    detail = '; '.join(f'{name} says {json.dumps(value, sort_keys=True)}'
                       for name, value in sorted(known.items()))
    return [f'The reports disagree on {label}: {detail}.']


def binding(finalist):
    """Why these reports cannot be read as one decision, if they cannot.

    Kept ahead of the criteria and separate from them: a binding failure means the
    question was assembled wrong, and no amount of good numbers underneath it repairs
    that. Every check here is between two reports, never inside one.
    """
    comparison = finalist.get('comparison') or {}
    report = finalist.get('standing') or {}
    flight = finalist.get('preflight') or {}
    snapshot = comparison.get('snapshot') or {}
    known = report.get('provenance')
    artifact, evaluated = flight.get('sha256'), snapshot.get('candidate_hash')
    reasons = []
    if not isinstance(artifact, str) or not artifact:
        reasons.append('The preflight carries no artifact sha256, so nothing can be tied '
                       'to the file that would be uploaded.')
    if not isinstance(evaluated, str) or not evaluated:
        reasons.append('The comparison carries no candidate hash.')
    if artifact and evaluated and artifact != evaluated:
        reasons.append(
            f'The comparison evaluated {evaluated} and the preflight flew {artifact}. An '
            'agent run by name hashes its sources and this module, an agent run by path '
            'hashes the file, so the two identities coincide only when the evaluation ran '
            'the built artifact itself. Re-run the comparison with the artifact path as '
            'the candidate; nothing else makes "the same SHA-256 that was evaluated" true.')
    if known is None:
        reasons.append('The standing is not bound to an artifact: loaded from matches.csv, '
                       'which drops the hash columns. Point eval.standing at the run '
                       'directory so matches.jsonl supplies the provenance.')
    elif artifact and known.get('candidate_hash') != artifact:
        reasons.append(f'The standing measured {known.get("candidate_hash")}, not the '
                       f'artifact {artifact} that was flown and would be sent.')
    known = known or {}
    reasons += _disagree('the engine fingerprint',
                         {'the comparison': snapshot.get('environment'),
                          'the standing': known.get('environment'),
                          'the preflight': flight.get('environment')})
    reasons += _disagree('the backend', {'the comparison': snapshot.get('backend'),
                                         'the standing': known.get('backend')})
    # The two panels are different populations by design -- a paired cohort against the
    # incumbent, and the meta panel -- so they need not agree on membership. Where they
    # do overlap, the same opponent has to be the same artifact.
    mine, theirs = snapshot.get('opponent_hashes') or {}, known.get('opponent_hashes') or {}
    moved = sorted(name for name in set(mine) & set(theirs) if mine[name] != theirs[name])
    if moved:
        reasons.append('Opponents changed artifact between the comparison and the '
                       'standing: ' + ', '.join(moved) + '.')
    return reasons


def run_spec(finalist):
    """Every field that must not change silently between planning, running and deciding.

    A forward-compatible stand-in for issue #46: the fields exist today, scattered across
    two reports, and hashing them gives one string that two runs can be compared by.
    """
    snapshot = (finalist.get('comparison') or {}).get('snapshot') or {}
    known = (finalist.get('standing') or {}).get('provenance') or {}
    spec = {'environment': snapshot.get('environment'), 'backend': snapshot.get('backend'),
            'configuration': snapshot.get('configuration'),
            'strong_cut': snapshot.get('cut'),
            'max_rating_age_days': snapshot.get('max_rating_age_days'),
            'ratings_sha256': snapshot.get('ratings_sha256'),
            'families_sha256': snapshot.get('families_sha256'),
            'comparison_split': (finalist.get('comparison') or {}).get('evaluation_split'),
            'comparison_panel': sorted(snapshot.get('opponent_hashes') or {}),
            'standing_environment': known.get('environment'),
            'standing_backend': known.get('backend'),
            'standing_configuration': known.get('configuration'),
            'standing_panel': sorted(known.get('opponent_hashes') or {}),
            'standing_seeds': known.get('seeds'),
            'candidate_hash': snapshot.get('candidate_hash'),
            'baseline_hash': snapshot.get('baseline_hash')}
    return {**spec, 'sha256': digest(spec)}


def criteria(finalist, *, now, registry=None):
    """The answers, once the reports are known to be about the same thing."""
    comparison = finalist.get('comparison') or {}
    report = finalist.get('standing') or {}
    flight = finalist.get('preflight') or {}
    reasons = []

    gate = decide(comparison, finalist.get('incumbent'), finalist.get('ceiling'))
    if gate['verdict'] != 'SUBMIT':
        reasons += ['Paired gate: ' + reason for reason in gate['reasons']]

    absolute = report.get('gate') or {}
    if absolute.get('verdict') != 'PASS':
        reasons += ['Standing: ' + reason for reason
                    in absolute.get('reasons') or ['no standing gate in the report.']]
    elif not absolute.get('safe'):
        reasons += ['Standing: ' + reason for reason in absolute.get('safe_reasons') or []]

    # Only ask this of a standing that can answer it. An unbound standing has no seeds
    # to classify, and reporting that as a second failure would double-count the one
    # missing fact that `binding` already refuses on.
    if report.get('provenance') is not None:
        split = split_of(report['provenance'].get('seeds'), registry)
        if split != 'validation':
            reasons.append(f'Standing: the panel ran on {split or "unregistered"} seeds. An '
                           'absolute standing that authorizes a release comes from reserved '
                           'validation seeds, like the paired comparison beside it.')

    for band in TOP20_BANDS:
        opponents = ((report.get('per_band') or {}).get(band) or {}).get('opponents') or []
        if len(opponents) < 2:
            reasons.append(f'Panel: band {band} carries {len(opponents)} opponent(s). A '
                           'decisive band represented by one artifact measures that '
                           'artifact, not the band.')

    snapshot = comparison.get('snapshot') or {}
    as_of, max_age = snapshot.get('as_of'), snapshot.get('max_rating_age_days')
    try:
        observed = date.fromisoformat(as_of)
    except (TypeError, ValueError):
        observed = None
    if observed is None or not isinstance(max_age, (int, float)):
        reasons.append('Panel: the comparison snapshot does not say when the ratings were '
                       'observed, so its freshness cannot be checked.')
    else:
        age = (now.date() - observed).days
        if age > max_age:
            reasons.append(f'Panel: the rating snapshot is {age} days old, past the '
                           f'{max_age:g}-day limit the comparison itself declares.')

    if flight.get('status') != 'PASSED':
        reasons.append(f'Preflight: status is {flight.get("status")!r}, not PASSED. The '
                       'exact file has not been shown to play a season.')
    return reasons


def _incumbent(finalist, declared):
    """The agent in the slot this send would displace -- derived, never re-typed.

    Naming the slot is enough. Copying its id and hash beside the slot label would be one
    more place for the two to drift apart, and `eval/submit_gate.py` checks that hash
    against the baseline leg that was actually run.
    """
    slot = declared.get(finalist.get('displaces'))
    # A slot declared without an id or a hash names nothing to displace. `policy` reports
    # the malformed declaration; here it simply leaves the incumbent underived, and
    # `eval/submit_gate.py` refuses to decide without one.
    if not slot or any(not isinstance(slot.get(field), str) or not slot.get(field)
                       for field in SLOT_FIELDS):
        return None
    return {'id': slot['id'], 'hash': slot['hash'],
            'displaces': f'slot {slot["slot"]} ({slot["id"]}, '
                         f'{slot.get("episodes", "unknown")} observable episodes since '
                         f'{slot.get("submitted_at", "an undeclared date")})'}


def policy(declaration, finalists, declared, *, now):
    """The account-state and calendar checks, over a state we are told rather than read."""
    reasons = []
    checked = declaration.get('checked_at')
    try:
        age = now - datetime.fromisoformat(checked)
    except (TypeError, ValueError):
        age = None
        reasons.append('The slot declaration has no parseable `checked_at`; an undated '
                       'account state cannot support a decision about that account.')
    if age is not None and age > timedelta(hours=MAX_DECLARATION_AGE_HOURS):
        reasons.append(f'The slot declaration is {age.total_seconds() / 3600:.0f} h old, '
                       f'past the {MAX_DECLARATION_AGE_HOURS} h limit; the slots rotate by '
                       'recency and may have moved under it.')
    entries = declaration.get('slots') or []
    if len(entries) > ACTIVE_SLOTS:
        reasons.append(f'{len(entries)} slots declared; the account holds {ACTIVE_SLOTS}.')
    for entry in entries:
        if any(not isinstance(entry.get(field), str) or not entry.get(field)
               for field in SLOT_FIELDS):
            reasons.append('Every declared slot must name ' + ', '.join(SLOT_FIELDS)
                           + ' as non-empty strings.')
            break

    active = {entry['hash']: entry for entry in entries if isinstance(entry.get('hash'), str)}
    taken = {}
    for finalist in finalists:
        name, slot = finalist.get('id'), finalist.get('displaces')
        if slot not in declared:
            reasons.append(f'{name} would displace slot {slot!r}, which the declaration '
                           'does not contain.')
        elif slot in taken:
            reasons.append(f'{name} and {taken[slot]} would both displace slot {slot}. Two '
                           'sends into one slot leave one of them holding nothing.')
        else:
            taken[slot] = name
        artifact = (finalist.get('preflight') or {}).get('sha256')
        if artifact in active:
            reasons.append(f'{name} is byte-identical to the agent already in slot '
                           f'{active[artifact]["slot"]}. Re-sending a file restarts its '
                           'history and changes nothing that is played.')

    # Two slots holding one file is the degenerate case of spending both on the same
    # bet, and the per-slot check above cannot see it: neither finalist is active yet.
    sent = {}
    for finalist in finalists:
        artifact = (finalist.get('preflight') or {}).get('sha256')
        if not isinstance(artifact, str) or not artifact:
            continue
        if artifact in sent:
            reasons.append(f'{finalist.get("id")} and {sent[artifact]} are the same file '
                           f'({artifact[:8]}). Two slots holding one artifact is one bet '
                           'bought twice, and the team is scored on the better of the two.')
        sent[artifact] = finalist.get('id')

    planned, used = len(finalists), declaration.get('daily_submissions_used')
    if not isinstance(used, int) or used < 0:
        reasons.append('The declaration must state `daily_submissions_used` for today; '
                       'quota does not carry over and cannot be inferred.')
    elif used + planned > DAILY_QUOTA - RECOVERY_RESERVE:
        reasons.append(f'{used} of today\'s {DAILY_QUOTA} uploads are spent and {planned} '
                       f'more are planned, leaving under the {RECOVERY_RESERVE} held back '
                       'for recovering a failed upload.')
    if now > LAST_PLANNED_SWAP:
        reasons.append(f'{now.isoformat()} is past the {LAST_PLANNED_SWAP.isoformat()} '
                       'planning cut-off, which exists to leave a day for recovery.')
    return {'reasons': reasons, 'declared_slots': entries, 'displacing': taken,
            'checked_at': checked, 'daily_submissions_used': used, 'planned_sends': planned,
            'hours_to_deadline': (DEADLINE - now).total_seconds() / 3600,
            'hours_to_planning_cutoff': (LAST_PLANNED_SWAP - now).total_seconds() / 3600}


def complementarity(finalists, *, floor=LINEAGE_FLOOR):
    """Whether the two finalists fail in the same place.

    The team is scored on the better of its two slots, so a second slot is worth what it
    covers that the first does not. Two artifacts sharing a lineage hole are one bet
    bought twice. This is reported, never a veto: a pair can be correlated and still be
    the two best things we have.
    """
    if len(finalists) < 2:
        return {'applies': False, 'note': 'One finalist; complementarity is not a question.'}
    names = [finalist.get('id') for finalist in finalists]
    lineages = [((finalist.get('standing') or {}).get('per_lineage') or {})
                for finalist in finalists]
    shared = sorted(set(lineages[0]) & set(lineages[1]))
    rates = {name: {group: lineages[i].get(group, {}).get('win_rate') for group in shared}
             for i, name in enumerate(names)}
    measured = [group for group in shared
                if all(rates[name][group] is not None for name in names)]
    both_below = [group for group in measured
                  if all(rates[name][group] < floor for name in names)]
    covered = [group for group in measured
               if len({rates[name][group] >= floor for name in names}) == 2]
    correlation = None
    if len(measured) >= 2:
        try:
            correlation = statistics.correlation(*[[rates[name][g] for g in measured]
                                                   for name in names])
        except statistics.StatisticsError:
            correlation = None
    warnings = []
    if both_below:
        warnings.append('Both finalists are held under the ' + f'{floor:.0%} floor by '
                        + ', '.join(both_below) + '. Two slots, one hole.')
    if correlation is not None and correlation >= .9 and not covered:
        warnings.append(f'Per-lineage results correlate at {correlation:.2f} and neither '
                        'finalist covers a lineage the other loses; the second slot is '
                        'buying very little.')
    if not shared:
        warnings.append('The two standings share no lineage, so they were measured against '
                        'different populations and cannot be compared here.')
    return {'applies': True, 'finalists': names, 'shared_lineages': shared,
            'unmeasured_lineages': sorted(set(shared) - set(measured)),
            'win_rate_by_lineage': rates, 'both_below_floor': both_below,
            'covered_by_exactly_one': covered, 'correlation': correlation,
            'lineage_floor': floor,
            'warnings': warnings or ['The two finalists do not share a measured hole.']}


def dossier(finalists, declaration, *, now=None, registry=None):
    """The whole decision, for one or two finalists and one declared account state."""
    now = now or datetime.now(timezone.utc)
    declared = {entry['slot']: entry for entry in (declaration.get('slots') or [])
                if isinstance(entry.get('slot'), str)}
    account = policy(declaration, finalists, declared, now=now)
    rows = []
    for finalist in finalists:
        bound = dict(finalist, incumbent=_incumbent(finalist, declared))
        refusals = binding(bound)
        failures = criteria(bound, now=now, registry=registry)
        # An account-level problem blocks every send, so it is a failure of each candidate
        # rather than a footnote a reader has to remember to apply.
        failures += ['Policy: ' + reason for reason in account['reasons']]
        verdict = ('NO DECISION' if refusals and not failures
                   else 'NO SUBMIT' if failures else 'SUBMIT')
        flight = finalist.get('preflight') or {}
        rows.append({
            'id': finalist.get('id'), 'verdict': verdict,
            'artifact': flight.get('artifact'), 'artifact_sha256': flight.get('sha256'),
            'evaluated_hash': ((finalist.get('comparison') or {}).get('snapshot') or {}
                               ).get('candidate_hash'),
            'preflight_status': flight.get('status'),
            'displaces': finalist.get('displaces'), 'incumbent': bound['incumbent'],
            'run_spec': run_spec(finalist),
            'paired': decide(finalist.get('comparison') or {}, bound['incumbent'],
                             finalist.get('ceiling')),
            'standing': (finalist.get('standing') or {}).get('gate'),
            'standing_split': split_of(((finalist.get('standing') or {}).get('provenance')
                                        or {}).get('seeds'), registry),
            'refusals': refusals, 'failures': failures})
    verdicts = [row['verdict'] for row in rows]
    return {'schema_version': 1, 'policy_version': 1, 'generated_at': now.isoformat(),
            'verdict': ('SUBMIT' if 'SUBMIT' in verdicts else 'NO SUBMIT'
                        if 'NO SUBMIT' in verdicts else 'NO DECISION'),
            'candidates': rows, 'account': account,
            'complementarity': complementarity(finalists),
            'policy': {'deadline': DEADLINE.isoformat(),
                       'last_planned_swap': LAST_PLANNED_SWAP.isoformat(),
                       'daily_quota': DAILY_QUOTA, 'recovery_reserve': RECOVERY_RESERVE,
                       'active_slots': ACTIVE_SLOTS,
                       'source': 'docs/FINAL_SUBMISSION_POLICY.md'},
            'note': 'Read-only. No submission was made and the Kaggle account was not read.'}


def _short(value):
    return '--------' if not isinstance(value, str) or not value else value[:8]


def render(result):
    """The block a human reads before deciding. Both finalists side by side, always."""
    rows = result['candidates']
    width = max([24] + [len(str(row['id'] or '')) + 2 for row in rows])
    def line(label, cells):
        return f'  {label:<22}' + ''.join(f'{str(cell):<{width}}' for cell in cells)
    out = [f'RELEASE DOSSIER  {result["generated_at"]}',
           f'verdict = {result["verdict"]}', '',
           line('', [row['id'] for row in rows]),
           line('artifact sha256', [_short(row['artifact_sha256']) for row in rows]),
           line('evaluated hash', [_short(row['evaluated_hash']) for row in rows]),
           line('run spec', [_short(row['run_spec']['sha256']) for row in rows]),
           line('paired gate', [row['paired']['verdict'] for row in rows]),
           line('standing', [f'{(row["standing"] or {}).get("verdict")}'
                             f'{" / defended" if (row["standing"] or {}).get("safe") else ""}'
                             for row in rows]),
           line('standing seeds', [row['standing_split'] or 'unregistered' for row in rows]),
           line('preflight', [row['preflight_status'] or 'missing' for row in rows]),
           line('displaces', [row['displaces'] for row in rows]),
           line('verdict', [row['verdict'] for row in rows]), '']
    account = result['account']
    out.append(f'{account["hours_to_deadline"]:.0f} h to the deadline, '
               f'{account["hours_to_planning_cutoff"]:.0f} h to the planning cut-off; '
               f'{account["daily_submissions_used"]} of {DAILY_QUOTA} uploads spent today, '
               f'{account["planned_sends"]} planned.')
    for row in rows:
        out += ['', f'{row["id"]}: {row["verdict"]}']
        out += ['  refuses: ' + reason for reason in row['refusals']]
        out += ['  fails:   ' + reason for reason in row['failures']]
        if not row['refusals'] and not row['failures']:
            out.append('  sends ' + str(row['artifact']) + ', destroying '
                       + (row['incumbent'] or {}).get('displaces', 'nothing declared'))
    if result['complementarity']['applies']:
        out += ['', 'complementarity']
        out += ['  - ' + note for note in result['complementarity']['warnings']]
    return '\n'.join(out) + '\n'


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--slots', required=True,
                        help='JSON declaring the active submission slots and today\'s quota')
    parser.add_argument('--candidate', action='append', default=[], metavar='ID:SLOT',
                        help='finalist id and the slot it displaces, e.g. v004:A')
    parser.add_argument('--comparison', action='append', default=[],
                        help='paired comparison against the agent in that slot')
    parser.add_argument('--standing', action='append', default=[],
                        help='eval.standing report for the same artifact')
    parser.add_argument('--preflight', action='append', default=[],
                        help='submission.preflight report for the file to upload')
    parser.add_argument('--ceiling', help='optional comparison against the strongest panel artifact')
    parser.add_argument('--registry', help='seed registry; defaults to seed_registry.json')
    parser.add_argument('--output')
    args = parser.parse_args()
    counts = {len(args.candidate), len(args.comparison), len(args.standing), len(args.preflight)}
    if len(counts) != 1 or not args.candidate:
        parser.error('Pass one --comparison, --standing and --preflight per --candidate')

    audit = []
    def load(path):
        raw = Path(path).read_bytes()
        audit.append({'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest()})
        return json.loads(raw)

    ceiling = load(args.ceiling) if args.ceiling else None
    finalists = []
    for spec, comparison, report, flight in zip(args.candidate, args.comparison,
                                                args.standing, args.preflight):
        name, _, slot = spec.partition(':')
        if not slot:
            parser.error(f'--candidate {spec!r} must be ID:SLOT, naming the slot it displaces')
        finalists.append({'id': name, 'displaces': slot, 'comparison': load(comparison),
                          'standing': load(report), 'preflight': load(flight),
                          'ceiling': ceiling})
    result = dossier(finalists, load(args.slots), registry=args.registry)
    result['audit'] = {'inputs': audit}
    print(render(result), end='')
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2, default=str) + '\n')


if __name__ == '__main__':
    main()
