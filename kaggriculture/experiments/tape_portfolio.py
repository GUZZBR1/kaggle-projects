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
LEAD_SALE = {lead_sale!r}
LEAD_SKIP = ('WHEAT', 'FERTILIZER')
MIN_SELL_PRICE = 2
MAX_ORDERS = 10
LAST_ACT_STEP = 718
SHED_CAPACITY = 100
ANIMALS = ('GOOSE', 'COW', 'SHEEP')
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


def near_shed(position, board):
    """The shed occupies the four centre tiles; only a unit standing on one deposits."""
    if not isinstance(position, (list, tuple)) or len(position) < 2:
        return False
    half = board // 2
    return position[0] in (half - 1, half) and position[1] in (half - 1, half)


def holdings_after(observation, market, action):
    """What the shed will hold when the market runs, not what it holds right now.

    Unit actions resolve before the market does, so a hand standing at the shed
    with a DROP this turn has already deposited its load by the time an order is
    matched. Counting only the current shed is what makes a lead sale look
    impossible: the tape carries goods in on turn T and sells them on T+1, so at
    T the shed is still empty and every candidate is rejected for lack of stock.
    """
    shed = {{}}
    for item, count in (observation['private']['shed'] or {{}}).items():
        try:
            shed[item] = max(0, int(count))
        except (TypeError, ValueError):
            pass
    total = sum(shed.values())
    farm = observation['farms'][int(observation['player'])]
    board = len(farm['tiles']) or 10
    positions = [farm['farmer']] + [list(p) for p in (farm['hands'] or [])]
    inventories = observation['private']['inventories'] or []
    units = [action.get('farmer') or ['PASS']] + list(action.get('hands') or [])
    for index in range(min(len(units), len(positions))):
        if not near_shed(positions[index], board):
            continue
        unit = units[index] or ['PASS']
        operation = unit[0] if unit else 'PASS'
        carried = inventories[index] if index < len(inventories) else {{}}
        if operation == 'PICKUP' and len(unit) >= 2 and unit[1] in shed:
            taken = min(shed[unit[1]], max(0, int(unit[2]) if len(unit) >= 3 else 1))
            shed[unit[1]] -= taken
            total -= taken
        elif operation == 'DROP':
            for item, held in (carried or {{}}).items():
                room = min(max(0, int(held)), max(0, SHED_CAPACITY - total))
                if room > 0:
                    shed[item] = shed.get(item, 0) + room
                    total += room
        elif operation == 'PLACE' and len(unit) >= 2 and unit[1] not in ANIMALS:
            item = unit[1]
            room = min(max(0, int(unit[2]) if len(unit) >= 3 else 1),
                       max(0, int((carried or {{}}).get(item, 0))),
                       max(0, SHED_CAPACITY - total))
            if room > 0:
                shed[item] = shed.get(item, 0) + room
                total += room
    for slot in market:
        if isinstance(slot, list) and len(slot) > 2 and slot[0] == 'SELL':
            try:
                shed[slot[1]] = shed.get(slot[1], 0) - int(slot[2])
            except (TypeError, ValueError):
                pass
    return shed


def lead_sale(market, observation, tape, turn, pending):
    """Sell next turn's planned lots now, and suppress them next turn.

    A product's price falls as the market's inventory of it rises, and the field
    has converged on similar production, so the seat that sells first takes the
    better price. Moving a sale one turn earlier is only free when the town does
    not consume between the two turns and the shop set does not change, which is
    what the guards below check. Mechanism from yhay81's fieldbook `_lead_sale`,
    as carried by the public v23 chassis; this is our own implementation of it.

    `pending` accumulates what to remove from next turn's orders, so the same
    lot is never sold twice.
    """
    nxt = turn + 1
    if nxt > LAST_ACT_STEP or nxt % (3 * 24) == 0 or turn % 4 == 0:
        return
    future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {{}}
    planned = {{}}
    for slot in future.get('market') or []:
        if isinstance(slot, list) and len(slot) > 2 and slot[0] == 'SELL':
            try:
                planned[slot[1]] = planned.get(slot[1], 0) + max(0, int(slot[2]))
            except (TypeError, ValueError):
                pass
    queued = {{slot[1] for slot in market
              if isinstance(slot, list) and len(slot) > 1 and slot[0] == 'SELL'}}
    held = holdings_after(observation, market, tape[turn])
    prices = observation['market']['prices']
    for item in PRODUCTS:
        if item in LEAD_SKIP or item in queued or planned.get(item, 0) <= 0:
            continue
        quantity = min(held.get(item, 0), planned[item])
        if quantity <= 0 or prices.get(item, 0) < MIN_SELL_PRICE:
            continue
        if len(market) >= MAX_ORDERS:
            break
        market.append(['SELL', item, quantity])
        pending[item] = pending.get(item, 0) + quantity


