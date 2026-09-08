"""Compare tape blocks at a shared boundary, and score how cleanly they join.

The public method behind the strongest artifacts is not "collect tapes". It is:
cut recorded games at the boundaries where the town reveals itself, test candidate
blocks at the *same* boundary on fresh seeds and both seats, then generate better
blocks scored by the state they hand to the block after them. Our arena already
does paired comparison, but only of whole agents, so the middle step is missing
and nothing downstream can be built without it.

A block is not portable on its own. It assumes a farm: hands hired, tiles planted,
goods in the shed, the farmer standing somewhere. Splice it after a prefix that
leaves a different farm and its actions address things that are not there. That
is what `join_distance` measures, and whether it predicts the spliced result is
the question that decides if a search can use it instead of playing every game.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

BLOCK = 72
TURNS = 719
# What a following block actually depends on, and roughly how much.
WEIGHTS = {'money': 1.0, 'hands': 6.0, 'farmer': 3.0, 'quadrants': 8.0,
           'tiles': 1.5, 'shed': 0.5, 'seeds': 0.5, 'carried': 0.5}


def boundaries(block=BLOCK, turns=TURNS):
    """Cut points: the town unlocks a shop every three days, so blocks align to that."""
    return [cut for cut in range(block, turns, block)]


def fingerprint(observation, seat):
    """The part of the world a following block was recorded against."""
    farm = observation['farms'][seat]
    private = observation['private']
    tiles = Counter()
    for row in farm['tiles']:
        for tile in row:
            if isinstance(tile, dict):
                kind = tile.get('kind')
                tiles[f"{kind}:{tile.get('crop') or tile.get('animal') or ''}"] += 1
    carried = Counter()
    for inventory in private['inventories'] or []:
        carried.update({k: v for k, v in (inventory or {}).items() if v})
    return {
        'money': float(farm['money']),
        'farmer': list(farm['farmer']),
        'hands': [list(p) for p in farm['hands']],
        'quadrants': len(farm['unlocked_quadrants']),
        'tiles': dict(tiles),
        'shed': {k: v for k, v in private['shed'].items() if v},
        'seeds': {k: v for k, v in private['seeds'].items() if v},
        'carried': dict(carried),
    }


def _counter_distance(left, right):
    keys = set(left) | set(right)
    total = sum(abs(left.get(k, 0) - right.get(k, 0)) for k in keys)
    scale = max(1, sum(left.values()), sum(right.values()))
    return total / scale


def _grid_distance(left, right, board=10):
    return (abs(left[0] - right[0]) + abs(left[1] - right[1])) / (2 * board)


def join_distance(left, right, weights=None):
    """How far the world a block was recorded in sits from the world it would join.

    Zero means the prefix hands the block exactly the farm it expects. Each term
    is normalised to roughly 0..1 before weighting, so no single term dominates
    by unit alone; the weights say what a block actually cannot recover from.
    Missing hands and locked quadrants are unrecoverable inside one block, cash
    and shed contents are not, and the weights reflect that ordering.
    """
    weights = dict(WEIGHTS if weights is None else weights)
    parts = {}
    high = max(abs(left['money']), abs(right['money']), 1.0)
    parts['money'] = abs(left['money'] - right['money']) / high
    parts['quadrants'] = abs(left['quadrants'] - right['quadrants']) / 4.0
    count = max(1, len(left['hands']), len(right['hands']))
    parts['hands'] = abs(len(left['hands']) - len(right['hands'])) / count
    parts['farmer'] = _grid_distance(left['farmer'], right['farmer'])
    for key in ('tiles', 'shed', 'seeds', 'carried'):
        parts[key] = _counter_distance(left[key], right[key])
    total = sum(weights[k] * v for k, v in parts.items())
    return {'distance': total / sum(weights.values()), 'parts': parts}


def splice(prefix, suffix, cut):
    """Play `prefix` up to `cut`, then `suffix` from `cut` on."""
    if not 0 < cut < len(prefix):
        raise ValueError(f'cut {cut} outside the tape')
    if len(prefix) != len(suffix):
        raise ValueError('Tapes must cover the same number of turns')
    return [dict(action) for action in prefix[:cut]] + [dict(action) for action in suffix[cut:]]


def states_at(replay_path, seat, cuts):
    """Fingerprint one recorded game at each cut."""
    turns = json.loads(Path(replay_path).read_text())['turns']
    by_step = {turn['step']: turn for turn in turns}
    states = {}
    for cut in cuts:
        turn = by_step.get(cut)
        if turn is None:
            continue
        states[cut] = fingerprint(turn['observations'][seat], seat)
    return states


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--replays', required=True, help='comma-separated lab replay files')
    parser.add_argument('--seat', type=int, default=0)
    parser.add_argument('--block', type=int, default=BLOCK)
    parser.add_argument('--output')
    args = parser.parse_args()
    cuts = boundaries(args.block)
    states = {path: states_at(path, args.seat, cuts) for path in args.replays.split(',')}
    report = {'block': args.block, 'cuts': cuts, 'pairs': []}
    names = list(states)
    for cut in cuts:
        for left in names:
            for right in names:
                if left == right or cut not in states[left] or cut not in states[right]:
                    continue
                measured = join_distance(states[left][cut], states[right][cut])
                report['pairs'].append({'cut': cut, 'prefix': left, 'suffix': right,
                                        'distance': round(measured['distance'], 4),
                                        'parts': {k: round(v, 4) for k, v in measured['parts'].items()}})
    text = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(text + '\n', encoding='utf-8')
    print(json.dumps({'cuts': len(cuts), 'pairs': len(report['pairs'])}, indent=2))


if __name__ == '__main__':
    main()
