"""reports — small helpers for the JSON artefacts every stage leaves behind."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + "\n")


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text())


def update_counts(reports_dir: Path, stage: str, counts: dict[str, Any]) -> None:
    """Merge one stage's drop counts into reports/filter_counts.json (spec §7: log exactly what was dropped)."""
    path = reports_dir / "filter_counts.json"
    cur = read_json(path, {}) or {}
    cur[stage] = {**counts, "updated_at": int(time.time())}
    write_json(path, cur)
