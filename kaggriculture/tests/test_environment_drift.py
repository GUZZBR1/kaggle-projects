from pathlib import Path

import pytest

from arena.engine import VERSION
from scripts.check_environment import INTERPRETER_PATH, check_environment


class FakeDistribution:
    def __init__(self, version: str, interpreter: Path) -> None:
        self.version = version
        self.interpreter = interpreter

    def locate_file(self, path: Path) -> Path:
        assert path == INTERPRETER_PATH
        return self.interpreter


def test_changed_interpreter_hash_is_rejected(tmp_path: Path) -> None:
    interpreter = tmp_path / "kaggriculture.py"
    interpreter.write_text("# simulated upstream change\n")
    distribution = FakeDistribution(VERSION, interpreter)

    with pytest.raises(RuntimeError, match=r"Environment mismatch: .*sha256="):
        check_environment(distribution)
