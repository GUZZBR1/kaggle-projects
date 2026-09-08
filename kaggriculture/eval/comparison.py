"""Freeze the evidence and cohort behind a reproducible wins-only comparison."""
from datetime import date
import hashlib
import json
from pathlib import Path

from .ladder import (ROOT, STRONG_CUT, MAX_RATING_AGE_DAYS, delta_win, delta_interval,
                     leave_one_out, carried_by, load_ratings, concentrated_regression, _paired)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    allow_nan=False).encode()).hexdigest()


def load_families():
    entries = json.loads((ROOT / 'opponents/manifest.json').read_text())
    return {row['id']: row.get('family') or row['id'] for row in entries}


def build_comparison(baseline, candidate, *, ratings=None, families=None, mirrors=(), split=None,
                     cut=STRONG_CUT, max_age_days=MAX_RATING_AGE_DAYS, today=None):
    today = today or date.today()
    ratings = json.loads(json.dumps(load_ratings() if ratings is None else ratings))
    families = dict(load_families() if families is None else families)
    options = dict(cut=cut, max_age_days=max_age_days, today=today)
    result = delta_win(baseline, candidate, ratings, **options)
    left, right = _paired(baseline, candidate)
    names = sorted(result['per_opponent'])
    families = {name: families.get(name, name) for name in names}
    mirrors = set(mirrors)
    if not mirrors <= set(names):
        raise ValueError('Declared mirror must belong to the compared panel')
    # Byte-identical self-play is independently detectable. Tape sharing can be
    # declared explicitly, because historical match rows do not record tape lineage.
    mirrors.update(name for (_, _, name), row in left.items()
                   if row['candidate_hash'] == row['opponent_hash'])
    strong = {name for name in names if result['per_opponent'][name]['cohort'] == 'strong'}
    dropped = {}
    for family in sorted({families[name] for name in strong}):
        rows = [{'seed': key[0], 'score': right[key]['score'] - old['score']}
                for key, old in left.items() if key[2] in strong and families[key[2]] != family]
        dropped[family] = {'games': len(rows),
                           'delta_win': sum(r['score'] for r in rows) / len(rows) if rows else None,
                           'ci95': delta_interval(rows) if rows else [None, None]}
    result.update(schema_version=1, evidence_validated=True, evaluation_split=split,
                  leave_one_out=leave_one_out(baseline, candidate, ratings, **options),
                  leave_family_out=dropped, mirrors=sorted(mirrors), families=families)
    result['concentrated_regression'] = concentrated_regression(result)
    result['carried_by'] = carried_by(result['leave_one_out'])
    result['carried_by_family'] = carried_by(dropped)
    result['snapshot'] = {
        'as_of': today.isoformat(), 'cut': cut, 'max_rating_age_days': max_age_days,
        'ratings': ratings, 'ratings_sha256': digest(ratings),
        'families': families, 'families_sha256': digest(families),
        'baseline_hash': next(iter(left.values()))['candidate_hash'],
        'candidate_hash': next(iter(right.values()))['candidate_hash'],
        'opponent_hashes': {name: row['opponent_hash'] for (_, _, name), row in left.items()},
        'environment': next(iter(left.values()))['environment'],
        'configuration': {key: value for key, value in next(iter(left.values()))['configuration'].items()
                          if key != 'seed'},
        'backend': next(iter(left.values()))['backend'],
        'baseline_rows_sha256': digest(list(left.values())),
        'candidate_rows_sha256': digest(list(right.values())),
    }
    return result
