import copy
from datetime import date
import json
from pathlib import Path

import pytest

from eval.comparison import build_comparison
from eval.ladder import delta_win
from eval.submit_gate import decide

TODAY = date(2026, 9, 8)
RATINGS = {name: dict(rating=2500, kind='direct', observed_at='2026-09-08')
           for name in ('top', 'other', 'third', 'mirror')}


def games(score=0, count=100, names=('top', 'other', 'third')):
    return [dict(seed=seed, seat=seat, opponent=name, candidate_hash='old',
                 opponent_hash=name + '-hash', environment={}, configuration={'seed': seed},
                 backend='fast', failures=[], opponent_failures=[], score=score, margin=0)
            for seed in range(count) for name in names for seat in (0, 1)]


def comparison(before, after, **kwargs):
    return build_comparison(before, after, ratings=RATINGS, families={}, today=TODAY,
                            split='validation', **kwargs)


@pytest.mark.parametrize('field,value', [
    ('candidate_hash', 'different'), ('opponent_hash', 'different'),
    ('environment', {'engine': 'changed'}), ('configuration', {'startingMoney': 5}),
    ('backend', 'official'), ('failures', ['crash']), ('opponent_failures', ['crash']),
    ('score', 3), ('score', float('nan'))])
def test_rejects_contaminated_wins_only_evidence(field, value):
    before, after = games(count=2), games(count=2)
    after[0][field] = value
    with pytest.raises(ValueError):
        comparison(before, after)


def test_same_missing_seat_on_both_legs_is_not_complete_evidence():
    rows = [row for row in games(count=2) if row['seat'] == 0]
    with pytest.raises(ValueError, match='both seats'):
        comparison(rows, rows)


def test_same_missing_opponent_block_on_both_legs_is_rejected():
    rows = games(count=2)
    rows = [r for r in rows if not (r['seed'] == 0 and r['opponent'] == 'top')]
    with pytest.raises(ValueError, match='complete seed blocks'):
        comparison(rows, rows)


def test_adapters_and_missing_metadata_cannot_be_erased_by_opponent_id():
    before, after = games(count=2), games(count=2)
    for row in after:
        row['opponent'] = 'clock::' + row['opponent']
    with pytest.raises(ValueError, match='Unpaired'):
        comparison(before, after)
    after = games(count=2)
    del after[0]['environment']
    with pytest.raises(ValueError, match='Missing comparison evidence'):
        comparison(before, after)


def test_bootstrap_is_row_order_independent_and_one_block_has_no_ci():
    before, after = games(count=3), games(count=3)
    for row in after:
        row['score'] = .5 if row['seed'] == 0 else 1
    a = comparison(before, after)
    b = comparison(list(reversed(before)), list(reversed(after)))
    assert a == b
    assert a['bootstrap']['samples'] >= 10000
    one = comparison(games(count=1), games(score=1, count=1))
    assert one['strong']['ci95'] == [None, None]
    assert decide(one)['verdict'] == 'NO SUBMIT'


def test_gate_accepts_broad_validation_gain_and_ignores_margin():
    before, after = games(), games(score=1)
    result = comparison(before, after)
    assert decide(result)['verdict'] == 'SUBMIT'
    for row in after:
        row['margin'] = -1000000
    assert decide(comparison(before, after)) == decide(result)
    result['evaluation_split'] = 'dev'
    assert decide(result)['verdict'] == 'NO SUBMIT'


def test_gate_rejects_missing_leave_out_evidence_and_strong_regression():
    before, after = games(), games(score=1)
    result = comparison(before, after)
    del result['leave_one_out']['top']
    assert decide(result)['verdict'] == 'NO SUBMIT'
    for old, new in zip(before, after):
        if old['opponent'] == 'top':
            old['score'], new['score'] = 1, 0
    result = decide(comparison(before, after))
    assert result['verdict'] == 'NO SUBMIT'
    assert any('Regression against strong opponents: top' in r for r in result['reasons'])


def test_gate_catches_a_family_carried_by_two_related_artifacts():
    before, after = games(), games()
    for row in after:
        if row['opponent'] != 'third':
            row['score'] = 1
    result = build_comparison(before, after, ratings=RATINGS, today=TODAY,
        families={'top': 'shared', 'other': 'shared', 'third': 'independent'}, split='validation')
    assert result['carried_by'] == []
    assert result['carried_by_family'] == ['shared']
    assert decide(result)['verdict'] == 'NO SUBMIT'


def historical_rows():
    data = json.loads((Path(__file__).parent / 'fixtures/v004-paired.json').read_text())
    before, after = [], []
    for seed, seat, opponent, a, b, margin_a, margin_b in data['pairs']:
        common = dict(seed=seed, seat=seat, opponent=opponent,
            opponent_hash=data['opponent_hashes'][opponent], environment=data['environment'],
            configuration=dict(data['configuration'], seed=seed), backend=data['backend'],
            failures=[], opponent_failures=[])
        before.append(dict(common, candidate_hash=data['baseline_hash'], score=a, margin=margin_a))
        after.append(dict(common, candidate_hash=data['candidate_hash'], score=b, margin=margin_b))
    return before, after


def test_v004_reproduces_paired_numbers_and_gate_names_the_mirror():
    before, after = historical_rows()
    ratings = {'yhay_router_0908': dict(rating=2713.9, observed_at='2026-09-08', kind='direct'),
               'thomas_t95': dict(rating=2359.8, observed_at='2026-09-08', kind='direct')}
    result = build_comparison(before, after, ratings=ratings, families={}, today=TODAY,
                             mirrors=['yhay_router_0908'], split='validation')
    assert result['all']['delta_win'] == pytest.approx(.080)
    assert result['all']['ci95'] == pytest.approx([.045714285714285714, .11428571428571428])
    without = [[r for r in rows if 'yhay_router_0908' not in r['opponent']] for rows in (before, after)]
    delta = delta_win(*without, ratings=ratings, today=TODAY)
    assert delta['all']['delta_win'] == pytest.approx(.0166666667)
    assert delta['all']['ci95'] == pytest.approx([-.026666666666666665, .06])
    gate = decide(result)
    assert gate['verdict'] == 'NO SUBMIT'
    assert any('mirror / shared-tape opponent yhay_router_0908' in r for r in gate['reasons'])
