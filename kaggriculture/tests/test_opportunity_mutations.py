"""State-aware work must propose only what the observed tile admits, in every context.

The blind generator's failure is the thing being fixed: filling idle slots with a command
whose precondition does not hold produces ineffective actions, not wins. These tests hold
the generator to the engine's own preconditions, which are quoted in the module docstring.
"""
import random

import pytest

from experiments.opportunity_mutations import (WORK, admissible, opportunities,
                                               opportunity_mutations)


def tape(idle_turns=(), hands=1):
    actions = []
    for turn in range(719):
        action = dict(farmer=['PASS'] if turn in idle_turns else ['NORTH'],
                      hands=[['PASS'] if turn in idle_turns else ['EAST']] * hands, market=[])
        actions.append(action)
    return actions


def observation(tiles, *, day=3, seat=0, hands=((1, 0),), inventories=({}, {})):
    board = [[None] * 4 for _ in range(4)]
    for (x, y), tile in tiles.items():
        board[y][x] = tile
    return {'player': seat, 'day': day, 'step': 72,
            'farms': [{'farmer': [0, 0], 'hands': [list(spot) for spot in hands],
                       'tiles': board, 'money': 0}],
            'private': {'inventories': [dict(item) for item in inventories]}}


PLANT = {'kind': 'PLANT', 'crop': 'WHEAT', 'planted_day': 0, 'watered_today': False,
         'yield_units': 3, 'fertilized_until_day': -1}
ANIMAL = {'kind': 'COOP', 'animal': 'GOOSE', 'yield_units': 2, 'fed_today': False,
          'cared_today': False, 'fertilizer_available': True}


def test_a_locked_or_empty_tile_admits_nothing():
    """A locked tile arrives as the string `LOCKED` and every tile action no-ops on it."""
    assert admissible(None, observation({}), 3, 0) == []


def test_plant_preconditions_follow_the_engine():
    watered = dict(PLANT, watered_today=True)
    assert 'WATER' in admissible(PLANT, observation({}), 3, 0)
    assert 'WATER' not in admissible(watered, observation({}), 3, 0)
    # HARVEST returns nothing before first_yield_day, whatever yield_units says.
    young = dict(PLANT, planted_day=3)
    assert 'HARVEST' not in admissible(young, observation({}), 3, 0)
    assert 'HARVEST' in admissible(PLANT, observation({}), 3, 0)
    # FERTILIZE consumes from the unit's own inventory, not the shed.
    assert 'FERTILIZE' not in admissible(PLANT, observation({}), 3, 0)
    carrying = observation({}, inventories=({'FERTILIZER': 1}, {}))
    assert 'FERTILIZE' in admissible(PLANT, carrying, 3, 0)


def test_animal_preconditions_follow_the_engine():
    found = admissible(ANIMAL, observation({}), 3, 0)
    assert set(found) == {'HARVEST', 'CARE', 'COLLECT_FERTILIZER'}
    # FEED costs one WHEAT from the acting unit.
    fed = admissible(ANIMAL, observation({}, inventories=({'WHEAT': 1}, {})), 3, 0)
    assert 'FEED' in fed
    quiet = dict(ANIMAL, fed_today=True, cared_today=True, fertilizer_available=False,
                 yield_units=0)
    assert admissible(quiet, observation({}, inventories=({'WHEAT': 1}, {})), 3, 0) == []
    # An empty structure is not an animal, even though the engine's `"animal" in tile`
    # would accept it and burn the wheat.
    assert admissible(dict(ANIMAL, animal=None), observation({}), 3, 0) == []


def test_only_slots_the_tape_leaves_idle_are_proposed():
    actions = tape(idle_turns=(72,))
    observations = {turn: observation({(0, 0): PLANT, (1, 0): ANIMAL}) for turn in range(72, 76)}
    found = opportunities(actions, [observations], 72, 76)
    assert {turn for turn, *_ in found} == {72}
    assert {role for _, role, _, _ in found} == {'farmer', 'hands'}


def test_same_tile_and_day_collapses_to_the_earliest_turn():
    """A second WATER on the same tile and day is a no-op by the rule that admitted it."""
    actions = tape(idle_turns=(72, 73, 74))
    observations = {turn: observation({(0, 0): PLANT}) for turn in range(72, 76)}
    watering = [item for item in opportunities(actions, [observations], 72, 76)
                if item[3] == 'WATER' and item[1] == 'farmer']
    assert watering == [(72, 'farmer', None, 'WATER')]


def test_an_opportunity_absent_from_one_context_is_not_proposed():
    """A trajectory belongs to one context; only what every probe admits is worth games."""
    actions = tape(idle_turns=(72,))
    here = {72: observation({(0, 0): PLANT})}
    there = {72: observation({(0, 0): dict(PLANT, watered_today=True, yield_units=0)})}
    assert opportunities(actions, [here], 72, 76)
    assert opportunities(actions, [here, there], 72, 76) == []


def test_proposals_change_only_idle_slots_inside_the_block():
    actions = tape(idle_turns=(72, 100))
    observations = {turn: observation({(0, 0): PLANT, (1, 0): ANIMAL}) for turn in range(72, 144)}
    variants = opportunity_mutations(actions, 72, 144, 6, random.Random(3),
                                     observation_sets=[observations])
    assert variants
    for variant in variants:
        assert variant['actions'][:72] == actions[:72]
        assert variant['actions'][144:] == actions[144:]
        for turn in range(72, 144):
            for key in ('farmer', 'hands'):
                before, after = actions[turn][key], variant['actions'][turn][key]
                if before != after:
                    assert turn in (72, 100)
                    changed = [after] if key == 'farmer' else after
                    assert all(order[0] in WORK for order in changed if order != ['PASS'])


def test_no_observed_opportunity_yields_no_proposal():
    """Without a probe there is nothing admissible, and nothing may be fabricated."""
    actions = tape(idle_turns=(72,))
    assert opportunity_mutations(actions, 72, 144, 4, random.Random(1)) == []


@pytest.mark.parametrize('bad', [dict(start=-1, end=72), dict(start=72, end=72),
                                 dict(start=0, end=720)])
def test_a_bounded_block_is_required(bad):
    with pytest.raises(ValueError):
        opportunity_mutations(tape(), count=1, rng=random.Random(1), **bad)
