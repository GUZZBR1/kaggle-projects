"""Run the read-only release dossier from the project directory."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval.dossier import main

if __name__ == '__main__':
    main()
