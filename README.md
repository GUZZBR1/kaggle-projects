# Kaggriculture Lab

This repository is a reproducible strategy and evaluation lab for the Kaggle
Kaggriculture competition. A match has two players and runs for 30 in-game days
(720 turns). The project keeps policy development, local evaluation, reporting,
and submission packaging separate so that results can be traced to an exact
agent and environment.

## Quick start

Requirements:

- Python 3.12 or newer
- Bash and a POSIX runtime (Linux, macOS, or WSL)

```bash
git clone https://github.com/baskpascal/kaggle-projects.git
cd kaggle-projects/kaggriculture
bash scripts/setup.sh
source .venv/bin/activate
```

The setup script creates `.venv`, installs the locked dependencies, installs
`kaggle-environments==1.32.7` without its unrelated optional dependencies, and
prints the validated environment fingerprint. The runner deliberately rejects
a different package version or interpreter hash; results from a different game
engine are not comparable without revalidation.

All commands below assume that the current directory is `kaggriculture/` and
that the virtual environment is active. Native Windows is not currently
supported: the match deadline uses the POSIX-only `signal.SIGALRM`; use WSL
instead.

## Run one match

```bash
python -m arena.match \
  --candidate challenger \
  --opponent starter \
  --seed 123
```

The command prints a JSON result containing the score, money, margin, failures,
runtime, agent hashes, and environment fingerprint. The relevant defaults are
`challenger` versus `champion`, seed `123`, candidate seat `0`, and the `fast`
backend. Use `--seat 1` to swap seats, `--backend official` to drive the
official environment step-by-step, and `--replay replays/example.json` to keep
a turn transcript. `--agent` is an alias for `--candidate`.

Candidates and opponents may be built-in names (`starter`, `pass`, `random`,
`crop`, `animal`, `diversified`, `champion`, or `challenger`) or paths to Python
files that expose an `agent` callable. For example, the vendored `cok_v10`
benchmark is addressed by path, not by its manifest ID:

```bash
python -m arena.match \
  --candidate challenger \
  --opponent opponents/public/cok_v10/main.py \
  --seed 123
```

## Run a league

```bash
python -m arena.league \
  --candidate challenger \
  --opponents starter,crop,animal,diversified \
  --seeds 1000:1100 \
  --split dev \
  --workers 4 \
  --output experiments/results/challenger-dev
```

Seed ranges are half-open, so `1000:1100` contains 100 seeds. The league runs
both seats for every seed/opponent pair; the example above therefore runs
`100 * 4 * 2 = 800` games. Opponents are a comma-separated list. Seeds may be a
half-open range or a comma-separated list of unique integers.

`--output` is required and must name a directory that does not already exist.
The directory receives:

- `matches.jsonl` and `matches.csv`: per-game data
- `summary.json`: machine-readable metadata and aggregate metrics
- `report.md`: a compact human-readable report
- `dashboard.html`: a standalone, filterable match table

The league defaults to four workers, the `fast` backend, the `dev` split, seeds
`1000:1010`, and the four opponents shown above. It records both seats together
within each seed block when calculating confidence intervals.

## Seed discipline

The ranges in [`config.yaml`](kaggriculture/config.yaml) are experimental
boundaries, not interchangeable pools:

| Split | Range | Intended use |
| --- | --- | --- |
| Development | `1000:1100` | Frequent iteration and tuning |
| Validation | `100000:100200` | Occasional promotion checks, not tuning |
| Holdout | starts at `9000000` | One new, disjoint allocation per release |

Treat a validation or holdout range as consumed after inspecting its results.
Do not tune against individual seeds or move failed validation seeds into the
development set. Record the exact holdout allocation with the release so it is
never silently reused.

This discipline is currently enforced by convention: `config.yaml` is not
loaded automatically by the CLI, and `--split` only labels report metadata. It
does not select or validate `--seeds`. The CLI accepts `dev` and `validation`
labels only; holdout allocation belongs to the release procedure.

## Build and preflight a submission

```bash
python -m submission.build
python -m submission.preflight submission/dist/main.py
```

The build produces three files:

- `submission/dist/main.py`: the standalone, standard-library-only agent
- `submission/dist/main.manifest.json`: its digest, effective parameters, and
  component source hashes
- `submission/dist/main.tar.gz`: a reproducible archive with `main.py` at its
  root

Parameter overrides can be supplied as a JSON object with `--params FILE`, and
the staging path can be changed with `--output PATH`. Unknown parameter names
are rejected. The builder also refuses to overwrite an existing, different
`main.py`.

Preflight must receive the generated Python file as its positional argument.
It exercises Kaggle's actual file loader in self-play, using seed `314159`, and
requires both agents to finish without trace errors across all 720 states. It
also checks the 100 MiB file limit and reports the artifact and environment
hashes. `--output FILE` optionally saves that result as JSON.

Preflight does not inspect `main.tar.gz` or compare the manifest automatically;
it validates `main.py`. Submit the archive only after its corresponding Python
file passes.

## Architecture

| Layer | Responsibility |
| --- | --- |
| [`agent/`](kaggriculture/agent/) | Policy, state model, economics, routing, planning, and parameters |
| [`arena/`](kaggriculture/arena/) | Agent loading, pinned engine access, matches, leagues, parallelism, and seeds |
| [`eval/`](kaggriculture/eval/) | Seed-blocked metrics and report generation |
| [`submission/`](kaggriculture/submission/) | Single-file packaging and real-loader preflight |

[`opponents/`](kaggriculture/opponents/) contains benchmark agents and their
provenance. [`versions/`](kaggriculture/versions/) contains frozen release
artifacts; neither directory is part of the four-layer implementation flow.

## Immutable releases

Build into `submission/dist/`, run preflight there, and then create a new
`versions/vNNN/` directory containing the matching `main.py`, manifest, and
archive. Never edit or rebuild an existing version directory. A new policy,
parameter set, or source state requires a new version.

The manifest records the SHA-256 of the generated source, the complete effective
parameter set, and a SHA-256 for every source module folded into `main.py`. Given
a trusted manifest, those values detect policy or parameter drift. They do not
authenticate authorship, hash the tar archive, or freeze the Kaggle runtime;
the environment fingerprint reported by setup, matches, and preflight covers
the runtime separately. Generate and verify release artifacts in the POSIX
workspace because line-ending conversion can change a checkout's raw byte hash.

## Third-party benchmark

[`opponents/public/cok_v10`](kaggriculture/opponents/public/cok_v10/) is retained
for benchmark evaluation only and is not included by the submission builder.
Its provenance record credits
[`COK-ZhangZiliang/Kaggriculture`](https://github.com/COK-ZhangZiliang/Kaggriculture)
at commit
[`7ef67eac`](https://github.com/COK-ZhangZiliang/Kaggriculture/commit/7ef67eac458cd9ecd13786063e2e581fbe7403ec),
with the pinned artifact hash in
[`opponents/manifest.json`](kaggriculture/opponents/manifest.json). The retained
material is Apache-2.0 licensed; see its
[`LICENSE`](kaggriculture/opponents/public/cok_v10/LICENSE) and detailed
[`THIRD_PARTY_NOTICES.md`](kaggriculture/opponents/public/cok_v10/THIRD_PARTY_NOTICES.md).

## Tests

```bash
python -m pytest
```
