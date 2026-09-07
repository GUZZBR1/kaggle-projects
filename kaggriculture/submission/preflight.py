import argparse
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path

from arena.engine import fingerprint, make_environment


def preflight(path, seed=314159):
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
    return {'artifact': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'environment': fingerprint(), 'seed': seed, 'states': len(env.steps),
            'rewards': [s.reward for s in env.state], 'status': 'PASSED'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = preflight(args.path)
    if args.output:
        Path(args.output).write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
