import os
from datetime import datetime
from typing import Optional

# Internal state for per-run output directory management
_RUN_OUT_DIR: Optional[str] = None


def project_root() -> str:
    """Return the absolute path to the project root (directory containing this repository)."""
    # This file is in <root>/agent/run_dir.py
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


def ensure_run_dir() -> str:
    """Create (once) and return the path to the per-run output directory under <root>/out/<timestamp>.

    The directory name is controlled by the tool and is not configurable by the agent.
    """
    global _RUN_OUT_DIR
    if _RUN_OUT_DIR is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_out = os.path.join(project_root(), "out")
        os.makedirs(base_out, exist_ok=True)
        run_dir = os.path.join(base_out, timestamp)
        # If a folder with the same name exists (unlikely), derive a unique suffix
        suffix = 1
        unique_dir = run_dir
        while os.path.exists(unique_dir):
            suffix += 1
            unique_dir = f"{run_dir}_{suffix}"
        os.makedirs(unique_dir, exist_ok=True)
        _RUN_OUT_DIR = unique_dir
    return _RUN_OUT_DIR
