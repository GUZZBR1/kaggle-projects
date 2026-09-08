"""How much win rate is reachable by deciding games that are already almost decided.

Issue #41 step one. A front-run or a terminal-liquidation layer can only convert games
the arena already ends within a few coins; every other loss is an economy gap that no
sell timing repairs. This module measures that reachable headroom before anyone builds
the layer, and is meant to be re-run whenever the panel is refreshed: the headroom is a
property of the opponents we are currently paired with, not of our agent alone.

`docs/FRONT_RUN_HEADROOM.md` records what the instrument says today,
`docs/NEAR_TIE_TRIAGE.md` the hand count that preceded it, and
`docs/PAIRED_EVALUATION.md` the release bar the headroom has to clear.
"""
import csv
from pathlib import Path

from .ladder import opponent_id

DEFAULT_THRESHOLDS = (50, 500)


def _rows(source):
    """Accept a matches.csv path, a results directory, or already-parsed rows."""
    if isinstance(source, (str, Path)):
        path = Path(source)
        if path.is_dir():
            path = path / 'matches.csv'
        with path.open() as handle:
            return [dict(row, seat=int(row['seat']), score=float(row['score']),
                         margin=float(row.get('margin', row.get('margin_diagnostic', 0))))
                    for row in csv.DictReader(handle)]
    return [dict(row) for row in source]


def _tally(rows, threshold):
    """Games we do not win that the arena decided inside `threshold` coins.

    A tie is worth half a win already, so flipping one is worth half as much as
    flipping a loss. Counting them as equal would overstate the headroom.
    """
    losses = [r for r in rows if r['score'] < .5 and abs(r['margin']) <= threshold]
    ties = [r for r in rows if r['score'] == .5 and abs(r['margin']) <= threshold]
    reachable = len(losses) + .5 * len(ties)
    return {'games': len(rows), 'losses_within': len(losses), 'ties_within': len(ties),
            'win_rate': sum(r['score'] for r in rows) / len(rows) if rows else None,
            'headroom': reachable / len(rows) if rows else None,
            'ceiling_win_rate': ((sum(r['score'] for r in rows) + reachable) / len(rows)
                                 if rows else None)}


def near_ties(source, thresholds=DEFAULT_THRESHOLDS):
    """Reachable headroom overall, per opponent, and per seat.

    Per seat because a market race is resolved by order index between the two seats:
    a layer that only pays from one side is a different finding from one that pays
    from both, and an aggregate hides it.
    """
    rows = _rows(source)
    if not rows:
        raise ValueError('No match rows to measure')
    for row in rows:
        row['opponent'] = opponent_id(row['opponent'])
    thresholds = sorted({int(t) for t in thresholds})
    if not thresholds or thresholds[0] < 0:
        raise ValueError('Thresholds must be non-negative and non-empty')
    opponents = sorted({row['opponent'] for row in rows})
    return {
        'games': len(rows),
        'thresholds': thresholds,
        'overall': {t: _tally(rows, t) for t in thresholds},
        'per_opponent': {name: {t: _tally([r for r in rows if r['opponent'] == name], t)
                                for t in thresholds} for name in opponents},
        'per_seat': {seat: {t: _tally([r for r in rows if r['seat'] == seat], t)
                            for t in thresholds} for seat in sorted({r['seat'] for r in rows})},
    }


def verdict(measurement, threshold=DEFAULT_THRESHOLDS[0], bar=.02):
    """Whether the reachable headroom is worth building an opponent model for.

    `bar` defaults to two points of win rate. Below that the effect cannot produce the
    strictly positive CI95 that `eval.submit_gate` requires over 100 paired blocks, so
    the layer would be unfalsifiable in the only measurement that promotes anything.
    """
    headroom = measurement['overall'][threshold]['headroom']
    return {'threshold': threshold, 'headroom': headroom, 'bar': bar,
            'build': headroom is not None and headroom >= bar,
            'reason': (f'{headroom:.4f} of games are within {threshold} coins and not won, '
                       f'{"at or above" if headroom is not None and headroom >= bar else "below"} '
                       f'the {bar:.2f} bar a paired release gate can resolve.')}


def main():
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('runs', nargs='+', help='matches.csv files or results directories')
    parser.add_argument('--thresholds', default=','.join(str(t) for t in DEFAULT_THRESHOLDS))
    parser.add_argument('--bar', type=float, default=.02)
    parser.add_argument('--output')
    args = parser.parse_args()
    thresholds = [int(t) for t in args.thresholds.split(',') if t]
    report = {}
    for run in args.runs:
        measurement = near_ties(run, thresholds)
        measurement['verdict'] = verdict(measurement, thresholds[0], args.bar)
        report[str(run)] = measurement
    text = json.dumps(report, indent=2, default=str) + '\n'
    if args.output:
        Path(args.output).write_text(text)
    print(text, end='')


if __name__ == '__main__':
    main()
