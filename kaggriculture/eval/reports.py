import csv
import html
import json
from pathlib import Path


def write_report(directory, rows, summary, metadata):
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=False)
    (path / 'matches.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
    (path / 'summary.json').write_text(json.dumps({'metadata': metadata, **summary}, indent=2) + '\n')
    fields = ['candidate', 'opponent', 'seed', 'seat', 'score', 'money', 'opponent_money', 'margin', 'steps', 'wall_seconds']
    with (path / 'matches.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)
    daily = summary.get('daily')
    if daily:
        columns = [k for k in daily['days'][0] if k not in ('orders', 'realized_price')]
        with (path / 'daily.csv').open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=columns, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(daily['days'])
    lines = ['# League report', '', f"Candidate: {metadata['candidate']}",
             f"Games: {summary['games']}; seed blocks: {summary['seed_blocks']}",
             f"Win/draw/loss: {summary['win_rate']:.1%} / {summary['draw_rate']:.1%} / {summary['loss_rate']:.1%}",
             f"Score: {summary['score_rate']:.1%}; seed-block CI95: {summary['score_ci95']}",
             f"Failures: {summary['failures']}; ineffective unit actions: {summary['no_effect_actions']}",
             f"Runtime (ms): {summary['runtime_ms']}", '',
             '| Opponent | Games | Score | CI95 | Mean margin |', '|---|---:|---:|---|---:|']
    for name, data in summary['per_opponent'].items():
        lines.append(f"| {name} | {data['games']} | {data['score_rate']:.1%} | {data['score_ci95']} | {data['mean_margin']:.0f} |")
    if daily:
        problems = daily['reconciliation_problems']
        lines += ['', '## Daily economics', '',
                  f"First revenue step: {daily['first_revenue_step']}",
                  f"Games that never sold: {daily['games_without_revenue']}",
                  f"Cash floor: {daily['cash_floor']}",
                  'Per-day aggregates reconcile to the audited totals.' if not problems
                  else f'RECONCILIATION FAILED ({len(problems)}); see summary.json.',
                  'Full per-day rows are in `daily.csv`.']
    (path / 'report.md').write_text('\n'.join(lines) + '\n')
    records = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(r[f]))}</td>' for f in fields) + '</tr>' for r in rows)
    page = '<!doctype html><meta charset="utf-8"><title>Kaggriculture league</title>'
    page += '<style>body{font:16px system-ui;margin:2rem;background:#f6f7f2;color:#17251a}td,th{padding:.5rem;border-bottom:1px solid #ccd}table{border-collapse:collapse}input{padding:.6rem}</style>'
    page += '<h1>Kaggriculture league</h1><pre>' + html.escape('\n'.join(lines[:8])) + '</pre>'
    page += '<label>Filter matches <input id="filter"></label><table><thead><tr>'
    page += ''.join('<th>' + f + '</th>' for f in fields) + '</tr></thead><tbody>' + records + '</tbody></table>'
    page += '<script>document.querySelector("#filter").oninput=e=>document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(e.target.value.toLowerCase()))</script>'
    (path / 'dashboard.html').write_text(page)
