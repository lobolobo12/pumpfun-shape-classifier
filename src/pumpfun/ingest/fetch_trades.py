"""fetch_trades — walk the queue, one tape per coin, resumable.

State lives in two places so a run that dies at hour 6 restarts where it stopped:
  data/raw/cache/<xx>/<mint>.json.gz   the tape (same JSON shape as the trading repo's cache)
  data/raw/fetch_ledger.sqlite         one row per attempted mint

Host policy: `mac` shares the IP with the live attention collector and refuses
to run while the repo's holder-shape fetcher is up (unless --force); `vps` uses
its own budget. `--probe N` fetches a seeded random N and writes
reports/cost_probe.json — the numbers that size the full run.
"""

from __future__ import annotations

import gzip
import json
import logging
import random
import sqlite3
import subprocess
import time
import zlib
from pathlib import Path

import polars as pl

from pumpfun.config import Config
from pumpfun.ingest.swap_api import Anchor, SwapApiClient, TradeFile
from pumpfun.reports import read_json, write_json

log = logging.getLogger(__name__)

LEDGER_DDL = """
create table if not exists fetch (
  mint text primary key,
  status text not null,           -- ok | empty | error
  pages integer not null,
  requests integer not null,
  trades integer not null,
  complete integer not null,
  until_ms integer not null,
  fetched_at integer not null,
  error text
)
"""


