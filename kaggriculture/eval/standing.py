"""What the harness reports first: win rate against the top cohort, not rating, not gold.

The prize in Kaggriculture is a cliff -- every position from first to tenth pays the
same and eleventh pays nothing -- so the question is not "did the candidate improve"
but "is it strong enough, in absolute terms, against the top". That is a different
statistic from the paired delta in `eval/ladder.py`, which stays the promotion test
between two of *our* agents. This module answers the standing question.

Rating deliberately does not appear. It lags, it depends on the age and trajectory of
a submission, the final Bradley-Terry recomputation discards it as the fundamental
criterion, and the strongest agents are being withdrawn from the ladder so that the
best observable opponent is not the best existing one. Absolute win rate against a
panel we control is the quantity that survives all four of those.

Thresholds are tiered by the opponent's standing rather than by one rating cut, because
a candidate that beats ranks 30-100 comfortably and only draws with the top ten is not
a top-ten candidate. See docs/TOP10_STANDING.md.
"""
import statistics

from .metrics import blocked_interval

# Rank bands and the win rate each one has to clear before a top-ten finish is credible.
BANDS = (('top10', 1, 10, .55), ('rank10_30', 11, 30, .60), ('rank30_100', 31, 100, .65))
TOP20_BANDS = ('top10', 'rank10_30')
SAFE_TOP20_WIN_RATE = .58
# A structural 25-75 against a lineage the meta is full of sinks a run whatever the
# aggregate says, so the floor is a gate condition and not a diagnostic.
LINEAGE_FLOOR = .40
# What a match row has to carry before a standing can name the artifact it measured.
PROVENANCE_FIELDS = ('candidate_hash', 'environment', 'backend')


def band_of(rank):
    """None for an unranked opponent: unknown never counts into a band, only out of one."""
    if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
        return None
    for name, low, high, _ in BANDS:
        if low <= rank <= high:
            return name
    return None


def _rate(rows):
    if not rows:
        return {'games': 0, 'win_rate': None, 'ci95': [None, None]}
    return {'games': len(rows), 'win_rate': statistics.mean(r['score'] for r in rows),
            'ci95': blocked_interval(rows, samples=10000)}


def provenance(rows):
    """What this standing is a standing *of*, or None when the rows cannot say.

    `matches.csv` drops the hash columns, so a standing loaded from it measures an
    artifact it cannot name: the win rates are right and nothing ties them to the agent
    a release decision is about. Supplying that tie here would be the same hand-carry
    `eval/dossier.py` exists to remove, so the report states that it has none and the
    dossier refuses the combination. A run directory keeps `matches.jsonl`, which does
    carry the fields, and `main` prefers it for that reason.
    """
    if any(field not in row for row in rows for field in PROVENANCE_FIELDS):
        return None
    first = rows[0]
    for field in PROVENANCE_FIELDS:
        if any(row[field] != first[field] for row in rows):
            raise ValueError(f'Standing mixes {field} across rows; one standing is one '
                             'artifact, under one engine, on one backend')
    hashes = {}
    for row in rows:
        if 'opponent_hash' not in row:
            continue
        if hashes.setdefault(row['opponent'], row['opponent_hash']) != row['opponent_hash']:
            raise ValueError(f'Opponent {row["opponent"]} changed artifact mid-panel')
    return {'candidate_hash': first['candidate_hash'], 'environment': first['environment'],
            'backend': first['backend'],
            'configuration': {key: value for key, value
                              in (first.get('configuration') or {}).items() if key != 'seed'},
            'opponent_hashes': dict(sorted(hashes.items())),
            'seeds': sorted({row['seed'] for row in rows})}


