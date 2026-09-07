"""Fail when the latest Kaggle interpreter differs from the validated lock."""

from __future__ import annotations

import hashlib
from importlib import metadata
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from arena.engine import INTERPRETER_HASH, VERSION  # noqa: E402


PACKAGE = "kaggle-environments"
INTERPRETER_PATH = Path(
    "kaggle_environments/envs/kaggriculture/kaggriculture.py"
)


def installed_fingerprint(
    distribution: metadata.Distribution | None = None,
) -> tuple[str, str]:
    """Return version and interpreter digest without importing the package."""
    distribution = distribution or metadata.distribution(PACKAGE)
    interpreter = Path(distribution.locate_file(INTERPRETER_PATH))
    if not interpreter.is_file():
        raise RuntimeError(f"Kaggriculture interpreter not found: {interpreter}")
    digest = hashlib.sha256(interpreter.read_bytes()).hexdigest()
    return distribution.version, digest


def check_environment(
    distribution: metadata.Distribution | None = None,
) -> tuple[str, str]:
    """Raise when the installed environment no longer matches arena.engine."""
    version, digest = installed_fingerprint(distribution)
    if version != VERSION or digest != INTERPRETER_HASH:
        raise RuntimeError(
            "Environment mismatch: "
            f"version={version}, sha256={digest}; revalidate before changing lock"
        )
    return version, digest


def main() -> None:
    version, digest = check_environment()
    print(f"Environment lock is current: version={version}, sha256={digest}")


if __name__ == "__main__":
    main()