class Ledger:
    def __init__(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.con = sqlite3.connect(path)
        self.con.execute(LEDGER_DDL)
        self.con.commit()

    def done(self) -> set[str]:
        return {r[0] for r in self.con.execute("select mint from fetch where status in ('ok','empty')")}

    def ok_mints(self) -> list[str]:
        return [r[0] for r in self.con.execute("select mint from fetch where status = 'ok' order by mint")]

    def mark(  # noqa: PLR0913
        self,
        mint: str,
        status: str,
        pages: int,
        requests: int,
        trades: int,
        complete: bool,
        until_ms: int,
        error: str | None = None,
    ) -> None:
        self.con.execute(
            "insert or replace into fetch values (?,?,?,?,?,?,?,?,?)",
            (mint, status, pages, requests, trades, int(complete), until_ms, int(time.time()), error),
        )
        self.con.commit()

    def summary(self) -> dict[str, int]:
        return {s: n for s, n in self.con.execute("select status, count(*) from fetch group by status")}

    def close(self) -> None:
        self.con.close()


def cache_path(cfg: Config, mint: str) -> Path:
    return cfg.trade_cache_dir / mint[:2] / f"{mint}.json.gz"


def load_cached(cfg: Config, mint: str) -> TradeFile | None:
    p = cache_path(cfg, mint)
    if not p.exists():
        return None
    with gzip.open(p, "rt") as f:
        return TradeFile.from_json(json.load(f))


def save_cached(cfg: Config, tf: TradeFile) -> None:
    p = cache_path(cfg, tf.mint)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    with gzip.open(tmp, "wt") as f:
        json.dump(tf.to_json(), f)
    tmp.replace(p)


def study_fetcher_running() -> bool:
    r = subprocess.run(["pgrep", "-f", "holder-shape-study"], capture_output=True, text=True)
    return r.returncode == 0 and r.stdout.strip() != ""


def _cursor_ms(cursor: str | None) -> int | None:
    if not cursor or "-" not in cursor:
        return None
    try:
        return int(cursor.rsplit("-", 1)[1])
    except ValueError:
        return None


def import_seed(cfg: Config, queue: pl.DataFrame, ledger: Ledger) -> int:
    """Adopt the trading repo's cached tapes when they already cover our horizon."""
    src = cfg.sources.seed_trade_cache
    if not src.is_dir():
        return 0
    until = dict(queue.select("mint", "until_ms").iter_rows())
    done = ledger.done()
    n = 0
    for f in src.glob("*.json"):
        mint = f.stem
        if mint not in until or mint in done:
            continue
        d = json.loads(f.read_text())
        if not d.get("complete"):
            continue
        covered_to = _cursor_ms(d.get("startCursor")) or int(d.get("fetchedAt", 0))
        if covered_to < until[mint]:
            continue
        tf = TradeFile.from_json(d)
        save_cached(cfg, tf)
        ledger.mark(mint, "ok" if tf.trades else "empty", tf.pages, 0, len(tf.trades), True, until[mint])
        n += 1
    return n


def _window_trades(tf: TradeFile, launch_ms: int, window_s: int) -> int:
    end = launch_ms + window_s * 1000
    return sum(1 for t in tf.trades if t.at_ms < end)


def shard_of(mint: str, n: int) -> int:
    return zlib.crc32(mint.encode()) % n


def ledger_path(cfg: Config, shard: tuple[int, int] | None) -> Path:
    if shard is None:
        return cfg.ledger_path
    return cfg.ledger_path.with_name(f"fetch_ledger.shard{shard[0]}of{shard[1]}.sqlite")


def run(  # noqa: PLR0913
    cfg: Config,
    host: str,
    probe_n: int | None = None,
    force: bool = False,
    limit: int | None = None,
    do_import_seed: bool = False,
    shard: tuple[int, int] | None = None,
    max_seconds: float | None = None,
    rps: float | None = None,
    queue_path: Path | None = None,
) -> dict:
    if host == "mac":
        rps = rps or cfg.swap_api.rps_mac
        if study_fetcher_running() and not force:
            raise SystemExit("holder-shape-study.ts is running on this IP; wait for it or pass --force (and lower --rps)")
    elif host == "vps":
        rps = rps or cfg.swap_api.rps_vps
    else:
        raise SystemExit(f"unknown host {host!r}")

    queue = pl.read_parquet(queue_path or (cfg.interim_dir / "fetch_queue.parquet"))
    if shard is not None:
        i, n = shard
        queue = queue.filter(pl.col("mint").map_elements(lambda m: shard_of(m, n) == i, return_dtype=pl.Boolean))
    ledger = Ledger(ledger_path(cfg, shard))
    if do_import_seed:
        n = import_seed(cfg, queue, ledger)
        log.info("imported %d seed tapes from %s", n, cfg.sources.seed_trade_cache)
    done = ledger.done()
    done_file = cfg.data_dir / "queue" / "done.parquet"
    if done_file.exists():
        done |= set(pl.read_parquet(done_file)["mint"].to_list())
    # Newest launches first: the most decision-relevant data lands before the deep history.
    todo = queue.filter(~pl.col("mint").is_in(list(done))).sort("launch_time_ms", descending=True)
    if probe_n:
        rnd = random.Random(cfg.seed)
        idx = sorted(rnd.sample(range(todo.height), min(probe_n, todo.height)))
        todo = todo[idx]
    if limit:
        todo = todo.head(limit)
    log.info(
        "fetch: host=%s rps=%.2f shard=%s queue=%d done=%d todo=%d budget=%s",
        host,
        rps,
        shard,
        queue.height,
        len(done),
        todo.height,
        f"{max_seconds:.0f}s" if max_seconds else "none",
    )

    client = SwapApiClient(cfg.swap_api, rps=rps)
    anchor: Anchor | None = None
    # A fresh (slot, time) pair from the most recently launched coin in the queue.
    if queue.height:
        newest_mint, newest_ms = queue.sort("launch_time_ms", descending=True).select("mint", "launch_time_ms").row(0)
        t = client.newest(newest_mint, newest_ms)
        if t:
            anchor = Anchor(slot=t.slot, at_ms=t.at_ms)
            log.info("anchor from %s: slot %d at %d", newest_mint[:8], t.slot, t.at_ms)

    per_coin: list[dict] = []
    t0 = time.monotonic()
    req0 = client.stats.requests
    try:
        work = todo.select("mint", "launch_time_ms", "launch_day", "until_ms").iter_rows()
        for i, (mint, launch_ms, _day, until_ms) in enumerate(work):
            if max_seconds is not None and time.monotonic() - t0 > max_seconds:
                log.info("time budget reached after %d coins; stopping (resumable)", i)
                break
            r0 = client.stats.requests
            try:
                tf = client.fetch_tape(mint, created_ms=int(launch_ms), until_ms=int(until_ms), anchor=anchor)
            except Exception as e:  # noqa: BLE001 — keep walking, the ledger records it
                log.exception("fetch failed for %s", mint)
                ledger.mark(mint, "error", 0, client.stats.requests - r0, 0, False, int(until_ms), error=repr(e))
                continue
            reqs = client.stats.requests - r0
            if tf.trades:
                save_cached(cfg, tf)
                newest = max(tf.trades, key=lambda t: t.at_ms)
                if anchor is None or newest.at_ms > anchor.at_ms:
                    anchor = Anchor(slot=newest.slot, at_ms=newest.at_ms)
            ledger.mark(mint, "ok" if tf.trades else "empty", tf.pages, reqs, len(tf.trades), tf.complete, int(until_ms))
            per_coin.append(
                {
                    "mint": mint,
                    "pages": tf.pages,
                    "requests": reqs,
                    "trades": len(tf.trades),
                    "complete": tf.complete,
                    "trades_in_window": _window_trades(tf, int(launch_ms), cfg.window_seconds),
                    "programs": sorted({t.program for t in tf.trades}),
                }
            )
            if (i + 1) % 25 == 0:
                el = time.monotonic() - t0
                rq = client.stats.requests - req0
                log.info(
                    "%d/%d coins, %d req, %.2f req/s, 429s=%d, gap=%.2fs",
                    i + 1,
                    todo.height,
                    rq,
                    rq / max(el, 1e-9),
                    client.stats.http_429,
                    client.gap_seconds,
                )
    finally:
        client.close()
        elapsed = time.monotonic() - t0
        summary = {
            "host": host,
            "shard": None if shard is None else f"{shard[0]}/{shard[1]}",
            "rps_configured": rps,
            "coins_attempted": len(per_coin),
            "elapsed_s": round(elapsed, 1),
            "requests": client.stats.requests - req0,
            "req_per_s": round((client.stats.requests - req0) / max(elapsed, 1e-9), 3),
            "http_429": client.stats.http_429,
            "http_other": client.stats.http_other,
            "network_err": client.stats.network_err,
            "bytes": client.stats.bytes,
            "ledger": ledger.summary(),
        }
        ledger.close()
        runs = read_json(cfg.reports_dir / "fetch_runs.json", []) or []
        runs.append({**summary, "at": int(time.time())})
        write_json(cfg.reports_dir / "fetch_runs.json", runs)
        if probe_n and per_coin:
            _write_probe(cfg, summary, per_coin, queue.height - len(done))
    return summary


def _write_probe(cfg: Config, summary: dict, per_coin: list[dict], remaining: int) -> None:
    n = len(per_coin)
    reqs = sum(c["requests"] for c in per_coin)
    pages = sum(c["pages"] for c in per_coin)
    trades = sum(c["trades"] for c in per_coin)
    with_min = sum(1 for c in per_coin if c["trades_in_window"] >= cfg.min_trades_in_window)
    pool = sum(1 for c in per_coin if any(p != "pump" for p in c["programs"]))
    incomplete = sum(1 for c in per_coin if not c["complete"])
    req_per_coin = reqs / n
    probe = {
        "coins": n,
        "requests_per_coin": round(req_per_coin, 3),
        "pages_per_coin": round(pages / n, 3),
        "trades_per_coin": round(trades / n, 1),
        "bytes_per_coin": round(summary["bytes"] / n),
        "share_ge_min_trades_in_window": round(with_min / n, 4),
        "share_reaching_pool": round(pool / n, 4),
        "share_incomplete": round(incomplete / n, 4),
        "measured_req_per_s": summary["req_per_s"],
        "http_429": summary["http_429"],
        "remaining_queue": remaining,
        "projected_requests_remaining": round(req_per_coin * remaining),
        "projected_hours_at_measured_rate": round(req_per_coin * remaining / max(summary["req_per_s"], 1e-9) / 3600, 1),
        "projected_hours_at_vps_rps": round(req_per_coin * remaining / cfg.swap_api.rps_vps / 3600, 1),
        "trades_in_window_hist": _hist([c["trades_in_window"] for c in per_coin], [0, 1, 5, 10, 25, 50, 100, 250, 1000]),
    }
    write_json(cfg.reports_dir / "cost_probe.json", probe)
    log.info("cost probe -> %s", cfg.reports_dir / "cost_probe.json")
    for k, v in probe.items():
        if k != "trades_in_window_hist":
            log.info("  %s: %s", k, v)


def _hist(xs: list[int], edges: list[int]) -> dict[str, int]:
    out: dict[str, int] = {}
    for lo, hi in zip(edges, edges[1:] + [None], strict=False):
        key = f"{lo}-{hi - 1}" if hi else f"{lo}+"
        out[key] = sum(1 for x in xs if x >= lo and (hi is None or x < hi))
    return out