def standing(rows, ranks=None, lineages=None, *, panel=None, floor=LINEAGE_FLOOR,
             safe_top20=SAFE_TOP20_WIN_RATE):
    """Absolute standing of one agent against a panel, banded by opponent rank.

    `rows` are match records carrying opponent, seat, seed and score. `ranks` maps an
    opponent id to its leaderboard rank; an opponent absent from it is reported under
    `unbanded` and gates nothing. `lineages` groups opponents that share provenance --
    the manifest family is the usual source -- and defaults to one lineage per opponent.

    `panel` is a snapshot from `eval/panel.py`, and it is the form a release standing
    should take: the ranks and the lineages are derived from it instead of typed beside
    the run, the report records the revision it stood against, and a panel that cannot
    support the question -- an empty decisive band, a band carried by one lineage, an
    observation past its freshness window -- fails the gate rather than being averaged
    into a number that looks fine. Passing both is a contradiction, not a merge.
    """
    if not rows:
        raise ValueError('Cannot report standing over an empty panel')
    reference = None
    if panel is not None:
        from . import panel as panels
        if ranks is not None or lineages is not None:
            raise ValueError('A panel snapshot already carries the ranks and the lineages; '
                             'passing them beside it is the drift the snapshot removes')
        ranks, lineages = panels.ranks(panel), panels.lineages(panel)
        reference = panels.reference(panel)
    elif ranks is None:
        raise ValueError('Standing needs either a panel snapshot or a ranks mapping')
    for row in rows:
        if row['score'] not in (0., .5, 1.):
            raise ValueError('Standing is a wins-only statistic; margin is not a score')
    lineages = dict(lineages or {})
    opponents = sorted({row['opponent'] for row in rows})
    bands = {name: band_of(ranks.get(name)) for name in opponents}
    seats = sorted({row['seat'] for row in rows})

    def subset(predicate):
        return [row for row in rows if predicate(row['opponent'])]

    per_band = {}
    for name, _, _, threshold in BANDS:
        measured = _rate(subset(lambda o, n=name: bands[o] == n))
        per_band[name] = {**measured, 'threshold': threshold,
                          'opponents': sorted(o for o in opponents if bands[o] == name),
                          # An empty band is unmeasured, which is not a pass.
                          'pass': measured['win_rate'] is not None and measured['win_rate'] >= threshold}
    per_lineage = {group: _rate(subset(lambda o, g=group: lineages.get(o, o) == g))
                   for group in sorted({lineages.get(o, o) for o in opponents})}
    worst = min(per_lineage.items(), key=lambda item: item[1]['win_rate'])
    top20 = _rate(subset(lambda o: bands[o] in TOP20_BANDS))

    report = {
        'games': len(rows), 'seed_blocks': len({row['seed'] for row in rows}),
        'overall': _rate(rows),
        'per_seat': {seat: _rate([r for r in rows if r['seat'] == seat]) for seat in seats},
        'per_band': per_band,
        'unbanded': {**_rate(subset(lambda o: bands[o] is None)),
                     'opponents': sorted(o for o in opponents if bands[o] is None),
                     'gates_nothing': True},
        'per_lineage': per_lineage,
        'worst_lineage': {'lineage': worst[0], **worst[1]},
        'median_lineage_win_rate': statistics.median(
            row['win_rate'] for row in per_lineage.values()),
        'top20': top20,
        'lineage_floor': floor,
        'provenance': provenance(rows),
        'panel': reference,
    }
    report['gate'] = gate(report, floor=floor, safe_top20=safe_top20)
    return report


def gate(report, *, floor=LINEAGE_FLOOR, safe_top20=SAFE_TOP20_WIN_RATE):
    """Two tiers: credible top-ten contender, and a standing worth defending.

    The first tier is every populated band over its threshold with no lineage collapse.
    The second adds an absolute top-20 win rate and an interval clearly off 50%, which
    is the point at which the team stops trying to enter the top ten and is competing
    in it.
    """
    reasons = []
    # The panel refuses first, and for a different reason than the numbers do: a band
    # carried by one lineage or a snapshot a fortnight old makes every win rate below it
    # a statement about the wrong population. A standing over a panel that cannot answer
    # the question is not a weaker pass, it is not an answer.
    for refusal in ((report.get('panel') or {}).get('gate') or {}).get('refusals') or []:
        reasons.append('Panel: ' + refusal)
    for name, _, _, threshold in BANDS:
        row = report['per_band'][name]
        if row['win_rate'] is None:
            reasons.append(f'Band {name} is unmeasured: no opponent in the panel carries that rank.')
        elif not row['pass']:
            reasons.append(f'Band {name} is {row["win_rate"]:.1%}, under the {threshold:.0%} it has to clear.')
    worst = report['worst_lineage']
    if worst['win_rate'] is not None and worst['win_rate'] < floor:
        reasons.append(f'Lineage {worst["lineage"]} holds us to {worst["win_rate"]:.1%}, '
                       f'a structural matchup rather than variance.')
    verdict = 'FAIL' if reasons else 'PASS'
    top20, safe = report['top20'], []
    if verdict == 'FAIL':
        safe = ['Not a contender yet.']
    else:
        if top20['win_rate'] is None or top20['win_rate'] < safe_top20:
            safe.append(f'Top-20 win rate is {_pct(top20["win_rate"])}, under {safe_top20:.0%}.')
        if top20['ci95'][0] is None or top20['ci95'][0] <= .5:
            safe.append(f'The top-20 interval lower bound is {_pct(top20["ci95"][0])}, not clearly above 50%.')
    return {'verdict': verdict, 'reasons': reasons or ['Every populated band clears its '
            'threshold and no lineage holds us below the floor.'],
            'safe': not safe, 'safe_reasons': safe or ['Top-20 win rate and interval both '
            'clear the defended-standing bar.']}


