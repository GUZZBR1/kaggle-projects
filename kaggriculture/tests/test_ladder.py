"""The local objective has to be the leaderboard's objective, or the optimiser drifts.

Two failures are the ones worth guarding: scoring a candidate on coins, which the fit never
sees, and reading an average that one opponent is carrying.
"""
import pytest

from eval.ladder import (carried_by, cohort, concentrated_regression, delta_win,
                         leave_one_out, opponent_id, score, tally)


RATINGS = {'top': {'rating': 2700., 'observed_at': '2026-09-08'},
           'mid': {'rating': 2350., 'observed_at': '2026-09-08'},
           'low': {'rating': 900., 'observed_at': '2026-09-08'},
           'stale': {'rating': 2900., 'observed_at': '2026-08-01'},
           'blank': {'rating': None, 'observed_at': '2026-09-08'}}
TODAY = __import__('datetime').date(2026, 9, 8)


def game(opponent, seed, seat, score_value, margin=0):
    return {'opponent': f'clock::opponents/public/{opponent}/main.py', 'seed': seed,
            'seat': seat, 'score': score_value, 'margin': margin}


def league(results, seeds=range(10)):
    """`results` maps an opponent to the score it concedes in every game."""
    return [game(name, seed, seat, value)
            for name, value in results.items() for seed in seeds for seat in (0, 1)]


def test_opponent_id_is_idempotent():
    """Callers pass a full spec or an already-extracted id; both must survive."""
    assert opponent_id('clock::opponents/public/thomas_t95/main.py') == 'thomas_t95'
    assert opponent_id('thomas_t95') == 'thomas_t95'
    assert opponent_id('versions/v004/main.py') == 'v004'


@pytest.mark.parametrize('name,expected', [
    ('top', 'strong'), ('mid', 'strong'), ('low', 'weak'),
    ('stale', 'unknown'), ('blank', 'unknown'), ('never_measured', 'unknown')])
def test_an_unrated_or_stale_opponent_is_never_strong(name, expected):
    """Defaulting an unmeasured opponent into the primary metric would decide the thing
    the primary metric exists to measure."""
    assert cohort(name, RATINGS, today=TODAY) == expected


def test_a_game_scores_win_loss_or_tie_and_nothing_else():
    counts = tally([game('top', 0, 0, 1), game('top', 0, 1, .5), game('top', 1, 0, 0)])
    assert (counts['wins'], counts['ties'], counts['losses']) == (1, 1, 1)
    assert counts['win_rate'] == pytest.approx(.5)
    with pytest.raises(ValueError, match='margin is not a score'):
        tally([game('top', 0, 0, 12000)])


def test_margin_never_moves_the_metric():
    """The whole point: a wider win is not a better result."""
    lean = league({'top': 1., 'low': 0.})
    rich = [dict(row, margin=20000) for row in lean]
    without_diagnostic = lambda rows: {key: value for key, value
                                       in score(rows, RATINGS, today=TODAY)['primary'].items()
                                       if key != 'mean_margin_diagnostic'}
    assert without_diagnostic(lean) == without_diagnostic(rich)
    # The diagnostic still moves; it just never reaches the metric.
    assert score(rich, RATINGS, today=TODAY)['primary']['mean_margin_diagnostic'] == 20000


def test_the_primary_metric_ignores_the_weak_end_of_the_panel():
    """Rating-adaptive matchmaking stops pairing a strong agent against weak ones, so an
    aggregate that averages them in is a number the ladder will never reproduce."""
    rows = league({'top': 0., 'mid': 0., 'low': 1., 'never_measured': 1.})
    result = score(rows, RATINGS, today=TODAY)
    assert result['primary']['win_rate'] == pytest.approx(0.)
    assert result['secondary']['win_rate'] == pytest.approx(.5)


def test_an_unpaired_comparison_raises_instead_of_widening():
    base = league({'top': .5}, seeds=range(4))
    with pytest.raises(ValueError, match='Unpaired'):
        delta_win(base, league({'top': .5}, seeds=range(3)), RATINGS, today=TODAY)
    with pytest.raises(ValueError, match='Duplicate'):
        delta_win(base + base[:1], base + base[:1], RATINGS, today=TODAY)


def test_a_gain_carried_by_one_opponent_is_named():
    """A candidate that beats the panel member it shares tapes with, and ties everything
    else, reports a healthy average. Dropping that opponent is what exposes it."""
    base = league({'top': .5, 'mid': .5})
    candidate = league({'top': 1., 'mid': .5})
    delta = delta_win(base, candidate, RATINGS, today=TODAY)
    assert delta['strong']['delta_win'] == pytest.approx(.25)
    dropped = leave_one_out(base, candidate, RATINGS, today=TODAY)
    assert dropped['mid']['delta_win'] == pytest.approx(.5)
    assert dropped['top']['delta_win'] == pytest.approx(0.)
    assert carried_by(dropped) == ['top']


def test_a_broad_gain_is_not_flagged_as_carried():
    base = league({'top': 0., 'mid': 0.})
    candidate = league({'top': 1., 'mid': 1.})
    dropped = leave_one_out(base, candidate, RATINGS, today=TODAY)
    assert carried_by(dropped) == []


def test_a_regression_against_one_opponent_survives_a_positive_average():
    base = league({'top': .5, 'mid': .5})
    candidate = league({'top': 0., 'mid': 1.})
    delta = delta_win(base, candidate, RATINGS, today=TODAY)
    assert delta['strong']['delta_win'] == pytest.approx(0.)
    assert concentrated_regression(delta) == ['top']
