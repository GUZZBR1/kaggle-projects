"""Issue #22: per-day economics must reconcile with the audited game totals."""
import json

import pytest

from arena.match import run_match
from eval.metrics import daily_profile, reconcile, summarize
from eval.reports import write_report

FIELDS = ['day', 'turns', 'cash_start', 'cash_end', 'cash_min', 'revenue', 'sales', 'orders',
          'hands_mean', 'hands_peak', 'hires', 'plantings', 'harvests', 'pass_actions',
          'ineffective_actions', 'overflow_items', 'first_revenue_step', 'quadrants_end',
          'occupied_end', 'animals_end', 'shed_end', 'shed_peak', 'carried_peak',
          'shed_capacity', 'expenditure', 'unit_actions']


@pytest.fixture(scope='module')
def game():
    return run_match('challenger', 'animal', 37, 0)


def test_every_requested_field_is_present_for_every_day(game):
    assert game['telemetry_version'] == 1
    days = game['daily']
    assert [day['day'] for day in days] == list(range(30))
    for day in days:
        assert not set(FIELDS) - set(day)
    assert sum(day['turns'] for day in days) == game['steps']
    assert json.loads(json.dumps(game['daily'])), 'telemetry must serialize into the report'


def test_daily_rows_reconcile_with_the_final_metrics(game):
    assert reconcile(game) == []
    days = game['daily']
    assert days[-1]['cash_end'] == game['money']
    assert days[0]['cash_start'] == 3000
    revenue = {item: {'units': 0, 'revenue': 0} for item in game['sales']}
    for day in days:
        for item, sale in day['sales'].items():
            revenue[item]['units'] += sale['units']
            revenue[item]['revenue'] += sale['revenue']
    assert revenue == game['sales']


def test_cash_is_explained_by_revenue_minus_expenditure(game):
    for day in game['daily']:
        assert abs(day['cash_reconciliation_error']) < 1e-6
        assert day['cash_min'] <= min(day['cash_start'], day['cash_end'])
        for item, sale in day['sales'].items():
            assert sale['realized_price'] == sale['revenue'] / sale['units']


def test_market_orders_are_classified_by_what_executed(game):
    for day in game['daily']:
        orders = day['orders']
        total = sum(orders[k] for k in ('executed', 'failed', 'invalid', 'truncated') if k in orders)
        assert total == orders.get('requested', 0)


def test_the_opponent_is_measured_on_the_same_schema(game):
    assert [day['day'] for day in game['opponent_daily']] == [day['day'] for day in game['daily']]
    assert game['opponent_daily'][-1]['cash_end'] == game['opponent_money']


def test_telemetry_does_not_change_the_outcome():
    on = run_match('challenger', 'crop', 43, 1)
    off = run_match('challenger', 'crop', 43, 1, telemetry_enabled=False)
    for key in ('score', 'money', 'opponent_money', 'audit', 'sales', 'steps', 'failures'):
        assert on[key] == off[key]
    assert off['daily'] is None and off['telemetry_version'] is None


def test_reconcile_catches_a_corrupted_row(game):
    broken = dict(game, daily=[dict(day) for day in game['daily']])
    broken['daily'][-1] = dict(broken['daily'][-1], cash_end=-1)
    assert 'final cash disagrees' in reconcile(broken)
    assert reconcile(dict(game, daily=None)) == ['telemetry missing']


def test_the_profile_answers_the_liquidity_questions(game, tmp_path):
    rows = [dict(game, candidate='challenger')]
    profile = daily_profile(rows)
    assert profile['reconciliation_problems'] == []
    assert len(profile['days']) == 30
    assert profile['first_revenue_step']['mean'] >= 0
    assert profile['cash_floor']['min'] <= 3000

    summary = summarize(rows)
    assert summary['telemetry_version'] == 1
    write_report(tmp_path / 'report', rows, summary, {'candidate': 'challenger'})
    daily_csv = (tmp_path / 'report' / 'daily.csv').read_text()
    assert daily_csv.startswith('day,games,cash_end,cash_min,revenue')
    assert len(daily_csv.strip().splitlines()) == 31
    assert 'reconcile to the audited totals' in (tmp_path / 'report' / 'report.md').read_text()