def _pct(value):
    return 'unmeasured' if value is None else f'{value:.1%}'


def render(report, candidate='candidate', panel='TOP20 META'):
    """The block the harness prints. Win rate leads; nothing else is above it."""
    overall, low, high = report['overall'], *report['overall']['ci95']
    seats = '   '.join(f'seat{seat} = {_pct(row["win_rate"])}'
                       for seat, row in sorted(report['per_seat'].items()))
    stood = report.get('panel') or {}
    against = (f'{panel} (panel {stood["revision"][:12]}, observed {stood["observed_at"]})'
               if stood else f'{panel} (no panel snapshot)')
    lines = [f'Candidate {candidate}', f'vs {against}', '',
             f'WR = {_pct(overall["win_rate"])}   '
             f'95% CI = [{_pct(low)}, {_pct(high)}]   '
             f'({overall["games"]} games, {report["seed_blocks"]} seed blocks)',
             seats,
             f'worst lineage = {_pct(report["worst_lineage"]["win_rate"])} '
             f'({report["worst_lineage"]["lineage"]})   '
             f'median lineage = {_pct(report["median_lineage_win_rate"])}', '']
    for name, _, _, threshold in BANDS:
        row = report['per_band'][name]
        lines.append(f'  {name:<12} {_pct(row["win_rate"]):>10}  need {threshold:.0%}  '
                     f'{"PASS" if row["pass"] else "FAIL"}  ({row["games"]} games)')
    if report['unbanded']['opponents']:
        lines.append(f'  {"unbanded":<12} {_pct(report["unbanded"]["win_rate"]):>10}  '
                     f'gates nothing  ({", ".join(report["unbanded"]["opponents"])})')
    lines += ['', f'promotion gate = {report["gate"]["verdict"]}',
              f'defended standing = {"YES" if report["gate"]["safe"] else "NO"}']
    lines += ['  - ' + reason for reason in report['gate']['reasons']]
    if not report['gate']['safe']:
        lines += ['  - ' + reason for reason in report['gate']['safe_reasons']]
    return '\n'.join(lines) + '\n'


def main():
    import argparse
    import json
    from pathlib import Path
    from .near_ties import _rows
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', help='matches.csv file or results directory')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--panel', dest='panel_snapshot',
                       help='a filed eval.panel revision; the form a release standing takes')
    group.add_argument('--ranks', help='JSON mapping opponent id to leaderboard rank')
    parser.add_argument('--lineages', help='JSON mapping opponent id to lineage; defaults to the manifest family')
    parser.add_argument('--candidate', default='candidate')
    parser.add_argument('--panel-label', default='TOP20 META', dest='panel')
    parser.add_argument('--output')
    args = parser.parse_args()
    from .comparison import load_families
    from .ladder import opponent_id
    # Prefer matches.jsonl: matches.csv drops the hash columns, and they are what binds
    # this standing to one artifact for eval.dossier.
    run = Path(args.run)
    full = run / 'matches.jsonl' if run.is_dir() else None
    rows = ([json.loads(line) for line in full.read_text().splitlines() if line]
            if full is not None and full.exists() else _rows(args.run))
    for row in rows:
        row['opponent'] = opponent_id(row['opponent'])
    if args.panel_snapshot:
        from .panel import load as load_panel
        if args.lineages:
            parser.error('--lineages contradicts --panel: the snapshot carries the lineages')
        report = standing(rows, panel=load_panel(args.panel_snapshot))
    else:
        lineages = (json.loads(Path(args.lineages).read_text()) if args.lineages
                    else load_families())
        report = standing(rows, json.loads(Path(args.ranks).read_text()), lineages)
    print(render(report, args.candidate, args.panel), end='')
    if args.output:
        Path(args.output).write_text(json.dumps(report, indent=2, default=str) + '\n')


if __name__ == '__main__':
    main()
