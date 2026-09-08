"""Issue #24: provenance-gated, family-level public base tournament."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import statistics

from arena.agents import agent_hash, invoke, load_agent
from arena.engine import INTERPRETER_HASH, VERSION, make_environment
from arena.league import run_league
from arena.match import observations
from eval.compare import compare
from eval.metrics import blocked_interval, summarize


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / 'opponents' / 'manifest.json'
V002 = ROOT / 'versions' / 'v002' / 'main.py'
REQUIRED = ('id', 'family', 'path', 'sha256', 'license', 'engine', 'lineage',
            'adaptation_notes')


def _v002_entry():
    manifest = json.loads((V002.parent / 'main.manifest.json').read_text(encoding='utf-8'))
    return {
        'id': 'v002',
        'family': 'internal_adaptive_planner',
        'path': str(V002),
        'sha256': manifest['sha256'],
        'license': 'Repository license; first-party frozen artifact',
        'engine': {'name': 'kaggriculture', 'version': VERSION},
        'lineage': 'kaggriculture_internal_planner_v000_v002',
        'adaptation_notes': 'None; immutable v002 release artifact',
        'source': 'this repository',
        'version': 'v002',
        'base_selection_candidate': True,
        'evaluation_opponent': True,
    }


def _absolute_path(value):
    path = Path(value)
    return path.resolve() if path.is_absolute() else (ROOT / path).resolve()


def _source(entry):
    return entry.get('source') or entry.get('repository') or entry.get('source_url')


def _version(entry):
    return entry.get('version') or entry.get('commit') or entry.get('revision')


def validate_entry(entry, *, manifest_path=DEFAULT_MANIFEST):
    """Return a normalized entry or fail closed before any game runs."""
    missing = [field for field in REQUIRED if not entry.get(field)]
    if not _source(entry):
        missing.append('source/repository')
    if not _version(entry):
        missing.append('version/commit')
    if missing:
        raise ValueError(f"{entry.get('id', '<unknown>')} lacks provenance fields: {missing}")
    if not isinstance(entry['family'], str) or not isinstance(entry['lineage'], str):
        raise ValueError(f"{entry['id']} family and lineage must be strings")
    license_name = str(entry['license']).strip().lower()
    if license_name in ('unknown', 'unverified', 'none', 'n/a'):
        raise ValueError(f"{entry['id']} has no verified license")
    engine = entry['engine']
    engine_version = ((engine.get('version') or engine.get('kaggle_environments'))
                      if isinstance(engine, dict) else str(engine))
    if VERSION not in str(engine_version):
        raise ValueError(f"{entry['id']} targets engine {engine!r}, expected {VERSION}")
    if isinstance(engine, dict) and engine.get('interpreter_sha256') not in (None, INTERPRETER_HASH):
        raise ValueError(f"{entry['id']} targets a different interpreter")
    path = _absolute_path(entry['path'])
    try:
        path.relative_to(ROOT)
    except ValueError as exc:
        raise ValueError(f"{entry['id']} path escapes the project") from exc
    if not path.is_file():
        raise ValueError(f"{entry['id']} artifact is missing: {path}")
    # Git may materialize tracked Python text with CRLF on Windows. Accept the
    # exact checkout digest or its canonical LF form, and retain both so the
    # decision remains auditable across platforms.
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    canonical = hashlib.sha256(path.read_text(encoding='utf-8').replace('\r\n', '\n').encode()).hexdigest()
    if entry['sha256'] not in (digest, canonical):
        raise ValueError(f"{entry['id']} SHA256 mismatch: manifest={entry['sha256']} "
                         f"actual={digest} canonical={canonical}")
    result = dict(entry, path=str(path), source=_source(entry), version=_version(entry))
    result['agent_spec'] = 'clock::' + str(path)
    result['checkout_sha256'] = digest
    result['canonical_sha256'] = canonical
    result['manifest'] = str(Path(manifest_path).resolve())
    return result


def load_pool(manifest_path=DEFAULT_MANIFEST, candidate_ids=None, opponent_ids=None):
    raw = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    if not isinstance(raw, list):
        raise ValueError('Opponent manifest must be a list')
    entries = [_v002_entry(), *raw]
    normalized = {entry['id']: validate_entry(entry, manifest_path=manifest_path)
                  for entry in entries}
    if len(normalized) != len(entries):
        raise ValueError('Manifest IDs must be unique, including reserved id v002')
    if candidate_ids is None:
        # The issue is specifically allowed to assess provenance-complete public
        # benchmark bundles as possible bases. `usage` still documents their
        # normal role; it is not allowed to silently exclude them from #24.
        candidate_ids = [entry['id'] for entry in entries]
    if opponent_ids is None:
        opponent_ids = [entry['id'] for entry in entries]
    unknown = (set(candidate_ids) | set(opponent_ids)) - normalized.keys()
    if unknown:
        raise ValueError(f'Unknown tournament IDs: {sorted(unknown)}')
    candidates = [normalized[name] for name in candidate_ids]
    opponents = [normalized[name] for name in opponent_ids]
    if len(candidates) < 3:
        raise ValueError('Base selection requires v002 and at least two public candidates')
    if len({entry['family'] for entry in candidates}) != len(candidates):
        raise ValueError('Candidates must represent distinct strategy families')
    if len({entry['lineage'] for entry in candidates}) != len(candidates):
        raise ValueError('Duplicated candidate lineage cannot count as independent evidence')
    if len({entry['family'] for entry in opponents}) < 3:
        raise ValueError('Robust selection requires at least three opponent families')
    return candidates, opponents


def compatibility_check(entry, seed=17):
    """Exercise both accepted clock shapes before treating a bundle as evidence."""
    env = make_environment(seed)
    base = observations(env.state)[0]
    base['player'] = 0
    results = []
    for clock in ('missing', 'none'):
        obs = json.loads(json.dumps(base))
        if clock == 'missing':
            obs.pop('step', None)
        else:
            obs['step'] = None
        function = load_agent(entry['agent_spec'], seed)
        action = invoke(function, obs, dict(env.configuration))
        if not isinstance(action, dict) or set(action) != {'farmer', 'hands', 'market'}:
            raise ValueError(f"{entry['id']} returned malformed action for step={clock}")
        json.dumps(action, allow_nan=False)
        results.append({'clock': clock, 'action_sha256': hashlib.sha256(
            json.dumps(action, sort_keys=True).encode()).hexdigest()})
    if len({row['action_sha256'] for row in results}) != 1:
        raise ValueError(f"{entry['id']} changes action when optional step is absent")
    return {'status': 'compatible', 'checks': results}


def _family_rows(rows, opponents):
    families = {}
    for entry in opponents:
        for value in (entry['path'], entry.get('agent_spec')):
            if value:
                families[value] = entry['family']
        families[str(Path(entry['path']).resolve())] = entry['family']
    grouped = defaultdict(list)
    for row in rows:
        name = row['opponent']
        family = families.get(name) or families.get(str(Path(name).resolve()))
        if family is None:
            raise ValueError(f'No family provenance for opponent {name!r}')
        grouped[family].append(row)
    return grouped


def _family_summary(rows, opponents, own_family=None):
    """Family scores for one candidate, excluding its own mirror match.

    A candidate meets itself in the opponent pool and that match-up scores
    exactly .5 by construction, in both seats, for every candidate. Counting it
    tells us nothing about robustness and it silently floors the selection key
    at .5 for anyone who never loses a family, handing the decision to the
    tie-breaks instead. Worse, the variance tie-break then punishes a candidate
    for dominating, because .5 sits far from its real scores.
    """
    result = {}
    for family, batch in sorted(_family_rows(rows, opponents).items()):
        if family == own_family:
            continue
        scores = [row['score'] for row in batch]
        result[family] = {
            'games': len(batch),
            'seed_blocks': len({row['seed'] for row in batch}),
            'score': statistics.mean(scores),
            'score_ci95': blocked_interval(batch),
            'money': statistics.mean(row['money'] for row in batch),
            'margin_diagnostic': statistics.mean(row['margin'] for row in batch),
        }
    return result


def _paired_by_family(baseline, candidate, opponents):
    left = _family_rows(baseline, opponents)
    right = _family_rows(candidate, opponents)
    return {family: compare(left[family], right[family])['paired_deltas']
            for family in sorted(left)}


def analyze_tournament(results, candidates, opponents, *, min_seed_blocks=100,
                       tie_tolerance=.05):
    """Select by the worst family confidence bound, never aggregate score."""
    expected = {entry['id'] for entry in candidates}
    if set(results) != expected:
        raise ValueError('Missing or unexpected candidate results')
    if len({entry['family'] for entry in opponents}) < 3:
        raise ValueError('At least three opponent families are required')
    for entry in candidates:
        rival_families = {other['family'] for other in opponents} - {entry['family']}
        if len(rival_families) < 2:
            raise ValueError(f"{entry['id']} needs at least two rival families once its "
                             'own mirror match is excluded')
    metrics = {}
    for entry in candidates:
        rows = results[entry['id']]
        if len({row['seed'] for row in rows}) < min_seed_blocks:
            raise ValueError(f"{entry['id']} has fewer than {min_seed_blocks} seed blocks")
        if any(row['failures'] or row['opponent_failures'] for row in rows):
            raise ValueError(f"{entry['id']} has callback failures")
        families = _family_summary(rows, opponents, own_family=entry['family'])
        scores = [data['score'] for data in families.values()]
        metrics[entry['id']] = {
            'family': entry['family'],
            'aggregate': summarize(rows),
            'families': families,
            'worst_family_score': min(scores),
            'worst_family_ci95_lower': min(data['score_ci95'][0] for data in families.values()),
            'cross_family_score_stdev': statistics.pstdev(scores),
            'matchup_imbalance': max(scores) - min(scores),
        }
    baseline = results['v002']
    paired = {entry['id']: {
        'aggregate': compare(baseline, results[entry['id']]),
        'families': _paired_by_family(baseline, results[entry['id']], opponents),
    } for entry in candidates if entry['id'] != 'v002'}
    ordered = sorted(candidates, key=lambda entry: (
        -metrics[entry['id']]['worst_family_ci95_lower'],
        -metrics[entry['id']]['worst_family_score'],
        metrics[entry['id']]['cross_family_score_stdev'], entry['id']))
    best = ordered[0]
    best_floor = metrics[best['id']]['worst_family_score']
    selected = [entry for entry in ordered
                if best_floor - metrics[entry['id']]['worst_family_score'] <= tie_tolerance]
    return {
        'schema_version': 1,
        'selection_rule': 'max worst-family score CI95 lower over rival families only '
                          '(the mirror match is excluded); worst score and lower variance break ties',
        'status': 'selected',
        'selected_base': {key: best[key] for key in
                          ('id', 'family', 'path', 'agent_spec', 'sha256', 'lineage', 'source', 'version')},
        'selected_bases_within_tolerance': [entry['id'] for entry in selected],
        'tie_tolerance': tie_tolerance,
        'min_seed_blocks': min_seed_blocks,
        'metrics': metrics,
        'paired_vs_v002': paired,
    }


def run_tournament(candidates, opponents, seeds, output, *, workers=4, backend='fast',
                   split='dev', min_seed_blocks=100, tie_tolerance=.05):
    output = Path(output)
    if output.exists():
        raise FileExistsError(output)
    if split != 'dev':
        raise ValueError('Issue #24 selection is restricted to registered DEV evidence')
    checks = {entry['id']: compatibility_check(entry) for entry in candidates + opponents}
    output.mkdir(parents=True)
    results = {}
    try:
        for entry in candidates:
            rows, _, _ = run_league(entry['agent_spec'], [opponent['agent_spec'] for opponent in opponents],
                                    seeds, workers, backend, output / entry['id'], split)
            results[entry['id']] = rows
        decision = analyze_tournament(results, candidates, opponents,
                                      min_seed_blocks=min_seed_blocks,
                                      tie_tolerance=tie_tolerance)
        decision['protocol'] = {
            'split': split, 'seeds': seeds, 'backend': backend, 'seats': [0, 1],
            'candidates': candidates, 'opponents': opponents,
            'compatibility': checks,
        }
        (output / 'decision.json').write_text(json.dumps(decision, indent=2) + '\n', encoding='utf-8')
        return decision
    except Exception:
        (output / 'INCOMPLETE').write_text('This directory is not selection evidence.\n', encoding='utf-8')
        raise


def _ids(value):
    return value.split(',') if value else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest', default=str(DEFAULT_MANIFEST))
    parser.add_argument('--candidates', help='comma-separated manifest IDs; v002 is available')
    parser.add_argument('--opponents', help='comma-separated manifest IDs; v002 is available')
    parser.add_argument('--seeds', default='1000:1100')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--backend', choices=('fast', 'official'), default='fast')
    parser.add_argument('--output', required=True)
    parser.add_argument('--min-seed-blocks', type=int, default=100)
    parser.add_argument('--tie-tolerance', type=float, default=.05)
    args = parser.parse_args()
    from arena.seeds import parse_seeds
    candidates, opponents = load_pool(args.manifest, _ids(args.candidates), _ids(args.opponents))
    decision = run_tournament(candidates, opponents, parse_seeds(args.seeds), args.output,
                              workers=args.workers, backend=args.backend,
                              min_seed_blocks=args.min_seed_blocks,
                              tie_tolerance=args.tie_tolerance)
    print(json.dumps({'selected_base': decision['selected_base'],
                      'also_within_tolerance': decision['selected_bases_within_tolerance']}, indent=2))


if __name__ == '__main__':
    main()
