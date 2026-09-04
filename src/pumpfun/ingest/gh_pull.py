"""gh_pull — bring the GitHub Actions fetchers' output home.

Each workflow run uploads one artifact per shard holding that shard's cache
files and ledger. This downloads them with `gh`, copies tapes into
data/raw/cache (never overwriting a newer local file) and merges the shard
ledgers into the main ledger.
"""

from __future__ import annotations

import json
import logging
import shutil
import sqlite3
import subprocess
from pathlib import Path

from pumpfun.config import Config
from pumpfun.ingest.fetch_trades import LEDGER_DDL

log = logging.getLogger(__name__)


def _gh(*args: str) -> str:
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"gh {' '.join(args)} failed: {r.stderr.strip()}")
    return r.stdout


def recent_run_ids(limit: int, repo: str | None = None) -> list[int]:
    """Completed runs, newest first. A run whose one shard lost its runner is 'failure' as a whole while the
    other shards' artifacts are intact, so failed runs are pulled too; missing artifacts are just skipped."""
    ids: list[tuple[int, str]] = []
    for status in ("success", "failure"):
        args = ["run", "list", "--workflow", "fetch.yml", "--status", status, "--limit", str(limit), "--json", "databaseId,createdAt"]
        if repo:
            args += ["-R", repo]
        ids += [(int(r["databaseId"]), str(r["createdAt"])) for r in json.loads(_gh(*args))]
    ids.sort(key=lambda t: t[1], reverse=True)
    return [i for i, _ in ids[:limit]]


def merge_ledger(main: Path, incoming: Path) -> int:
    con = sqlite3.connect(main)
    con.execute(LEDGER_DDL)
    con.execute("attach database ? as inc", (str(incoming),))
    n = con.execute(
        """
        insert or replace into fetch
        select i.* from inc.fetch i
          left join fetch m on m.mint = i.mint
         where m.mint is null or i.fetched_at >= m.fetched_at
        """
    ).rowcount
    con.commit()
    con.execute("detach database inc")
    con.close()
    return n


def merge_dir(cfg: Config, root: Path) -> tuple[int, int]:
    tapes = 0
    rows = 0
    for f in root.rglob("*.json.gz"):
        dst = cfg.trade_cache_dir / f.name[:2] / f.name
        if dst.exists() and dst.stat().st_mtime >= f.stat().st_mtime:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dst)
        tapes += 1
    for f in root.rglob("fetch_ledger*.sqlite"):
        rows += merge_ledger(cfg.ledger_path, f)
    return tapes, rows


def run(cfg: Config, run_ids: list[int], limit: int, repo: str | None = None) -> None:
    ids = run_ids or recent_run_ids(limit, repo)
    if not ids:
        log.info("no successful fetch runs found")
        return
    dl_root = cfg.data_dir / "gh"
    for rid in ids:
        dst = dl_root / str(rid)
        if dst.exists():
            log.info("run %d already downloaded", rid)
        else:
            dst.mkdir(parents=True, exist_ok=True)
            dl = ["run", "download", str(rid), "-D", str(dst)]
            if repo:
                dl += ["-R", repo]
            _gh(*dl)
        tapes, rows = merge_dir(cfg, dst)
        log.info("run %d: merged %d tapes, %d ledger rows", rid, tapes, rows)
        for rep in dst.rglob("cost_probe.json"):
            log.info("cost probe from run %d:\n%s", rid, rep.read_text())
    write_done_list(cfg)


def write_done_list(cfg: Config) -> int:
    """data/queue/done.parquet — every mint the Mac already holds; runners skip these whatever the shard count."""
    import polars as pl

    con = sqlite3.connect(cfg.ledger_path)
    mints = [r[0] for r in con.execute("select mint from fetch where status in ('ok','empty')")]
    con.close()
    out = cfg.data_dir / "queue" / "done.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    pl.DataFrame({"mint": mints}, schema={"mint": pl.String}).write_parquet(out)
    log.info("done list: %d mints -> %s", len(mints), out)
    return len(mints)
