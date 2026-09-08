"""A donor block is a proposal like any other: same frontier, same prefix, same suffix.

The point of the swap space is that the alternative comes from the same author's library,
so the join is inside one provenance. These tests hold the generator to the two properties
that make such a proposal measurable at all -- locality and difference -- and to the budget
order that decides which donor is worth a game first.
"""
import random

import pytest

from experiments.swap_mutations import swap_mutations


def tape(mark='A', block=(144, 288)):
    actions = [dict(farmer=['PASS'], hands=[], market=[]) for _ in range(719)]
    for turn in range(*block):
        actions[turn]['farmer'] = [mark]
    return actions


def test_an_identical_block_is_not_a_proposal():
    """A donor that agrees on the block is a duplicate, not an alternative."""
    base = tape()
    assert swap_mutations(base, 144, 288, 3, random.Random(1), donors=[tape()]) == []


def test_only_the_block_comes_from_the_donor():
    base, donor = tape(), tape('B')
    variant, = swap_mutations(base, 144, 288, 3, random.Random(1), donors=[donor])
    actions = variant['actions']
    assert actions[:144] == base[:144]
    assert actions[288:] == base[288:]
    assert actions[144:288] == donor[144:288]
    assert base == tape(), 'the incumbent must not be mutated in place'


def test_the_most_different_donor_is_proposed_first():
    """A donor differing in two turns is a tie-break; the budget must reach the real ones."""
    base = tape()
    near = tape()
    near[200]['farmer'] = ['B']
    far = tape('B')
    variants = swap_mutations(base, 144, 288, 2, random.Random(1), donors=[near, far])
    assert [variant['mutation']['donor'] for variant in variants] == [1, 0]
    assert variants[0]['mutation']['turns_changed'] == 144
    assert variants[1]['mutation']['turns_changed'] == 1


def test_the_budget_is_respected_and_duplicates_are_skipped():
    base = tape()
    variants = swap_mutations(base, 144, 288, 1, random.Random(1),
                              donors=[tape('B'), tape('C')])
    assert len(variants) == 1
    already = {variants[0]['sha256']}
    assert swap_mutations(base, 144, 288, 1, random.Random(1), excluded=already,
                          donors=[tape('B')]) == []


def test_a_donor_of_the_wrong_length_is_refused():
    with pytest.raises(ValueError, match='complete tape'):
        swap_mutations(tape(), 144, 288, 1, random.Random(1), donors=[tape()[:700]])


def test_no_donor_yields_no_proposal():
    assert swap_mutations(tape(), 144, 288, 3, random.Random(1)) == []
