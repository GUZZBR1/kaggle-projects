"""Render a submission that plays our tape library through the v23 reactive chassis.

Two levers have been measured separately on this bench and never together.
`docs/YHAY_ROUTER_FINDING.md` shows that tape quality is the largest one: the four
tapes `yhay81/shop-router-0908` carries reach 0,750 worst family with no reactive
repair at all, where our harvested tapes reach 0,325. `docs/CHASSIS_FINDING.md`
shows the second: with *identical* tapes, wrapping them in per-turn repair layers
is worth +0,225 worst family, because a recorded plan replayed into a town with a
different shop mix is wrong in small, fixable ways rather than wrong in spirit.

This module is the combination. The chassis comes verbatim from the pinned
`aberatozer_v23` bundle, which is Apache-2.0 and says so in its own header; we take
everything up to the point where it installs its own tapes and router, and install
ours instead. Nothing in the chassis is edited, so what runs here is the same code
that was measured as part of that artifact, and the licence header and credit lines
travel with every artifact we emit.

The router is rendered literally rather than interpreted, for the same reason the
tape portfolio is: what runs on the ladder should be what was measured.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import zlib

ROOT = Path(__file__).resolve().parents[1]
CHASSIS = ROOT / 'opponents' / 'public' / 'aberatozer_v23' / 'main.py'
CHASSIS_MANIFEST = CHASSIS.parent / 'main.manifest.json'

# The upstream file is license header, chassis, `make_agent`, and then its own
# payload. This is the first line of that payload; everything above it is the part
# we reuse, and the marker is asserted rather than searched loosely so that a
# re-pinned bundle with a different shape fails the build instead of silently
# truncating the chassis.
PAYLOAD_MARKER = '# Donor stream: thomastschinkel (Apache-2.0); runtime ideas: yhay81;'

# Layer defaults follow the pinned artifact, including `front_run` off: it needs an
# `opponent_plan` the chassis is not given here, and with none it is inert anyway.
SETTINGS = {
    'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'front_run': False,
    'budget_guard': True, 'room_guard': True, 'clamp_sells': True, 'dead_stock': True,
    'terminal_liquidation': True,
}

FOOTER = '''

# --------------------------------------------------------------------------- portfolio
# Tapes: {provenance}
# The chassis above is unmodified upstream code; everything below is this project's.
import base64 as _b64
import json as _json
import zlib as _zlib

_TAPES = _json.loads(_zlib.decompress(_b64.b85decode({blob!r})))
_ROUTES = {{index: tape for index, tape in enumerate(_TAPES)}}
_STAGES = {stages!r}
_SETTINGS = {settings!r}


def _shop_count(observation, name):
    shops = _get(_get(observation, 'town', {{}}) or {{}}, 'unlocked_shops', []) or []
    return list(shops).count(name)


def _market_inventory(observation, item):
    market = _get(observation, 'market', {{}}) or {{}}
    return _int(_get(_get(market, 'inventory', {{}}) or {{}}, item, 10000), 10000)


_READERS = {{'shop_count': _shop_count, 'market_inventory': _market_inventory}}


def _router(observation, step, state):
    """One latched decision per stage; anything unreadable holds the current route.

    Each stage fires on the first step at or after its own step and never again, so
    a stage decides on the state of the world at the moment it was fitted for and a
    later swing in the same feature cannot flip a plan mid-flight.

    `when` names the routes a stage may fire from. A stage whose alternatives are
    variants of one season plan must not fire while a different season plan is
    running, because the tapes it chooses between were never written to follow the
    state that plan produces. The latch is still set either way, so a skipped stage
    does not fire later from a route it was not meant to leave.
    """
    for index, stage in enumerate(_STAGES):
        at, kind, subject, threshold, above, below, when = stage
        key = 'stage_%d' % index
        if step < at or state.get(key):
            continue
        state[key] = True
        if when and state.get('route', {default}) not in when:
            continue
        try:
            value = _READERS[kind](observation, subject)
        except Exception:
            continue
        state['route'] = above if value > threshold else below
    return state.get('route', {default})


_IMPL = make_agent(_ROUTES, router=_router, **_SETTINGS)


def agent(observation, configuration=None):
    # Keep the entry point last: Kaggle selects the last module-level callable.
    try:
        return _IMPL(observation, configuration)
    except Exception:
        return {{'farmer': ['PASS'], 'hands': [], 'market': []}}
'''


def prelude():
    """The pinned chassis, verified against its manifest and cut at its own payload."""
    manifest = json.loads(CHASSIS_MANIFEST.read_text(encoding='utf-8'))
    text = CHASSIS.read_text(encoding='utf-8')
    digest = hashlib.sha256(text.replace('\r\n', '\n').encode()).hexdigest()
    if digest != manifest['sha256']:
        raise ValueError(f"chassis bundle digest {digest} does not match its manifest")
    lines = text.split('\n')
    marks = [i for i, line in enumerate(lines) if line.startswith(PAYLOAD_MARKER)]
    if len(marks) != 1:
        raise ValueError(f'expected exactly one payload marker, found {len(marks)}')
    return '\n'.join(lines[:marks[0]]).rstrip('\n')


def build(tapes, stages, output, provenance='no provenance recorded', default=0,
          settings=None):
    """Render chassis + tapes + router into one standalone `main.py`.

    `stages` is a list of (step, feature kind, subject, threshold, above, below)
    with an optional seventh field: at `step`, take route `above` when the feature
    exceeds `threshold` and `below` otherwise. That is the same shape the upstream
    routers use, and it is the shape a fitted decision stump takes. The seventh
    field, `when`, restricts the stage to firing from a listed set of routes; it
    defaults to firing from any route.
    """
    streams = [tape['actions'] if isinstance(tape, dict) else tape for tape in tapes]
    if not streams:
        raise ValueError('A portfolio needs at least one tape')
    if any(len(stream) != 719 for stream in streams):
        raise ValueError('Every tape must cover 719 turns')
    if not 0 <= default < len(streams):
        raise ValueError('The default route is outside the portfolio')
    normalized = []
    for stage in stages:
        if len(stage) not in (6, 7):
            raise ValueError('A stage is (step, kind, subject, threshold, above, below[, when])')
        at, kind, subject, threshold, above, below = stage[:6]
        when = tuple(stage[6]) if len(stage) == 7 else ()
        if any(route not in range(len(streams)) for route in when):
            raise ValueError(f'Stage at {at} guards on a route outside the portfolio')
        normalized.append((at, kind, subject, threshold, above, below, when))
        if kind not in ('shop_count', 'market_inventory'):
            raise ValueError(f'Unknown routing feature {kind!r}')
        if not 0 <= at < 719:
            raise ValueError(f'Routing step {at} is outside the episode')
        if max(above, below) >= len(streams) or min(above, below) < 0:
            raise ValueError(f'Stage at {at} routes outside the portfolio')
    blob = base64.b85encode(zlib.compress(
        json.dumps(streams, separators=(',', ':')).encode(), 9)).decode()
    source = prelude() + FOOTER.format(
        blob=blob, stages=normalized,
        settings=dict(SETTINGS, **(settings or {})), provenance=provenance, default=default)
    compile(source, str(output), 'exec')
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding='utf-8')
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tapes', required=True, help='JSON file holding a list of 719-action tapes')
    parser.add_argument('--stages', default='[]', help='JSON list of routing stages')
    parser.add_argument('--settings', default='{}', help='JSON object of chassis layer overrides')
    parser.add_argument('--default', type=int, default=0)
    parser.add_argument('--provenance', default='no provenance recorded')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    tapes = json.loads(Path(args.tapes).read_text(encoding='utf-8'))
    build(tapes, json.loads(args.stages), args.output, provenance=args.provenance,
          default=args.default, settings=json.loads(args.settings))
    print(json.dumps({'output': args.output, 'tapes': len(tapes),
                      'stages': json.loads(args.stages)}, indent=2))


if __name__ == '__main__':
    main()
