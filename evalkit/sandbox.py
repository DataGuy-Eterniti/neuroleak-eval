"""Builds a fresh workspace per trial and runs a Python script inside it.

Each trial starts from a clean temporary directory containing only the task
data (never the hidden labels), so nothing leaks between trials.
Note: model-written code is executed with your Python. Run the eval inside a
disposable environment (GitHub Codespaces, Colab, Kaggle or a container).
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from .generators import GENERATORS


def build_workspace(task_id: str, seed: int | None = None):
    gen = GENERATORS[task_id]
    files, hidden = gen() if seed is None else gen(seed)
    ws = Path(tempfile.mkdtemp(prefix=f"{task_id}_"))
    for rel, df in files.items():
        path = ws / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(path, index=False)
    (ws / "output").mkdir()
    return ws, hidden


def run_script(code: str, workspace: Path, timeout: int = 600, args: list[str] | None = None) -> dict:
    script = workspace / "solution.py"
    script.write_text(code)
    try:
        p = subprocess.run([sys.executable, "-I", str(script), *(args or [])], cwd=workspace,
                           capture_output=True, text=True, timeout=timeout)
        return {"returncode": p.returncode, "stdout": p.stdout[-4000:],
                "stderr": p.stderr[-4000:], "timeout": False}
    except subprocess.TimeoutExpired:
        return {"returncode": -1, "stdout": "", "stderr": "TIMEOUT", "timeout": True}