def suppress(market, pending):
    """Zero out lots already sold a turn early, keeping every slot in place.

    The engine races market orders by slot index, so a sold-out order must
    become a zero-quantity sale rather than disappear and shift the rest.
    """
    for slot in market:
        if not (isinstance(slot, list) and len(slot) > 2 and slot[0] == 'SELL'):
            continue
        owed = pending.get(slot[1], 0)
        if owed <= 0:
            continue
        try:
            quantity = int(slot[2])
        except (TypeError, ValueError):
            continue
        removed = min(max(0, quantity), owed)
        slot[2] = quantity - removed
        pending[slot[1]] = owed - removed
    pending.clear()


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
        state = [-1, -1, 0, {{}}]
        SESSIONS[seat] = state
    block = turn // BLOCK
    if state[1] != block:
        state[2] = route(block, observation, state[2])
        state[1] = block
    state[0] = turn
    tape = TAPES[state[2]]
    action = tape[turn]
    farmer = action.get('farmer')
    market = [order(slot) for slot in action.get('market', [])[:MAX_ORDERS]]
    if LEAD_SALE:
        try:
            suppress(market, state[3])
            lead_sale(market, observation, tape, turn, state[3])
        except Exception:
            # The tape alone is always playable; a failing edge never costs a turn.
            state[3].clear()
    return {{
        'farmer': farmer[:] if isinstance(farmer, list) and farmer else ['PASS'],
        'hands': [u[:] if isinstance(u, list) and u else ['PASS'] for u in action.get('hands', [])],
        'market': market,
    }}
'''


def build(tapes, rules, output, summary='no provenance recorded', lead_sale=True):
    """Render the portfolio. `rules` maps block index to a decision list.

    A rule is (feature, cut, above, below): take route `above` when the feature
    exceeds `cut` and `below` otherwise, where a negative route means "no opinion,
    try the next rule". A rule with feature < 0 is an unconditional default.

    `lead_sale` moves each planned sale one turn earlier where that is free.
    Measured value on our own tapes is zero: they already sell the moment the
    carrier reaches the shed, so there is no slack to take. Its one demonstrated
    effect is winning an exact mirror tie by a single coin, which is worth
    something on a ladder where many entries run the same public notebook. See
    docs/SELL_LEAD_CORRECTION.md before crediting it with more than that.
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
                                    products=PRODUCTS, population=POPULATION, shops=SHOPS,
                                    lead_sale=bool(lead_sale)),
                    encoding='utf-8')
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', required=True)
    parser.add_argument('--tapes', required=True, help='comma-separated tape id prefixes, in route order')
    parser.add_argument('--rules', default='{}', help='JSON object mapping block index to rules')
    parser.add_argument('--output', required=True)
    parser.add_argument('--no-lead-sale', dest='lead_sale', action='store_false',
                        help='build without the lead-sale edge, for paired comparison')
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
    build(chosen, rules, args.output, summary, lead_sale=args.lead_sale)
    print(json.dumps({'tapes': [t['sha256'][:12] for t in chosen], 'rules': rules,
                      'output': args.output}, indent=2))


if __name__ == '__main__':
    main()
