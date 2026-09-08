"""Swap a whole block for the same block of another tape in the same library.

This is the step the routing evidence points at. Editing actions inside a block is
exhausted on these tapes -- `docs/OPPORTUNITY_SEARCH.md` enumerated the whole admissible
work space of three blocks and moved nothing -- while `docs/SPLICE_DISTANCE.md` measured
that joins *across* provenances collapse. What has never been measured in win terms is the
join within one provenance: the same author's tapes, which were produced by one solver and
therefore share an economy, differing only in the block being swapped.

A donor block is a proposal exactly as a mutation is: the incumbent's prefix and suffix stay
byte for byte, only `[start, end)` comes from the donor, and the frontier check in
`block_solver.evaluate` refuses the evaluation unless the state entering the block is
identical to the incumbent's. So a donor that wins, wins from the same starting position.

Nothing here decides that a donor block is compatible. It decides only that it is
*different*, which is what makes it worth a game; the engine decides the rest.
"""
import copy

from experiments.tape_harvest import tape_digest

TURNS = 719


def swap_mutations(actions, start, end, count, rng, excluded=(), donors=()):
    if len(actions) != TURNS or not 0 <= start < end <= TURNS or count < 1:
        raise ValueError('Require a complete tape, bounded block and positive proposal count')
    proposals = []
    for index, donor in enumerate(donors):
        if len(donor) != TURNS:
            raise ValueError('Every donor must be a complete tape of the same length')
        if donor[start:end] == actions[start:end]:
            continue
        tape = copy.deepcopy(actions)
        tape[start:end] = copy.deepcopy(donor[start:end])
        turns = sum(1 for turn in range(start, end) if actions[turn] != donor[turn])
        proposals.append((index, tape, turns))
    # Most different first: a donor block that differs in two turns is a tie-break, not a
    # hypothesis, and the budget should reach the real alternatives before the near-copies.
    proposals.sort(key=lambda item: -item[2])
    seen, result = set(excluded) | {tape_digest(actions)}, []
    for index, tape, turns in proposals:
        identity = tape_digest(tape)
        if identity in seen:
            continue
        seen.add(identity)
        result.append(dict(actions=tape, sha256=identity,
                           mutation=dict(kind='block_swap', donor=index, turns_changed=turns)))
        if len(result) == count:
            break
    return result
