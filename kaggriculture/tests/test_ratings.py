"""The rating table decides the primary metric, so it has to be consistent and honest.

Three copies of every rating exist by design: `opponents/ratings.json` is the authority, the
per-bundle manifest travels with the pinned artifact, and `opponents/manifest.json` is the
aggregate. A copy that drifts would move the strong cohort without anyone deciding to, so
the drift fails the suite instead.
"""
from datetime import date, datetime
import json
from pathlib import Path

import pytest

from eval.ladder import KINDS, MAX_RATING_AGE_DAYS, cohort, load_ratings

ROOT = Path(__file__).resolve().parents[1]
RATINGS = json.loads((ROOT / 'opponents' / 'ratings.json').read_text(encoding='utf-8'))
BUNDLES = sorted(path.parent.name for path in
                 (ROOT / 'opponents' / 'public').glob('*/main.manifest.json'))


def test_every_pinned_bundle_is_rated_or_explicitly_unrated():
    """Silence is the failure mode: an opponent nobody classified must not exist."""
    covered = set(RATINGS['ratings']) | set(RATINGS['unrated'])
    assert set(BUNDLES) <= covered, f'unclassified: {sorted(set(BUNDLES) - covered)}'


@pytest.mark.parametrize('name', sorted(RATINGS['ratings']))
def test_rating_entries_are_well_formed(name):
    entry = RATINGS['ratings'][name]
    assert entry['kind'] in KINDS
    assert float(entry['rating']) > 0
    assert datetime.fromisoformat(entry['observed_at']).date() <= date.today()
    assert entry['source'].strip()


@pytest.mark.parametrize('name', BUNDLES)
def test_the_three_copies_agree(name):
    """A bundle manifest or the aggregate that disagrees with the authority is a bug."""
    authority = RATINGS['ratings'].get(name)
    manifest = json.loads((ROOT / 'opponents' / 'public' / name / 'main.manifest.json')
                          .read_text(encoding='utf-8')).get('ladder_rating')
    assert manifest == authority
    for entry in json.loads((ROOT / 'opponents' / 'manifest.json').read_text(encoding='utf-8')):
        if entry['id'] == name:
            assert entry.get('ladder_rating') == authority


def test_unrated_opponents_carry_a_reason():
    for name, reason in RATINGS['unrated'].items():
        assert name not in RATINGS['ratings']
        assert len(reason) > 20, f'{name} needs a reason, not a placeholder'


def test_an_upper_bound_above_the_cut_never_reaches_the_strong_cohort():
    """`thomas_t93` is the live instance: 2519.6, superseded, and it must stay unknown."""
    table = load_ratings()
    bounds = {name: entry for name, entry in table.items()
              if entry.get('kind') == 'author_upper_bound'}
    assert bounds, 'the guard is vacuous without at least one bounded opponent'
    for name, entry in bounds.items():
        assert cohort(name, table, today=date.fromisoformat(entry['observed_at'])) != 'strong'


def test_the_strong_cohort_is_not_a_single_mirror():
    """A primary metric measured against one opponent is a mirror match, not a metric."""
    table = load_ratings()
    today = max(date.fromisoformat(entry['observed_at']) for entry in table.values())
    strong = [name for name in table if cohort(name, table, today=today) == 'strong']
    assert len(strong) >= 2, strong


def test_the_age_limit_is_the_documented_one():
    """`docs/RATINGS_REFRESH.md` promises 14 days; the promise and the code are one thing."""
    assert MAX_RATING_AGE_DAYS == 14
    assert '14 dias' in (ROOT / 'docs' / 'RATINGS_REFRESH.md').read_text(encoding='utf-8')
