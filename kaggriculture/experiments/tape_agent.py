"""Emit a standalone submission that replays one harvested tape.

The field's strongest artifact carries five tapes and switches between them at
two of its ten blocks. Our harvest showed it emits only three distinct action
streams across two dozen varied games, so its routing is doing very little. That
raises a testable question this module exists to answer: is the routing worth
anything at all, or does the single best tape beat the agent that carries it?

A tape agent is deliberately the simplest possible baseline. It observes only
the canonical clock, ignores everything else, and cannot adapt. Anything that
beats it has to earn the difference.
"""
import argparse
import base64
import json
import zlib
from pathlib import Path

TEMPLATE = '''"""Replays one recorded action tape. Provenance: {provenance}."""
import base64
import json
import zlib

TAPE = json.loads(zlib.decompress(base64.b85decode({blob!r})))


def _order(slot):
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
    turn = observation.get('step')
    if not isinstance(turn, int):
        turn = int(observation['day']) * 24 + int(observation['hour'])
    if turn < 0 or turn >= len(TAPE):
        return {{'farmer': ['PASS'], 'hands': [], 'market': []}}
    action = TAPE[turn]
    farmer = action.get('farmer')
    return {{
        'farmer': farmer[:] if isinstance(farmer, list) and farmer else ['PASS'],
        'hands': [u[:] if isinstance(u, list) and u else ['PASS'] for u in action.get('hands', [])],
        'market': [_order(slot) for slot in action.get('market', [])[:10]],
    }}
'''


def build(tape, output, provenance='unknown'):
    actions = tape['actions'] if isinstance(tape, dict) else tape
    if len(actions) != 719:
        raise ValueError(f'A tape must cover 719 turns, got {len(actions)}')
    blob = base64.b85encode(zlib.compress(
        json.dumps(actions, separators=(',', ':')).encode(), 9)).decode()
    source = TEMPLATE.format(blob=blob, provenance=provenance)
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding='utf-8')
    return path


def select(library, rank=0):
    """Tapes arrive ranked by the margin they actually produced."""
    tapes = library['tapes']
    if not tapes:
        raise ValueError('The library is empty; nothing to replay')
    if not 0 <= rank < len(tapes):
        raise ValueError(f'rank {rank} outside a library of {len(tapes)} tapes')
    return tapes[rank]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', required=True)
    parser.add_argument('--rank', type=int, default=0)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    library = json.loads(Path(args.library).read_text())
    tape = select(library, args.rank)
    provenance = f"{tape['id']} from {Path(tape['donor']).name} vs {Path(tape['opponent']).name} " \
                 f"seed {tape['seed']} seat {tape['seat']} margin {tape['margin']:.0f}"
    build(tape, args.output, provenance)
    print(json.dumps({'tape': tape['id'], 'margin': tape['margin'], 'donor': tape['donor'],
                      'output': args.output}, indent=2))


if __name__ == '__main__':
    main()
