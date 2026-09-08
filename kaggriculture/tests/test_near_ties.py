"""Issue #41 step one: the headroom instrument must be able to say no."""
import csv

import pytest

from eval.near_ties import near_ties, verdict


def rows(specs):
    """specs: (opponent, seat, score, margin) tuples."""
    return [dict(opponent=o, seat=s, score=sc, margin=m) for o, s, sc, m in specs]


def test_a_tie_inside_the_threshold_is_worth_half_a_flipped_loss():
    # A tie already scores 0.5, so counting it as a whole reachable win would inflate
    # the headroom by exactly the amount the Bradley-Terry fit does not award.
    tie = near_ties(rows([('a', 0, .5, 0), ('a', 1, 1., 9000)]))['overall'][50]
    loss = near_ties(rows([('a', 0, 0., 0), ('a', 1, 1., 9000)]))['overall'][50]
    assert tie['headroom'] == .25 and loss['headroom'] == .5
    assert tie['ceiling_win_rate'] == loss['ceiling_win_rate'] == 1.


def test_a_wide_loss_is_not_reachable_and_does_not_move_the_ceiling():
    measurement = near_ties(rows([('a', 0, 0., -9000), ('a', 1, 1., 9000)]))
    assert measurement['overall'][50]['headroom'] == 0
    assert measurement['overall'][50]['ceiling_win_rate'] == .5
    assert verdict(measurement)['build'] is False


def test_the_instrument_flags_the_window_sell_lead_actually_closed():
    # Thirty-six mirror ties against one opponent: the pre-v004 shape, which must read
    # as buildable, next to a panel where the same games are already won, which must not.
    before = rows([('mirror', i % 2, .5, 0) for i in range(36)]
                  + [('other', i % 2, 1., 9000) for i in range(244)])
    after = rows([('mirror', i % 2, 1., 12) for i in range(36)]
                 + [('other', i % 2, 1., 9000) for i in range(244)])
    assert verdict(near_ties(before))['build'] is True
    assert near_ties(before)['per_opponent']['mirror'][50]['headroom'] == .5
    assert verdict(near_ties(after))['build'] is False


def test_seats_are_reported_apart_because_the_market_race_is_resolved_by_seat():
    measurement = near_ties(rows([('a', 0, 0., 10), ('a', 0, 0., 10),
                                  ('a', 1, 1., 10), ('a', 1, 1., 10)]))
    assert measurement['per_seat'][0][50]['headroom'] == 1.
    assert measurement['per_seat'][1][50]['headroom'] == 0.
    assert measurement['overall'][50]['headroom'] == .5


def test_reads_a_results_directory_and_normalises_the_opponent_spec(tmp_path):
    target = tmp_path / 'run'
    target.mkdir()
    with (target / 'matches.csv').open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(['candidate', 'opponent', 'seed', 'seat', 'score', 'margin'])
        writer.writerow(['us', 'clock::opponents/public/thomas_t95/main.py', 1, 0, 0.0, 20])
    measurement = near_ties(target)
    assert set(measurement['per_opponent']) == {'thomas_t95'}
    assert measurement['overall'][50]['losses_within'] == 1


@pytest.mark.parametrize('bad', [[], [('a', 0, 0., 0)]])
def test_empty_evidence_and_empty_thresholds_raise_instead_of_reporting_zero(bad):
    if bad:
        with pytest.raises(ValueError):
            near_ties(rows(bad), thresholds=[])
    else:
        with pytest.raises(ValueError):
            near_ties(rows(bad))
