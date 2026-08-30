"""manual_label — show each stripped chart, take g/b, score the operator (milestone 0).

Resumable: answers append to reports/charts/answers.jsonl; rerunning continues
where you stopped. Charts open in Preview and are closed after each answer.
"""

from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path

from pumpfun.config import Config
from pumpfun.reports import write_json

log = logging.getLogger(__name__)


def _show(path: Path) -> None:
    subprocess.run(["open", "-a", "Preview", str(path)], check=False)


def _close_preview() -> None:
    subprocess.run(["osascript", "-e", 'tell application "Preview" to close front window'], check=False, capture_output=True)


def score(manifest: list[dict], answers: dict[int, int]) -> dict:
    rows = [(m["label"], answers[m["chart_id"]], m["in_zone"]) for m in manifest if m["chart_id"] in answers]

    def stats(rs: list[tuple[int, int, bool]]) -> dict:
        tp = sum(1 for y, p, _ in rs if y == 1 and p == 1)
        fp = sum(1 for y, p, _ in rs if y == 0 and p == 1)
        fn = sum(1 for y, p, _ in rs if y == 1 and p == 0)
        tn = sum(1 for y, p, _ in rs if y == 0 and p == 0)
        n = len(rs)
        return {
            "n": n,
            "accuracy": (tp + tn) / n if n else None,
            "precision": tp / (tp + fp) if tp + fp else None,
            "recall": tp / (tp + fn) if tp + fn else None,
            "confusion": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
        }

    return {"all": stats(rows), "zone": stats([r for r in rows if r[2]]), "answered": len(rows), "total": len(manifest)}


def run(cfg: Config) -> None:
    out = cfg.reports_dir / "charts"
    manifest = json.loads((out / "manifest.json").read_text())
    log_path = out / "answers.jsonl"
    answers: dict[int, int] = {}
    if log_path.exists():
        for line in log_path.read_text().splitlines():
            if line.strip():
                d = json.loads(line)
                answers[int(d["chart_id"])] = int(d["pred"])
    todo = [m for m in manifest if m["chart_id"] not in answers]
    print(f"{len(answers)} answered, {len(todo)} to go. Keys: g = goes, b = does not, q = quit (resume later)")
    with log_path.open("a") as f:
        for m in todo:
            path = out / f"{m['chart_id']:03d}.png"
            _show(path)
            while True:
                ans = input(f"[{len(answers) + 1}/{len(manifest)}] g/b? ").strip().lower()
                if ans in ("g", "b", "q"):
                    break
            _close_preview()
            if ans == "q":
                break
            pred = 1 if ans == "g" else 0
            answers[m["chart_id"]] = pred
            f.write(json.dumps({"chart_id": m["chart_id"], "pred": pred}) + "\n")
            f.flush()
    result = score(manifest, answers)
    if result["answered"] == result["total"]:
        write_json(cfg.reports_dir / "human_benchmark.json", result)
        log.info("human benchmark -> %s", cfg.reports_dir / "human_benchmark.json")
    print(json.dumps(result, indent=1))
