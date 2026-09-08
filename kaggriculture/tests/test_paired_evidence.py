import copy
from datetime import date
import json
from pathlib import Path

import pytest

from eval.comparison import build_comparison
from eval.ladder import delta_win
from eval.submit_gate import decide

# The synthetic legs in this module are built by games(), whose baseline rows all
# carry candidate_hash='old', so that hash is the incumbent for every local fixture.
INCUMBENT = {'id': 'active', 'hash': 'old', 'displaces': 'slot A (v003)'}

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
    assert decide(result, INCUMBENT)['verdict'] == 'SUBMIT'
    for row in after:
        row['margin'] = -1000000
    assert decide(comparison(before, after), INCUMBENT) == decide(result, INCUMBENT)
    result['evaluation_split'] = 'dev'
    assert decide(result, INCUMBENT)['verdict'] == 'NO SUBMIT'


def test_a_passing_comparison_against_a_non_incumbent_decides_nothing():
    # The defect of issue #40: the baseline was the strongest panel artifact, which is
    # normally stronger than our own active agent, so a real gain was read as a refusal.
    result = comparison(games(), games(score=1))
    assert decide(result)['verdict'] == 'NO DECISION'
    wrong = dict(INCUMBENT, hash='some-panel-artifact')
    verdict = decide(result, wrong)
    assert verdict['verdict'] == 'NO DECISION'
    assert verdict['comparison_role'] == 'measurement'
    assert 'not the declared incumbent' in verdict['reasons'][0]
    assert decide(result, INCUMBENT)['verdict'] == 'SUBMIT'


@pytest.mark.parametrize('field', ['id', 'hash', 'displaces'])
def test_an_incomplete_incumbent_declaration_cannot_authorize_a_release(field):
    # `displaces` is the active-submission bookkeeping FINAL_SUBMISSION_POLICY requires
    # before a send, and nothing downstream can reconstruct which slot was destroyed.
    result = comparison(games(), games(score=1))
    assert decide(result, {**INCUMBENT, field: ''})['verdict'] == 'NO DECISION'


def test_a_failing_comparison_keeps_its_finding_when_the_baseline_is_only_a_measurement():
    # Refusing to decide must not erase a measured failure: NO SUBMIT survives, and the
    # reason it survives on is the criteria failure, not the missing declaration.
    result = comparison(games(), games())
    assert decide(result)['verdict'] == 'NO SUBMIT'
    assert any('strictly positive CI95' in r for r in decide(result)['reasons'])
    assert not any('No incumbent declared' in r for r in decide(result)['reasons'][:1])


def test_the_panel_ceiling_is_reported_beside_the_decision_and_never_changes_it():
    over_incumbent = comparison(games(), games(score=1))
    against_ceiling = comparison(games(score=1), games(score=1))
    plain = decide(over_incumbent, INCUMBENT)
    with_ceiling = decide(over_incumbent, INCUMBENT, against_ceiling)
    assert with_ceiling['verdict'] == plain['verdict'] == 'SUBMIT'
    assert with_ceiling['delta_over_panel_ceiling']['diagnostic_only'] is True
    assert with_ceiling['delta_over_panel_ceiling']['all']['delta_win'] == 0
    assert with_ceiling['delta_over_baseline']['all']['delta_win'] == 1


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
    # The yhay router is declared as the measurement baseline, not as an incumbent it
    # never was, and the verdict this run recorded at the time is unchanged.
    gate = decide(result)
    assert gate['verdict'] == 'NO SUBMIT'
    assert gate['comparison_role'] == 'measurement'
    assert any('mirror / shared-tape opponent yhay_router_0908' in r for r in gate['reasons'])


def recorded(name):
    return json.loads((Path(__file__).parent.parent / 'docs' / name).read_text())


def test_the_same_candidate_is_a_release_over_the_incumbent_and_a_measurement_over_the_ceiling():
    """Issue #40, on the two comparisons that actually contradicted each other.

    v004 against `thomas_t95`, the artifact that held our active slot, and v004 against
    the yhay router, the strongest artifact in the panel. Both were run; both are
    correct; only the first is a submission decision.
    """
    over_incumbent = recorded('incumbent-t95-comparison.json')
    over_ceiling = recorded('v004-paired-comparison.json')
    incumbent = {'id': 'thomas_t95', 'hash': over_incumbent['snapshot']['baseline_hash'],
                 'displaces': 'slot A (thomas_t95 verbatim, rated 2359.8)'}

    # Against the incumbent the effect clears every bar the gate sets on the effect
    # itself: strongly positive, no regression anywhere, carried by no single opponent.
    assert over_incumbent['strong']['delta_win'] == .5
    assert over_incumbent['strong']['ci95'][0] > 0
    assert over_incumbent['carried_by'] == [] and over_incumbent['carried_by_family'] == []
    assert min(row['delta_win'] for row in over_incumbent['per_opponent'].values()) >= 0

    # What remains against it is provenance only -- this run is dev and 20 blocks --
    # and nothing about whether the candidate is better.
    gate = decide(over_incumbent, incumbent)
    assert gate['verdict'] == 'NO SUBMIT' and gate['comparison_role'] == 'incumbent'
    assert all('validation provenance' in r or 'paired seed blocks' in r for r in gate['reasons'])

    # Against the panel ceiling the same candidate does not establish an effect. A
    # measured failure keeps its verdict however the baseline was declared -- softening
    # it to NO DECISION would lose the finding -- but the misdeclaration is still said.
    assert decide(over_ceiling)['verdict'] == 'NO SUBMIT'
    misdeclared = decide(over_ceiling, dict(incumbent, hash='not-the-baseline'))
    assert misdeclared['verdict'] == 'NO SUBMIT'
    assert misdeclared['comparison_role'] == 'measurement'
    assert any('not the declared incumbent' in r for r in misdeclared['reasons'])


def test_the_ceiling_delta_travels_with_the_decision_without_touching_it():
    over_incumbent = recorded('incumbent-t95-comparison.json')
    incumbent = {'id': 'thomas_t95', 'hash': over_incumbent['snapshot']['baseline_hash'],
                 'displaces': 'slot A'}
    gate = decide(over_incumbent, incumbent, recorded('v004-paired-comparison.json'))
    assert gate['delta_over_baseline']['strong']['delta_win'] == .5
    assert gate['delta_over_panel_ceiling']['all']['delta_win'] == pytest.approx(.08)
    assert gate['reasons'] == decide(over_incumbent, incumbent)['reasons']
