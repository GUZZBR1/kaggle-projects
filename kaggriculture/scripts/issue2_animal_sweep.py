"""Evaluate animal target/type combinations against the v000 league opponents."""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from arena.league import run_league
from arena.seeds import parse_seeds
from submission.build import build


ANIMAL_TYPES = ("GOOSE", "COW", "SHEEP")
ANIMAL_TARGETS = (0, 3, 6, 9)
OPPONENTS = (
    "starter",
    "crop",
    "animal",
    "diversified",
    "opponents/public/cok_v10/main.py",
)


def slug(animal_type: str, target: int) -> str:
    return f"{animal_type.lower()}-{target}"


def run_sweep(seeds: list[int], workers: int, artifact_dir: Path) -> list[dict]:
    results = []
    for target, animal_type in product(ANIMAL_TARGETS, ANIMAL_TYPES):
        name = slug(animal_type, target)
        artifact = artifact_dir / f"issue2-{name}.py"
        build(artifact, {"animal_target": target, "animal_type": animal_type})
        _, summary, _ = run_league(
            str(artifact), list(OPPONENTS), seeds, workers=workers, split="dev"
        )
        results.append(
            {
                "animal_type": animal_type,
                "animal_target": target,
                "score_rate": summary["score_rate"],
                "score_ci95": summary["score_ci95"],
                "mean_margin": summary["mean_margin"],
                "failures": summary["failures"],
                "opponent_failures": summary["opponent_failures"],
                "per_opponent": summary["per_opponent"],
                "artifact": str(artifact),
            }
        )
        print(
            f"{name}: score={summary['score_rate']:.1%} "
            f"CI95={summary['score_ci95']} margin={summary['mean_margin']:.0f}",
            flush=True,
        )
    return results


def write_report(output: Path, seeds: list[int], workers: int, results: list[dict]) -> None:
    output.mkdir(parents=True, exist_ok=False)
    payload = {
        "candidate": "current agent with animal parameter overrides",
        "opponents": list(OPPONENTS),
        "seeds": seeds,
        "seed_blocks": len(seeds),
        "workers": workers,
        "results": results,
    }
    (output / "summary.json").write_text(json.dumps(payload, indent=2) + "\n")
    ranked = sorted(results, key=lambda row: (row["score_rate"], row["mean_margin"]), reverse=True)
    lines = [
        "# Animal strategy sweep",
        "",
        "Current policy variants were evaluated against the immutable v000 opponent set.",
        "",
        f"Games per configuration: {len(seeds) * len(OPPONENTS) * 2}",
        f"Seed blocks: {len(seeds)}",
        "",
        "| Rank | Animal | Target | Score | CI95 | Mean margin | Failures |",
        "|---:|---|---:|---:|---|---:|---:|",
    ]
    for rank, row in enumerate(ranked, 1):
        lines.append(
            f"| {rank} | {row['animal_type']} | {row['animal_target']} | "
            f"{row['score_rate']:.1%} | {row['score_ci95']} | "
            f"{row['mean_margin']:.0f} | {row['failures']} |"
        )
    lines.extend(
        [
            "",
            "The winner is selected by score rate, with mean margin used only as a tie-breaker.",
            "The sweep does not change the immutable `versions/v000` artifact.",
        ]
    )
    (output / "report.md").write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", default="1000:1100")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--output", default="experiments/results/issue2-animal-sweep")
    parser.add_argument("--artifacts", default="submission/dist")
    args = parser.parse_args()
    seeds = parse_seeds(args.seeds)
    results = run_sweep(seeds, args.workers, Path(args.artifacts))
    write_report(Path(args.output), seeds, args.workers, results)


if __name__ == "__main__":
    main()
