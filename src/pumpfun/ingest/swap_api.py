"""swap_api — pump.fun's keyless trade tape, fetched politely.

  GET {base_url}/{mint}/trades?limit=100[&createdTs=<ms>][&cursor=<slotIndexId>-<ms>]

Newest first; `pagination.nextCursor` pages older. A synthetic cursor
("<slot padded 10>9999999999-<ms>") jumps straight to a time so a long-lived
coin does not have to be walked from its newest trade; the slot is estimated
from an anchor (slot, ms) at `slot_ms_estimate` per slot, which over-estimates
the slot length so the jump lands AFTER the target and nothing is skipped.

Rate limiting is the whole game (Cloudflare 1015 at ~300 req/min per IP,
sticky for a minute): one global gap between requests, x1.5 on a 429 (<= 10 s),
x0.85 after 25 clean requests (>= the configured gap); a 429 sleeps
`retry-after` + 5 s and is never a failure. Plain research UA — Cloudflare 403s
a browser UA from a non-browser TLS client.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any

import httpx

from pumpfun.config import SwapApi

log = logging.getLogger(__name__)


@dataclass
class FetchStats:
    requests: int = 0
    http_429: int = 0
    http_other: int = 0
    network_err: int = 0
    bytes: int = 0
    seconds_sleeping: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Trade:
    at_ms: int
    slot: int
    idx: int
    user: str
    is_buy: bool
    program: str
    sol: float
    tokens: float
    price_sol: float
    fill_price_sol: float | None
    tx: str

    def to_json(self) -> dict[str, Any]:
        return {
            "at": self.at_ms,
            "slot": self.slot,
            "idx": self.idx,
            "user": self.user,
            "side": "buy" if self.is_buy else "sell",
            "program": self.program,
            "sol": self.sol,
            "tokens": self.tokens,
            "priceSol": self.price_sol,
            "fillPriceSol": self.fill_price_sol,
            "tx": self.tx,
        }

    @staticmethod
    def from_json(d: dict[str, Any]) -> Trade:
        return Trade(
            at_ms=int(d["at"]),
            slot=int(d["slot"]),
            idx=int(d["idx"]),
            user=str(d["user"]),
            is_buy=d["side"] == "buy",
            program=str(d["program"]),
            sol=float(d["sol"]),
            tokens=float(d["tokens"]),
            price_sol=float(d["priceSol"]),
            fill_price_sol=None if d.get("fillPriceSol") is None else float(d["fillPriceSol"]),
            tx=str(d["tx"]),
        )


def parse_trade(r: dict[str, Any]) -> Trade:
    sid = str(r["slotIndexId"])
    at_ms = _iso_ms(str(r["timestamp"]))
    fp = r.get("fillPriceSol")
    return Trade(
        at_ms=at_ms,
        slot=int(sid[:10]),
        idx=int(sid[10:] or 0),
        user=str(r["userAddress"]),
        is_buy=r["type"] == "buy",
        program=str(r.get("program", "")),
        sol=float(r["amountSol"]),
        tokens=float(r["baseAmount"]),
        price_sol=float(r["priceSol"]),
        fill_price_sol=None if fp is None else float(fp),
        tx=str(r["tx"]),
    )


def _iso_ms(ts: str) -> int:
    from datetime import datetime

    return int(datetime.fromisoformat(ts.replace("Z", "+00:00")).timestamp() * 1000)


@dataclass(frozen=True)
class Anchor:
    slot: int
    at_ms: int


def synthetic_cursor(anchor: Anchor, until_ms: int, slot_ms_estimate: int) -> str | None:
    if until_ms >= anchor.at_ms:
        return None
    est = anchor.slot - (anchor.at_ms - until_ms) // slot_ms_estimate
    if est <= 0:
        return None
    return f"{est:010d}9999999999-{until_ms}"


@dataclass
class TradeFile:
    mint: str
    fetched_at_ms: int
    start_cursor: str | None
    complete: bool
    pages: int
    trades: list[Trade]

    def to_json(self) -> dict[str, Any]:
        return {
            "mint": self.mint,
            "fetchedAt": self.fetched_at_ms,
            "startCursor": self.start_cursor,
            "complete": self.complete,
            "pages": self.pages,
            "trades": [t.to_json() for t in self.trades],
        }

    @staticmethod
    def from_json(d: dict[str, Any]) -> TradeFile:
        return TradeFile(
            mint=str(d["mint"]),
            fetched_at_ms=int(d["fetchedAt"]),
            start_cursor=d.get("startCursor"),
            complete=bool(d.get("complete", False)),
            pages=int(d.get("pages", 0)),
            trades=[Trade.from_json(t) for t in d["trades"]],
        )


class SwapApiClient:
    def __init__(self, cfg: SwapApi, rps: float, sleep=time.sleep):
        self.cfg = cfg
        self.stats = FetchStats()
        self._min_gap = 1.0 / max(rps, 0.05)
        self._gap = self._min_gap
        self._next_at = 0.0
        self._clean = 0
        self._sleep = sleep
        self._http = httpx.Client(
            headers={"user-agent": cfg.user_agent, "accept": "application/json"},
            timeout=cfg.timeout_seconds,
        )

    @property
    def gap_seconds(self) -> float:
        return self._gap

    def close(self) -> None:
        self._http.close()

    def _wait_turn(self) -> None:
        now = time.monotonic()
        if self._next_at > now:
            self.stats.seconds_sleeping += self._next_at - now
            self._sleep(self._next_at - now)
        self._next_at = time.monotonic() + self._gap

    def _get(self, url: str) -> dict[str, Any] | None:
        for attempt in range(6):
            self._wait_turn()
            self.stats.requests += 1
            try:
                res = self._http.get(url)
            except httpx.HTTPError as e:
                self.stats.network_err += 1
                log.warning("network error %s (%s); retry %d", e.__class__.__name__, url[-60:], attempt)
                self._sleep(3.0 * (attempt + 1))
                continue
            self.stats.bytes += len(res.content)
            if res.status_code == 429:
                self.stats.http_429 += 1
                ra = res.headers.get("retry-after")
                try:
                    secs = float(ra) if ra is not None else 30.0
                except ValueError:
                    secs = 30.0
                self._gap = min(10.0, self._gap * 1.5)
                self._clean = 0
                log.info("429 — sleeping %.0f s, gap now %.2f s", secs + 5, self._gap)
                self.stats.seconds_sleeping += secs + 5
                self._sleep(secs + 5)
                continue
            self._clean += 1
            if self._clean >= 25:
                self._clean = 0
                self._gap = max(self._min_gap, self._gap * 0.85)
            if res.status_code in (400, 404):
                self.stats.http_other += 1
                return None
            if res.status_code >= 500 or res.status_code != 200:
                self.stats.http_other += 1
                self._sleep(3.0 * (attempt + 1))
                continue
            try:
                return res.json()
            except ValueError:
                self.stats.http_other += 1
                self._sleep(2.0)
        return None

    def _url(self, mint: str, created_ms: int | None, cursor: str | None) -> str:
        q = f"limit={self.cfg.page_limit}"
        if created_ms is not None:
            q += f"&createdTs={created_ms}"
        if cursor:
            q += f"&cursor={cursor}"
        return f"{self.cfg.base_url}/{mint}/trades?{q}"

    def newest(self, mint: str, created_ms: int | None = None) -> Trade | None:
        page = self._get(f"{self.cfg.base_url}/{mint}/trades?limit=1" + (f"&createdTs={created_ms}" if created_ms else ""))
        rows = (page or {}).get("trades") or []
        return parse_trade(rows[0]) if rows else None

    def fetch_tape(
        self,
        mint: str,
        created_ms: int,
        until_ms: int,
        anchor: Anchor | None,
        max_pages: int | None = None,
    ) -> TradeFile:
        """All trades of `mint` in [creation, until_ms], chronological, plus anything the last page carried."""
        max_pages = max_pages or self.cfg.max_pages_per_coin
        start = synthetic_cursor(anchor, until_ms, self.cfg.slot_ms_estimate) if anchor else None
        cursor = start
        out: list[Trade] = []
        complete = False
        pages = 0
        while pages < max_pages:
            page = self._get(self._url(mint, created_ms, cursor))
            pages += 1
            if page is None:
                break
            rows = [parse_trade(r) for r in page.get("trades") or []]
            out.extend(rows)
            pg = page.get("pagination") or {}
            oldest = rows[-1].at_ms if rows else None
            if not pg.get("hasMore") or not pg.get("nextCursor"):
                complete = True
                break
            if oldest is not None and oldest <= created_ms:
                complete = True
                break
            cursor = str(pg["nextCursor"])
        out.sort(key=lambda t: (t.slot, t.idx, t.at_ms))
        # De-duplicate on signature: pages can overlap at the cursor boundary.
        seen: set[str] = set()
        uniq: list[Trade] = []
        for t in out:
            if t.tx in seen:
                continue
            seen.add(t.tx)
            uniq.append(t)
        return TradeFile(
            mint=mint, fetched_at_ms=int(time.time() * 1000), start_cursor=start, complete=complete, pages=pages, trades=uniq
        )
