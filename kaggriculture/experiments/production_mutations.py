"""Bounded unit-work edits for tape search; measured legality/profit belongs to the engine.

No worker identities, movement commands, purchases, prefix or suffix are changed.
An idle substitution can be ineffective when the unit lacks a target or resource;
that is a measured outcome, never an assumed improvement.
"""
import copy
from experiments.tape_harvest import tape_digest

WORK = ('WATER', 'HARVEST', 'CARE', 'FEED', 'COLLECT_FERTILIZER', 'FERTILIZE')


def units(action):
    if isinstance(action.get('farmer'), list):
        yield 'farmer', None, action['farmer']
    for index, order in enumerate(action.get('hands', [])):
        if isinstance(order, list):
            yield 'hands', index, order


def command(action, role, index):
    return action[role] if index is None else action[role][index]


def assign(action, role, index, value):
    if index is None:
        action[role] = value
    else:
        action[role][index] = value


def production_mutations(actions, start, end, count, rng, excluded=()):
    if len(actions) != 719 or not 0 <= start < end <= 719 or count < 1:
        raise ValueError('Require a complete tape, bounded block and positive proposal count')
    descriptors = []
    idle = [(turn, role, index) for turn in range(start, end)
            for role, index, order in units(actions[turn]) if order == ['PASS']]
    # One coherent hypothesis per work type, covering idle slots throughout the block.
    for work in WORK:
        if idle:
            descriptors.append(dict(kind='idle_work', work=work, targets=idle))
    local = []
    for turn in range(start, end - 1):
        following = {(role, index): order for role, index, order in units(actions[turn + 1])}
        for role, index, order in units(actions[turn]):
            other = following.get((role, index))
            if not other or not order or order == other:
                continue
            # Only swap stationary work and idle: moving a command across a route
            # would change its target tile, rather than merely change its timing.
            if order[0] in (*WORK, 'PLANT', 'PASS') and other[0] in (*WORK, 'PLANT', 'PASS'):
                local.append(dict(kind='swap_work', turn=turn, role=role, index=index))
    rng.shuffle(local)
    descriptors.extend(local)
    seen = set(excluded) | {tape_digest(actions)}
    result = []
    for descriptor in descriptors:
        tape = copy.deepcopy(actions)
        if descriptor['kind'] == 'idle_work':
            for turn, role, index in descriptor['targets']:
                assign(tape[turn], role, index, [descriptor['work']])
        else:
            turn, role, index = (descriptor[key] for key in ('turn', 'role', 'index'))
            a, b = command(tape[turn], role, index), command(tape[turn + 1], role, index)
            assign(tape[turn], role, index, b)
            assign(tape[turn + 1], role, index, a)
        identity = tape_digest(tape)
        if identity in seen:
            continue
        seen.add(identity)
        result.append(dict(actions=tape, sha256=identity, mutation=descriptor))
        if len(result) == count:
            break
    return result
