"""The harness's headline number: absolute win rate against a banded panel."""
import re

import pytest

from eval.standing import BANDS, band_of, gate, render, standing


def rows(specs):
    """specs: (opponent, seat, score) tuples, one seed block per index."""
    return [dict(opponent=o, seat=s, seed=i // 2, score=sc)
            for i, (o, s, sc) in enumerate(specs)]


def panel(top10=1., mid=1., low=1., blocks=20):
    out = []
    for seed in range(blocks):
        for seat in (0, 1):
            for name, rate in (('a', top10), ('b', mid), ('c', low)):
                out.append(dict(opponent=name, seat=seat, seed=seed, score=rate))
    return out


RANKS = {'a': 5, 'b': 20, 'c': 60}


def test_an_empty_band_is_unmeasured_and_never_a_pass():
    # The panel's best public artifact sits at rank 45, so both top bands are empty.
    # Reading an empty band as satisfied is the one failure that would matter.
    report = standing(panel(), {'a': 45, 'b': 60, 'c': 90})
    assert report['per_band']['top10']['win_rate'] is None
    assert report['per_band']['top10']['pass'] is False
    assert report['gate']['verdict'] == 'FAIL'
    assert any('unmeasured' in r for r in report['gate']['reasons'])


def test_each_band_is_graded_against_its_own_threshold():
    # 57% clears the 55% asked of the top ten and misses the 60% asked of ranks 10-30.
    report = standing(panel(top10=1., mid=1., low=1.), RANKS)
    assert all(report['per_band'][name]['pass'] for name, *_ in BANDS)
    assert report['gate']['verdict'] == 'PASS'
    weak_mid = standing([dict(r, score=0. if r['opponent'] == 'b' and r['seed'] % 2 else 1.)
                         for r in panel()], RANKS)
    assert weak_mid['per_band']['top10']['pass'] is True
    assert weak_mid['per_band']['rank10_30']['pass'] is False
    assert weak_mid['gate']['verdict'] == 'FAIL'


def test_a_structural_lineage_loss_fails_the_gate_the_aggregate_would_hide():
    # 25-75 against one lineage while everything else is won: the aggregate reads well
    # above every threshold and the run is still not a top-ten run.
    hostile = [dict(r, score=0. if r['opponent'] == 'c' and r['seed'] % 4 else 1.)
               for r in panel()]
    report = standing(hostile, RANKS, {'a': 'shared', 'b': 'shared', 'c': 'shared'})
    assert report['overall']['win_rate'] > .7
    assert report['worst_lineage']['lineage'] == 'shared'
    lineage_split = standing(hostile, RANKS)
    assert lineage_split['worst_lineage']['lineage'] == 'c'
    assert lineage_split['worst_lineage']['win_rate'] == .25
    assert lineage_split['gate']['verdict'] == 'FAIL'
    assert any('structural matchup' in r for r in lineage_split['gate']['reasons'])


def at_rates(rates, blocks=50):
    """One row per (block, seat, opponent), each opponent won at its own fixed rate."""
    out = []
    for name, rate in rates.items():
        games = [i for i in range(blocks * 2)]
        wins = {i for i in games if i < round(rate * len(games))}
        for i in games:
            out.append(dict(opponent=name, seat=i % 2, seed=i // 2,
                            score=float(i in wins)))
    return out


def test_the_defended_standing_tier_is_stricter_than_the_contender_tier():
    contender = standing(panel(), RANKS)
    assert contender['gate']['verdict'] == 'PASS' and contender['gate']['safe'] is True
    # Every band exactly on its own threshold: a contender, but the top-20 rate is
    # 57.5%, under the 58% at which the standing is worth defending.
    marginal = standing(at_rates({'a': .55, 'b': .60, 'c': .65}), RANKS)
    assert marginal['gate']['verdict'] == 'PASS'
    assert marginal['top20']['win_rate'] == pytest.approx(.575)
    assert marginal['gate']['safe'] is False
    assert any('under 58%' in r for r in marginal['gate']['safe_reasons'])


def test_seats_are_reported_apart_because_one_seat_can_carry_the_aggregate():
    lopsided = [dict(r, score=float(r['seat'] == 0)) for r in panel()]
    report = standing(lopsided, RANKS)
    assert report['overall']['win_rate'] == .5
    assert report['per_seat'][0]['win_rate'] == 1. and report['per_seat'][1]['win_rate'] == 0.


def test_an_unranked_opponent_is_reported_and_gates_nothing():
    report = standing(panel(), {'a': 5, 'b': 20})
    assert report['unbanded']['opponents'] == ['c']
    assert report['unbanded']['gates_nothing'] is True
    assert report['per_band']['rank30_100']['win_rate'] is None
    assert 'c' not in report['top20']['ci95']


@pytest.mark.parametrize('rank,expected', [
    (1, 'top10'), (10, 'top10'), (11, 'rank10_30'), (30, 'rank10_30'),
    (31, 'rank30_100'), (100, 'rank30_100'), (101, None), (0, None),
    (None, None), (True, None), ('5', None)])
def test_band_boundaries_and_unknown_ranks(rank, expected):
    assert band_of(rank) == expected


def test_margin_passed_as_a_score_raises_instead_of_being_averaged():
    with pytest.raises(ValueError):
        standing([dict(opponent='a', seat=0, seed=1, score=9000.)], RANKS)
    with pytest.raises(ValueError):
        standing([], RANKS)


def test_the_rendered_block_leads_with_win_rate_and_never_prints_a_rating():
    text = render(standing(panel(), RANKS), candidate='v027', panel='TOP20 META')
    assert text.splitlines()[0] == 'Candidate v027'
    assert text.splitlines()[3].startswith('WR = ')
    # Rating and gold are the two quantities this report exists to stop leading with.
    assert not re.search(r'\b(rating|elo|gold|margin|coins)\b', text, re.I)
    assert 'promotion gate = PASS' in text


def test_gate_is_a_pure_reading_of_the_report():
    report = standing(panel(), RANKS)
    assert gate(report) == report['gate']
    assert gate(report, floor=.99)['verdict'] == 'PASS'
