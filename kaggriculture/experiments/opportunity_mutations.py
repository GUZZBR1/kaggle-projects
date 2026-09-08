"""Unit work proposed from the tile the unit is actually standing on, not from a guess.

The blind generator in `production_mutations` fills every idle slot of a block with the
same command and lets the engine decide. Measured, that produced between 1 696 and 1 800
ineffective actions per sixteen-game leg against 128 for the incumbent, and no win: almost
every proposal was a command with no target. This generator reads the incumbent's own
observed trajectory through the block and proposes only work whose precondition already
holds on the tile under that unit at that turn:

| work | precondition in the engine |
|---|---|
| `WATER` | the tile is a `PLANT` and `watered_today` is false |
| `HARVEST` | `yield_units > 0`, and for a plant the crop is past `first_yield_day` |
| `FERTILIZE` | the tile is a `PLANT` and the unit carries `FERTILIZER` |
| `FEED` | an animal is placed, `fed_today` is false and the unit carries `WHEAT` |
| `CARE` | an animal is placed and `cared_today` is false |
| `COLLECT_FERTILIZER` | an animal is placed and `fertilizer_available` is true |

A locked tile arrives as the string `LOCKED` and admits nothing, which falls out of the
dict check rather than needing its own rule.

Two honest limits. The opportunities are read from the incumbent's trajectory, so applying
several at once can invalidate the later ones -- a second `WATER` on the same tile and day
is a no-op by the same rule that made the first one legal. Same-day duplicates per tile are
therefore collapsed to their earliest turn, and what survives that is still measured, never
assumed. And a trajectory belongs to one context, so opportunities are intersected across
every probed context and only those present in all of them are proposed.
"""
import copy

from experiments.tape_harvest import tape_digest

WORK = ('WATER', 'HARVEST', 'CARE', 'FEED', 'COLLECT_FERTILIZER', 'FERTILIZE')
# The engine's own table, not an estimate: HARVEST returns nothing on a plant younger than
# this, whatever `yield_units` says. Read from kaggle_environments 1.32.7 CROPS.
FIRST_YIELD_DAY = {'WHEAT': 2, 'CARROT': 2, 'TOMATO': 8, 'STRAWBERRY': 10, 'MELON': 10}


def units(action):
    if isinstance(action.get('farmer'), list):
        yield 'farmer', None, action['farmer']
    for index, order in enumerate(action.get('hands', [])):
        if isinstance(order, list):
            yield 'hands', index, order


def position(observation, seat, role, index):
    farm = observation['farms'][seat]
    if role == 'farmer':
        return tuple(farm['farmer'])
    hands = farm['hands']
    return tuple(hands[index]) if index < len(hands) else None


def tile_at(observation, seat, spot):
    x, y = spot
    tiles = observation['farms'][seat]['tiles']
    if not 0 <= y < len(tiles) or not 0 <= x < len(tiles[y]):
        return None
    tile = tiles[y][x]
    return tile if isinstance(tile, dict) else None


def carried(observation, unit, item):
    inventories = observation['private'].get('inventories') or []
    return unit < len(inventories) and (inventories[unit] or {}).get(item, 0) > 0


def admissible(tile, observation, day, unit):
    """Every work whose precondition already holds on this tile for this unit."""
    if tile is None:
        return []
    found = []
    if tile.get('kind') == 'PLANT':
        if not tile.get('watered_today'):
            found.append('WATER')
        if carried(observation, unit, 'FERTILIZER'):
            found.append('FERTILIZE')
        mature = day - tile.get('planted_day', day) >= FIRST_YIELD_DAY.get(tile.get('crop'), 99)
        if tile.get('yield_units', 0) > 0 and mature:
            found.append('HARVEST')
    elif tile.get('animal'):
        if tile.get('yield_units', 0) > 0:
            found.append('HARVEST')
        if not tile.get('fed_today') and carried(observation, unit, 'WHEAT'):
            found.append('FEED')
        if not tile.get('cared_today'):
            found.append('CARE')
        if tile.get('fertilizer_available'):
            found.append('COLLECT_FERTILIZER')
    return found


def opportunities(actions, observation_sets, start, end):
    """Idle slots whose tile admits work, in every probed context.

    An opportunity is `(turn, role, index, work)`. Keyed that way, the intersection across
    contexts is exact: the same slot of the same turn must admit the same work in all of
    them, which is what makes a proposal worth spending games on.
    """
    per_context = []
    for observations in observation_sets:
        found = set()
        for turn in range(start, end):
            observation = observations.get(turn)
            if observation is None:
                continue
            seat = observation['player']
            day = observation['day']
            for role, index, order in units(actions[turn]):
                if order != ['PASS']:
                    continue
                spot = position(observation, seat, role, index)
                if spot is None:
                    continue
                # `private.inventories` is indexed farmer first, then hands in order.
                unit = 0 if role == 'farmer' else index + 1
                tile = tile_at(observation, seat, spot)
                for work in admissible(tile, observation, day, unit):
                    found.add((turn, role, index, work, day, spot))
        per_context.append(found)
    if not per_context:
        return []
    shared = set.intersection(*per_context)
    # Same tile, same day, same work: the engine no-ops every repeat, so keep the earliest.
    earliest = {}
    for turn, role, index, work, day, spot in sorted(shared):
        earliest.setdefault((day, spot, work), (turn, role, index, work))
    return sorted(earliest.values())


def apply_work(tape, turn, role, index, work):
    if role == 'farmer':
        tape[turn]['farmer'] = [work]
    else:
        tape[turn]['hands'][index] = [work]


def opportunity_mutations(actions, start, end, count, rng, excluded=(), observation_sets=()):
    if len(actions) != 719 or not 0 <= start < end <= 719 or count < 1:
        raise ValueError('Require a complete tape, bounded block and positive proposal count')
    available = opportunities(actions, observation_sets, start, end)
    descriptors = []
    for work in WORK:
        targets = [item for item in available if item[3] == work]
        if targets:
            descriptors.append(dict(kind='admissible_work', work=work, targets=targets))
    if len({item[3] for item in available}) > 1:
        descriptors.append(dict(kind='admissible_work', work='ALL', targets=available))
    singles = [dict(kind='admissible_slot', work=work, targets=[(turn, role, index, work)])
               for turn, role, index, work in available]
    rng.shuffle(singles)
    descriptors.extend(singles)

    seen, result = set(excluded) | {tape_digest(actions)}, []
    for descriptor in descriptors:
        tape = copy.deepcopy(actions)
        for turn, role, index, work in descriptor['targets']:
            apply_work(tape, turn, role, index, work)
        identity = tape_digest(tape)
        if identity in seen:
            continue
        seen.add(identity)
        summary = dict(kind=descriptor['kind'], work=descriptor['work'],
                       targets=len(descriptor['targets']),
                       turns=sorted({turn for turn, *_ in descriptor['targets']})[:8])
        result.append(dict(actions=tape, sha256=identity, mutation=summary))
        if len(result) == count:
            break
    return result
