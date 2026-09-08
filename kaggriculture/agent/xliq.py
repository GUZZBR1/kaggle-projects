"""Issue #25: an opening-only liquidity treatment around a frozen base agent."""
import copy

from .economy import ANIMALS, CROPS, price


DEFAULTS = {
    'opening_days': 3,
    'capital_floor': 1000,
    'short_crop': 'WHEAT',
    'premium_crop': 'STRAWBERRY',
    'short_seed_target': 6,
    'premium_seed_target': 2,
}


def _stock(observation, crop):
    private = observation['private']
    return private['seeds'].get(crop, 0) + private['shed'].get(crop, 0) + sum(
        inventory.get(crop, 0) for inventory in private['inventories'])


def _opening_plant_mix(action, observation, params):
    short, premium = params['short_crop'], params['premium_crop']
    remaining = {short: observation['private']['seeds'].get(short, 0),
                 premium: observation['private']['seeds'].get(premium, 0)}
    # Existing public tiles are the entire memory: no hidden state or cross-game leakage.
    planted = {short: 0, premium: 0}
    own = observation['farms'][observation['player']]
    for row in own['tiles']:
        for tile in row:
            if isinstance(tile, dict) and tile.get('crop') in planted:
                planted[tile['crop']] += 1
    unit_keys = [('farmer', None), *[('hands', i) for i in range(len(action['hands']))]]
    for key, index in unit_keys:
        original = action[key] if index is None else action[key][index]
        if not (isinstance(original, list) and len(original) >= 2 and original[0] == 'PLANT'):
            continue
        # Establish fast cashflow first, then reserve one in four opening tiles
        # for long-cycle premium growth.
        wants_premium = planted[premium] * 3 < planted[short] and remaining[premium] > 0
        crop = premium if wants_premium else short
        if remaining[crop] <= 0:
            crop = premium if crop == short else short
        if remaining[crop] <= 0:
            continue
        replacement = ['PLANT', crop]
        if index is None:
            action[key] = replacement
        else:
            action[key][index] = replacement
        remaining[crop] -= 1
        planted[crop] += 1


def _fib(index):
    a, b = 1, 1
    for _ in range(index):
        a, b = b, a + b
    return a


def _opening_budget(action, observation, configuration, params):
    """Retain base orders only while the public cash forecast respects the floor."""
    me = observation['farms'][observation['player']]
    available = max(0., float(me['money']) - params['capital_floor'])
    hires = me.get('hires_today', 0)
    quadrants = len(me.get('unlocked_quadrants', [0]))
    inventory = dict(observation.get('market', {}).get('inventory', {}))
    kept = []
    removed_seed_positions = []
    for index, order in enumerate(action['market']):
        if not isinstance(order, list) or not order:
            kept.append(order)
            continue
        op = order[0]
        if op == 'BUY_SEED':
            removed_seed_positions.append(index)
            continue
        cost = 0.
        if op == 'HIRE':
            cost = _fib(hires) * configuration.get('farmHandCostMult', 1)
        elif op == 'BUY_LAND' and 1 <= quadrants <= 3:
            cost = (1000, 2000, 4000)[quadrants - 1]
        elif op == 'BUY_ANIMAL' and len(order) >= 3 and order[1] in ANIMALS:
            cost = ANIMALS[order[1]][0] * max(0, int(order[2]))
        elif op == 'BUY_PRODUCT' and len(order) >= 3 and order[1] in ('WHEAT', 'FERTILIZER'):
            item, count = order[1], max(0, int(order[2]))
            current = inventory.get(item, 10000)
            cost = sum(price(item, current - offset - 1,
                             configuration.get('marketParams')) for offset in range(count))
        if cost > available:
            # This is the declared initial operating-capital surface. It does
            # not replace or re-order the base strategy; an unaffordable early
            # purchase is simply deferred by omission.
            continue
        kept.append(order)
        available -= cost
        if op == 'HIRE':
            hires += 1
        elif op == 'BUY_LAND':
            quadrants += 1
        elif op == 'BUY_PRODUCT' and len(order) >= 3:
            inventory[order[1]] = inventory.get(order[1], 10000) - max(0, int(order[2]))
    return kept, available, removed_seed_positions


def _opening_seed_orders(action, observation, configuration, params):
    short, premium = params['short_crop'], params['premium_crop']
    targets = {short: params['short_seed_target'], premium: params['premium_seed_target']}
    needed = {crop: max(0, target - _stock(observation, crop))
              for crop, target in targets.items()}
    orders, budget, removed_positions = _opening_budget(
        action, observation, configuration, params)
    additions = []
    for crop in (short, premium):
        count = min(needed[crop], int(budget // CROPS[crop][0]))
        if count:
            additions.append(['BUY_SEED', crop, count])
            budget -= count * CROPS[crop][0]
    limit = configuration.get('maxMarketOrdersPerTurn', 10)
    room = max(0, limit - len(orders))
    additions = additions[:room]
    insertion = min(removed_positions, default=len(orders))
    action['market'] = orders[:insertion] + additions + orders[insertion:]


def opening_treatment(base_action, observation, configuration=None, parameters=None):
    """Change only early planting/seed capital; return later actions byte-for-byte."""
    params = {**DEFAULTS, **(parameters or {})}
    day = observation.get('day')
    if type(day) is not int or day < 0:
        raise ValueError('X-LIQ requires the canonical public day clock')
    if day >= params['opening_days']:
        return base_action
    action = copy.deepcopy(base_action)
    if not isinstance(action, dict) or set(action) != {'farmer', 'hands', 'market'}:
        raise ValueError('Frozen base returned a malformed action')
    _opening_plant_mix(action, observation, params)
    _opening_seed_orders(action, observation, configuration or {}, params)
    return action


def wrap_agent(base_agent, parameters=None):
    def xliq_agent(observation, configuration=None):
        base_action = base_agent(observation, configuration)
        return opening_treatment(base_action, observation, configuration, parameters)
    return xliq_agent
