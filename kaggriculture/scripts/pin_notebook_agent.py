"""Extract a public notebook's agent verbatim and pin it under `opponents/public/`.

The panel is only worth what its provenance is worth, so extraction has to be mechanical
and repeatable rather than a hand-copied cell. Two shapes cover every artifact pinned so
far, and both are recognised here:

* a ``%%writefile main.py`` cell, whose body is the file byte for byte;
* a base64 (optionally gzip- or zlib-compressed) literal the notebook decodes into the
  source, which is how the larger agents keep the notebook readable.

Anything else - a notebook that builds its agent by running code, or one that needs a
native library compiled from sources it does not publish - is **not** provenance-complete
for us and is refused rather than approximated. `docs/PANEL_REFRESH.md` records the ones
refused and why.

    python scripts/pin_notebook_agent.py <user>/<kernel> --id <pin_id> [--dry-run]

The pin is written with its SHA-256 and a smoke game against the official starter agent;
a candidate that cannot play a full season is not pinned.
"""
import argparse
import base64
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
DECODERS = {'gzip': gzip.decompress, 'zlib': zlib.decompress, '': lambda blob: blob}


def pull(kernel, directory):
    subprocess.run(['kaggle', 'kernels', 'pull', kernel, '-p', directory, '-m'],
                   check=True, stdout=subprocess.DEVNULL)
    notebooks = sorted(Path(directory).glob('*.ipynb'))
    if notebooks:
        cells = json.loads(notebooks[0].read_text(encoding='utf-8'))['cells']
        return [''.join(cell['source']) for cell in cells if cell['cell_type'] == 'code']
    return [path.read_text(encoding='utf-8') for path in sorted(Path(directory).glob('*.py'))]


def from_writefile(cells):
    for cell in cells:
        if re.match(r'%%writefile\s+\S*main\.py\s*\n', cell):
            return cell.split('\n', 1)[1].encode()
    return None


def from_literal(cells):
    """A long base64 literal, decoded the way the notebook itself decodes it."""
    pattern = re.compile(r'(\w+)\s*=\s*(?:b?\'\'\'|b?"""|b?\'|b?")([A-Za-z0-9+/=\s]{2000,})')
    for cell in cells:
        for match in pattern.finditer(cell):
            name, payload = match.group(1), ''.join(match.group(2).split())
            try:
                blob = base64.b64decode(payload)
            except Exception:
                continue
            for label, decode in DECODERS.items():
                if label and f'{label}.decompress' not in cell:
                    continue
                try:
                    source = decode(blob)
                    compile(source, 'main.py', 'exec')
                    return source
                except Exception:
                    continue
    return None


def smoke(path, seed=314159):
    """A pin that cannot play a full season against the starter is not a pin."""
    result = subprocess.run(
        [str(ROOT / '.venv' / 'bin' / 'python'), '-m', 'arena.match',
         '--agent', f'clock::{path}', '--opponent', 'starter', '--seed', str(seed)],
        cwd=ROOT, check=True, capture_output=True, text=True)
    record = json.loads(result.stdout)
    if record['failures'] or record['steps'] < 719:
        raise RuntimeError(f'smoke game failed: {record["failures"]}')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('kernel', help='<user>/<kernel-slug>')
    parser.add_argument('--id', dest='pin', required=True, help='directory name under opponents/public')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as directory:
        cells = pull(args.kernel, directory)
    source = from_writefile(cells) or from_literal(cells)
    if source is None:
        print(f'{args.kernel}: no verbatim main.py found. Not provenance-complete; record the '
              f'refusal in docs/PANEL_REFRESH.md instead of approximating it.', file=sys.stderr)
        return 1
    compile(source, 'main.py', 'exec')
    digest = hashlib.sha256(source).hexdigest()
    print(f'{args.kernel}: {len(source)} bytes, sha256 {digest}')

    target = ROOT / 'opponents' / 'public' / args.pin / 'main.py'
    if args.dry_run:
        with tempfile.NamedTemporaryFile('wb', suffix='.py', delete=False) as handle:
            handle.write(source)
        record = smoke(handle.name)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source)
        record = smoke(target)
    print(f'smoke game vs starter: {record["money"]} to {record["opponent_money"]}, '
          f'{record["steps"]} steps, no failures')
    print('Now write main.manifest.json and the rating; see docs/PANEL_REFRESH.md.'
          if not args.dry_run else 'Dry run: nothing written.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
