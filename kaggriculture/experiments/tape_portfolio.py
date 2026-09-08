"""Emit a routed portfolio of tapes: several recordings and a rule for choosing.

A single tape is open-loop and cannot react to the world it wakes up in, which
matters here because the world is not visible at the start. At turn 0 the town has
no shops and every market price is the same in every game; the first shop unlocks
on day 3 and one more every three days after. So the information a farm plan would
want simply does not exist yet, and it arrives on a fixed 72-turn schedule.

That is why the strong public artifacts branch at 72-turn block boundaries: those
are exactly the moments when the game has told you something new. This module
builds the same shape of agent from a measured tape library. The routing rules are
decision lists over a public feature vector, fitted elsewhere against measured
rollouts; here we only render them into a standalone submission, and the rendering
is deliberately literal so that what runs on the ladder is what was measured.
"""
import argparse
import base64
import json
from pathlib import Path
import zlib

BLOCK = 72

# Feature order is part of the artifact's contract: a rule fitted against index k
# must read index k at runtime, so this list is duplicated verbatim into the
# emitted agent rather than imported, and must never be reordered in place.
PRODUCTS = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL',
            'FERTILIZER')
POPULATION = ('WHEAT', 'CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'GOOSE', 'COW', 'SHEEP')
SHOPS = ('BAKERY', 'BRUNCH_SPOT', 'FARMERS_MARKET', 'ICE_CREAM_SHOP', 'PET_CAFE',
         'PIZZA_SHOP', 'SMOOTHIE_SHOP', 'YARN_STORE')


def features(observation):
    """Public state only: shops, market, both farms' money and visible tiles."""
    shops = observation['town']['unlocked_shops']
    vector = [shops.count(shop) for shop in SHOPS]
    vector.append(len(shops))
    vector.extend(observation['market']['prices'].get(item, 0) for item in PRODUCTS)
    vector.extend(observation['market']['inventory'].get(item, 10000) - 10000
                  for item in PRODUCTS)
    seat = int(observation['player'])
    own, rival = observation['farms'][seat], observation['farms'][1 - seat]
    vector.extend((own['money'], rival['money'], own['money'] - rival['money']))
    for farm in (own, rival):
        population = [0] * 8
        for row in farm['tiles']:
            for tile in row:
                if isinstance(tile, dict):
                    item = tile.get('crop') if tile.get('kind') == 'PLANT' else tile.get('animal')
                    if item in POPULATION:
                        population[POPULATION.index(item)] += 1
        vector.extend(population)
    vector.extend((len(own['unlocked_quadrants']), len(rival['unlocked_quadrants'])))
    return vector


FEATURE_NAMES = ([f'shop_{name.lower()}' for name in SHOPS] + ['shops_total']
                 + [f'price_{item.lower()}' for item in PRODUCTS]
                 + [f'inventory_{item.lower()}' for item in PRODUCTS]
                 + ['own_money', 'rival_money', 'money_lead']
                 + [f'own_{item.lower()}' for item in POPULATION]
                 + [f'rival_{item.lower()}' for item in POPULATION]
                 + ['own_quadrants', 'rival_quadrants'])

TEMPLATE = '''"""Routed tape portfolio. {summary}

Routing happens only at 72-turn block boundaries, because that is the schedule on
which this game reveals itself: the town unlocks its first shop on day 3 and one
more every three days, and until then every game looks alike.
"""
import base64
import json
import zlib

TAPES, RULES = json.loads(zlib.decompress(base64.b85decode({blob!r})))
BLOCK = {block}
PRODUCTS = {products!r}
POPULATION = {population!r}
SHOPS = {shops!r}
SESSIONS = {{}}


def features(observation):
    """Public state only: shops, market, both farms' money and visible tiles."""
    shops = observation['town']['unlocked_shops']
    vector = [shops.count(shop) for shop in SHOPS]
    vector.append(len(shops))
    vector.extend(observation['market']['prices'].get(item, 0) for item in PRODUCTS)
    vector.extend(observation['market']['inventory'].get(item, 10000) - 10000
                  for item in PRODUCTS)
    seat = int(observation['player'])
    own, rival = observation['farms'][seat], observation['farms'][1 - seat]
    vector.extend((own['money'], rival['money'], own['money'] - rival['money']))
    for farm in (own, rival):
        population = [0] * 8
        for row in farm['tiles']:
            for tile in row:
                if isinstance(tile, dict):
                    item = tile.get('crop') if tile.get('kind') == 'PLANT' else tile.get('animal')
                    if item in POPULATION:
                        population[POPULATION.index(item)] += 1
        vector.extend(population)
    vector.extend((len(own['unlocked_quadrants']), len(rival['unlocked_quadrants'])))
    return vector


def route(block, observation, current):
    """First matching rule wins; an empty rule list holds the current route."""
    rules = RULES.get(str(block))
    if not rules:
        return current
    vector = None
    for feature, cut, above, below in rules:
        if feature < 0:
            return current if above < 0 else above
        if vector is None:
            vector = features(observation)
        chosen = above if vector[feature] > cut else below
        if chosen >= 0:
            return chosen
    return current


def order(slot):
    """Market slots race by index, so an unparseable slot still consumes one.

    A zero-quantity sale is read as an empty slot by the engine's own parser and
    survives tooling that discards unrecognised orders, so the slot cannot
    silently collapse into a different order's position.
    """
    if isinstance(slot, list) and slot:
        head = slot[0]
        if head in ('HIRE', 'BUY_LAND'):
            return slot[:]
        if head in ('BUY_SEED', 'BUY_PRODUCT', 'BUY_ANIMAL', 'SELL') and len(slot) > 2:
            try:
                if int(slot[2]) > 0:
                    return slot[:]
            except (TypeError, ValueError):
                pass
    return ['SELL', 'WHEAT', 0]


def agent(observation, configuration=None):
    """Kaggle callable; both self-play seats keep independent route commitments."""
    turn = observation.get('step')
    if not isinstance(turn, int):
        turn = int(observation['day']) * 24 + int(observation['hour'])
    if turn < 0 or turn >= len(TAPES[0]):
        return {{'farmer': ['PASS'], 'hands': [], 'market': []}}
    seat = int(observation['player'])
    state = SESSIONS.get(seat)
    if state is None or turn == 0 or turn < state[0]:
        state = [-1, -1, 0]
        SESSIONS[seat] = state
    block = turn // BLOCK
    if state[1] != block:
        state[2] = route(block, observation, state[2])
        state[1] = block
    state[0] = turn
    action = TAPES[state[2]][turn]
    farmer = action.get('farmer')
    return {{
        'farmer': farmer[:] if isinstance(farmer, list) and farmer else ['PASS'],
        'hands': [u[:] if isinstance(u, list) and u else ['PASS'] for u in action.get('hands', [])],
        'market': [order(slot) for slot in action.get('market', [])[:10]],
    }}
'''


def build(tapes, rules, output, summary='no provenance recorded'):
    """Render the portfolio. `rules` maps block index to a decision list.

    A rule is (feature, cut, above, below): take route `above` when the feature
    exceeds `cut` and `below` otherwise, where a negative route means "no opinion,
    try the next rule". A rule with feature < 0 is an unconditional default.
    """
    streams = [tape['actions'] if isinstance(tape, dict) else tape for tape in tapes]
    if not streams:
        raise ValueError('A portfolio needs at least one tape')
    if any(len(stream) != len(streams[0]) for stream in streams):
        raise ValueError('Every tape must cover the same number of turns')
    if len(streams[0]) != 719:
        raise ValueError(f'A tape must cover 719 turns, got {len(streams[0])}')
    for block, decisions in rules.items():
        for rule in decisions:
            if len(rule) != 4:
                raise ValueError(f'Block {block}: a rule is (feature, cut, above, below)')
            if max(rule[2], rule[3]) >= len(streams):
                raise ValueError(f'Block {block}: rule routes outside the portfolio')
    blob = base64.b85encode(zlib.compress(json.dumps(
        [streams, {str(k): v for k, v in rules.items()}], separators=(',', ':')).encode(), 9)).decode()
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(TEMPLATE.format(blob=blob, summary=summary, block=BLOCK,
                                    products=PRODUCTS, population=POPULATION, shops=SHOPS),
                    encoding='utf-8')
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', required=True)
    parser.add_argument('--tapes', required=True, help='comma-separated tape id prefixes, in route order')
    parser.add_argument('--rules', default='{}', help='JSON object mapping block index to rules')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    library = json.loads(Path(args.library).read_text())
    wanted = args.tapes.split(',')
    index = {tape['sha256']: tape for tape in library['tapes']}
    chosen = []
    for prefix in wanted:
        matched = [tape for sha, tape in index.items() if sha.startswith(prefix)]
        if len(matched) != 1:
            raise ValueError(f'{prefix} matched {len(matched)} tapes')
        chosen.append(matched[0])
    rules = {int(k): v for k, v in json.loads(args.rules).items()}
    summary = ' | '.join(f"{t['sha256'][:12]} {t.get('team')} {t.get('money')}" for t in chosen)
    build(chosen, rules, args.output, summary)
    print(json.dumps({'tapes': [t['sha256'][:12] for t in chosen], 'rules': rules,
                      'output': args.output}, indent=2))


if __name__ == '__main__':
    main()
