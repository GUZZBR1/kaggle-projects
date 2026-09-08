import argparse
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path

from arena.engine import fingerprint, make_environment

STARTING_CAPITAL = 3000


def liveness(steps, seat):
    """Prove the artifact actually plays, not just that it loads without error.

    A submission whose policy raises on every turn still completes 720 states:
    the wrapper swallows the exception and emits PASS. It looks identical to a
    healthy run in every check above, then plays PASS for the whole season on
    the ladder and keeps doing so until the competition ends. The Kaggriculture
    community has already lost submissions to exactly this, so the artifact has
    to demonstrate action, not merely survival.
    """
    farmer, hands, orders, idle, worst_idle = [], 0, 0, 0, 0
    for step in steps[1:]:
        action = step[seat].get('action') or {}
        head = action.get('farmer') or ['PASS']
        farmer.append(head[0] if isinstance(head, list) and head else 'PASS')
        units = [u for u in (action.get('hands') or []) if isinstance(u, list) and u and u[0] != 'PASS']
        slots = [o for o in (action.get('market') or []) if isinstance(o, list) and o]
        hands += len(units)
        orders += len(slots)
        if farmer[-1] == 'PASS' and not units and not slots:
            idle += 1
            worst_idle = max(worst_idle, idle)
        else:
            idle = 0
    acting = sum(1 for a in farmer if a != 'PASS')
    return {'turns': len(farmer), 'farmer_actions': acting,
            'farmer_action_rate': acting / len(farmer) if farmer else 0.,
            'first_farmer_action': farmer[0] if farmer else None,
            'first_acting_turn': next((i for i, a in enumerate(farmer) if a != 'PASS'), None),
            'hand_actions': hands, 'market_orders': orders,
            'longest_idle_streak': worst_idle,
            'distinct_farmer_actions': len(set(farmer))}


def check_liveness(report, reward, min_action_rate, max_idle_streak):
    problems = []
    if report['turns'] != 719:
        problems.append(f"policy ran {report['turns']} turns, expected 719")
    if report['first_acting_turn'] is None:
        problems.append('never took a farmer action: PASS-only artifact')
    if report['farmer_action_rate'] < min_action_rate:
        problems.append(f"farmer acted on {report['farmer_action_rate']:.1%} of turns, "
                        f'below the {min_action_rate:.0%} floor')
    if not report['market_orders']:
        problems.append('never issued a market order')
    if reward == STARTING_CAPITAL:
        problems.append(f'final money is exactly the starting capital {STARTING_CAPITAL}: '
                        'the season produced nothing')
    if report['longest_idle_streak'] > max_idle_streak:
        problems.append(f"idle for {report['longest_idle_streak']} consecutive turns, "
                        f'above the {max_idle_streak} limit')
    return problems


def preflight(path, seed=314159, min_action_rate=.05, max_idle_streak=72):
    path = Path(path).resolve()
    if path.stat().st_size > 100 * 1024 * 1024:
        raise ValueError('Submission exceeds 100 MiB')
    env = make_environment(seed)
    # Exercise Kaggle's actual file loader and callback wrapper, including config handling.
    with redirect_stdout(io.StringIO()) as logs:
        env.run([str(path), str(path)])
    failures = [s.status for s in env.state if s.status != 'DONE']
    trace_errors = [entry for turn in env.logs for entry in turn if entry.get('error')]
    if failures or trace_errors or len(env.steps) != 720:
        raise RuntimeError(f'Preflight failed: statuses={failures}, errors={trace_errors[:2]}, {logs.getvalue()[-2000:]}')
    rewards = [s.reward for s in env.state]
    reports = [liveness(env.steps, seat) for seat in (0, 1)]
    problems = {seat: check_liveness(reports[seat], rewards[seat], min_action_rate, max_idle_streak)
                for seat in (0, 1)}
    if any(problems.values()):
        raise RuntimeError(f'Preflight failed on liveness: {json.dumps(problems)}')
    return {'artifact': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'environment': fingerprint(), 'seed': seed, 'states': len(env.steps),
            'rewards': rewards, 'liveness': reports, 'status': 'PASSED'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--output')
    parser.add_argument('--min-action-rate', type=float, default=.05)
    parser.add_argument('--max-idle-streak', type=int, default=72)
    args = parser.parse_args()
    result = preflight(args.path, min_action_rate=args.min_action_rate,
                       max_idle_streak=args.max_idle_streak)
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
