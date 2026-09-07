import hashlib
import inspect
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = {
    'crop': {'only_crop': 'CARROT', 'adaptive': False, 'max_quadrants': 1},
    'animal': {'animal_target': 6, 'animal_type': 'GOOSE', 'max_hands': 9},
    'diversified': {'opponent_weight': 1.2, 'max_hands': 10, 'max_quadrants': 3},
}


def load_agent(name, seed=0):
    if name == 'champion':
        return load_agent(str(ROOT / 'versions/v000/main.py'), seed)
    if name in ('starter', 'pass'):
        from .engine import official
        return official().agents[name]
    if name == 'random':
        # The upstream random agent constructs an unseeded Random every turn.
        # This explicitly named local seeded baseline is reproducible instead.
        import random
        rng = random.Random(seed)
        def random_agent(obs, config=None):
            me = obs['farms'][obs['player']]
            choices = [['PASS'], ['NORTH'], ['SOUTH'], ['EAST'], ['WEST'], ['WATER'], ['HARVEST']]
            available = [c for c, n in obs['private']['seeds'].items() if n > 0]
            if available:
                choices += [['PLANT', rng.choice(available)]]
            market = [['SELL', c, n] for c, n in obs['private']['shed'].items() if n > 0]
            if me['money'] >= 20 and not available:
                market.append(['BUY_SEED', 'CARROT', 1])
            return {'farmer': rng.choice(choices), 'hands': [], 'market': market[:10]}
        return random_agent
    if name in VARIANTS or name == 'challenger':
        from agent.planner import policy
        params = VARIANTS.get(name, {})
        def variant(obs, config=None):
            return policy(obs, config, params)
        return variant
    path = Path(name).resolve()
    if not path.is_file():
        raise ValueError(f'Unknown agent {name!r}')
    # Fresh namespace per seat/game prevents accidental state leakage.
    # Public bundles register names such as v23/v43 in sys.modules. Keep those
    # modules private to this load, including when two seats load the same file.
    before = dict(sys.modules)
    name = '__kaggriculture_submission__'
    module = types.ModuleType(name)
    module.__file__ = str(path)
    sys.modules[name] = module
    try:
        exec(compile(path.read_text(encoding='utf-8'), str(path), 'exec'), module.__dict__)
        function = module.__dict__['agent']
    finally:
        for key in set(sys.modules) - before.keys():
            del sys.modules[key]
        sys.modules.update(before)
    return function


def invoke(function, observation, configuration):
    sig = inspect.signature(function)
    if len(sig.parameters) >= 2:
        return function(observation, configuration)
    return function(observation)


def agent_hash(name):
    if name == 'champion':
        return agent_hash(str(ROOT / 'versions/v000/main.py'))
    path = Path(name)
    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    if name in ('starter', 'pass'):
        from .engine import INTERPRETER_HASH
        return hashlib.sha256((INTERPRETER_HASH + name).encode()).hexdigest()
    digest = hashlib.sha256()
    for source in sorted((ROOT / 'agent').glob('*.py')):
        digest.update(source.name.encode())
        digest.update(source.read_bytes())
    digest.update(Path(__file__).read_bytes())
    digest.update(name.encode())
    return digest.hexdigest()
