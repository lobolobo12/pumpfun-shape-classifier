"""first_sight — where the paper bot first sees a coin's curve, sampled per coin for training.

The bot decides at the first curve update it gets at or after the 8.6 SOL crossing. A coin it tracked
from the scanner (3-8 SOL) is decided exactly at the crossing; a coin it first sees at 15 SOL is decided
at 15 SOL. Training mirrors that: the sampled level sets both the bot-view feature truncation and, when
`botlive.entry_at_first_sight` is on, the label's entry (first crossing of max(cross_level, level)).
"""

from __future__ import annotations

import zlib

from pumpfun.config import Config


def first_seen_level(cfg: Config, mint: str) -> float:
    """Deterministic per-coin sample. `botlive.first_seen_sol` is [lo, hi] (uniform) or a mixture
    [[lo, hi, weight], ...], e.g. the empirical histogram from the bot's nn_scores."""
    spec = (cfg.raw.get("botlive") or {}).get("first_seen_sol", [3.0, 6.0])
    h = zlib.crc32(mint.encode())
    u = (h % 10_000) / 10_000.0
    if spec and isinstance(spec[0], (list, tuple)):
        w = (h // 10_000 % 10_000) / 10_000.0
        acc = 0.0
        total = sum(float(c[2]) for c in spec)
        for lo, hi, wt in spec:
            acc += float(wt) / total
            if w <= acc:
                return float(lo) + (float(hi) - float(lo)) * u
        lo, hi, _ = spec[-1]
        return float(lo) + (float(hi) - float(lo)) * u
    lo, hi = spec
    return float(lo) + (float(hi) - float(lo)) * u


def entry_level(cfg: Config, mint: str) -> float | None:
    """The cross level for this coin's label: the sampled first-sight level when it is above the
    configured crossing and entry-at-first-sight is on; otherwise None (use cfg.cross_level_sol)."""
    if not (cfg.raw.get("botlive") or {}).get("entry_at_first_sight", False):
        return None
    lvl = first_seen_level(cfg, mint)
    return lvl if lvl > float(cfg.cross_level_sol) else None
