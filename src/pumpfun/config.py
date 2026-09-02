"""config — the one place config.yaml is read.

Every knob lives in config.yaml; a preset (presets/<name>.yaml) overlays it and
`--set a.b=c` overrides win over both. Nothing in src/ may carry a default for
any of these values.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config.yaml"
PRESETS_DIR = ROOT / "presets"


@dataclass(frozen=True)
class FeeBps:
    lp: int
    protocol: int
    creator: int


@dataclass(frozen=True)
class CurveExpected:
    initial_virtual_sol_lamports: int
    initial_virtual_token_raw: int
    initial_real_token_raw: int
    token_total_supply_raw: int
    token_decimals: int


@dataclass(frozen=True)
class Migration:
    base_tokens_raw: int
    quote_lamports: int
    virtual_quote_lamports: int


@dataclass(frozen=True)
class SwapApi:
    base_url: str
    user_agent: str
    page_limit: int
    rps_mac: float
    rps_vps: float
    slot_ms_estimate: int
    horizon_margin_seconds: int
    timeout_seconds: float
    max_pages_per_coin: int


@dataclass(frozen=True)
class Sources:
    attention_db: Path
    pumpportal_raw: Path
    seed_trade_cache: Path


@dataclass(frozen=True)
class Universe:
    max_first_seen_age_seconds: float
    coverage_min: float


@dataclass(frozen=True)
class Prescreen:
    sample_rate_unlikely_quiet: float
    sample_rate_unknown: float
    fdv_candidate_usd: float
    sample_rate_hist_candidate: float
    sample_rate_hist: float


@dataclass(frozen=True)
class Bench:
    n_per_class: int
    image_px: tuple[int, int]


@dataclass(frozen=True)
class Config:
    decision_mode: str
    cross_level_sol: float
    cross_min_age_seconds: float
    window_seconds: int
    resample_steps: int
    horizon_seconds: int
    tp: float
    sl: float
    trailing_stop: bool
    position_sol: float
    entry_lag_seconds: int
    min_trades_in_window: int
    neg_pos_ratio: float
    zone_sol: tuple[float, float]
    date_start: str
    date_end: str
    split_train_end: str
    split_val_end: str
    split_timezone: str
    fee_protocol_bps: int
    fee_creator_bps: int
    pool_fee_bps: FeeBps
    router_fee_pct: float
    tx_fee_sol: float
    curve_expected: CurveExpected
    curve_param_tolerance: float
    migration: Migration
    swap_api: SwapApi
    sources: Sources
    universe: Universe
    prescreen: Prescreen
    bench: Bench
    xgb: dict[str, Any]
    cnn: dict[str, Any]
    metrics: dict[str, Any]
    data_dir: Path
    reports_dir: Path
    seed: int
    preset: str | None
    raw: dict[str, Any]

    # derived paths --------------------------------------------------------
    @property
    def raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def interim_dir(self) -> Path:
        return self.data_dir / "interim"

    @property
    def processed_dir(self) -> Path:
        return self.data_dir / "processed"

    @property
    def tokens_path(self) -> Path:
        return self.raw_dir / "tokens.parquet"

    @property
    def trades_dir(self) -> Path:
        return self.raw_dir / "trades"

    @property
    def trade_cache_dir(self) -> Path:
        return self.raw_dir / "cache"

    @property
    def ledger_path(self) -> Path:
        return self.raw_dir / "fetch_ledger.sqlite"

    @property
    def position_lamports(self) -> int:
        return round(self.position_sol * 1_000_000_000)

    @property
    def tx_fee_lamports(self) -> int:
        return round(self.tx_fee_sol * 1_000_000_000)

    @property
    def entry_offset_seconds(self) -> int:
        return self.window_seconds + self.entry_lag_seconds

    @property
    def tape_until_seconds(self) -> int:
        """Seconds after launch up to which trades are needed."""
        return self.entry_offset_seconds + self.horizon_seconds + self.swap_api.horizon_margin_seconds


def _deep_merge(base: dict[str, Any], over: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def _parse_scalar(s: str) -> Any:
    return yaml.safe_load(s)


def _apply_overrides(d: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    out = copy.deepcopy(d)
    for item in overrides:
        if "=" not in item:
            raise ValueError(f"override must be key=value, got {item!r}")
        key, val = item.split("=", 1)
        parts = key.split(".")
        cur = out
        for p in parts[:-1]:
            if p not in cur or not isinstance(cur[p], dict):
                raise KeyError(f"unknown config path {key!r}")
            cur = cur[p]
        if parts[-1] not in cur:
            raise KeyError(f"unknown config key {key!r}")
        cur[parts[-1]] = _parse_scalar(val)
    return out


def _resolve(p: str) -> Path:
    path = Path(p).expanduser()
    return path if path.is_absolute() else ROOT / path


def load_config(
    path: Path = CONFIG_PATH,
    preset: str | None = None,
    overrides: list[str] | None = None,
) -> Config:
    with open(path) as f:
        d = yaml.safe_load(f)
    if preset:
        with open(PRESETS_DIR / f"{preset}.yaml") as f:
            d = _deep_merge(d, yaml.safe_load(f) or {})
    if overrides:
        d = _apply_overrides(d, overrides)
    return _build(d, preset)


def _build(d: dict[str, Any], preset: str | None) -> Config:
    ce = d["curve_expected"]
    mg = d["migration"]
    sa = d["swap_api"]
    so = d["sources"]
    un = d["universe"]
    ps = d["prescreen"]
    be = d["bench"]
    pf = d["pool_fee_bps"]
    return Config(
        decision_mode=str(d["decision_mode"]),
        cross_level_sol=float(d["cross_level_sol"]),
        cross_min_age_seconds=float(d["cross_min_age_seconds"]),
        window_seconds=int(d["window_seconds"]),
        resample_steps=int(d["resample_steps"]),
        horizon_seconds=int(d["horizon_seconds"]),
        tp=float(d["tp"]),
        sl=float(d["sl"]),
        trailing_stop=bool(d["trailing_stop"]),
        position_sol=float(d["position_sol"]),
        entry_lag_seconds=int(d["entry_lag_seconds"]),
        min_trades_in_window=int(d["min_trades_in_window"]),
        neg_pos_ratio=float(d["neg_pos_ratio"]),
        zone_sol=(float(d["zone_sol"][0]), float(d["zone_sol"][1])),
        date_start=str(d["date_start"]),
        date_end=str(d["date_end"]),
        split_train_end=str(d["split_train_end"]),
        split_val_end=str(d["split_val_end"]),
        split_timezone=str(d["split_timezone"]),
        fee_protocol_bps=int(d["fee_protocol_bps"]),
        fee_creator_bps=int(d["fee_creator_bps"]),
        pool_fee_bps=FeeBps(lp=int(pf["lp"]), protocol=int(pf["protocol"]), creator=int(pf["creator"])),
        router_fee_pct=float(d["router_fee_pct"]),
        tx_fee_sol=float(d["tx_fee_sol"]),
        curve_expected=CurveExpected(
            initial_virtual_sol_lamports=int(ce["initial_virtual_sol_lamports"]),
            initial_virtual_token_raw=int(ce["initial_virtual_token_raw"]),
            initial_real_token_raw=int(ce["initial_real_token_raw"]),
            token_total_supply_raw=int(ce["token_total_supply_raw"]),
            token_decimals=int(ce["token_decimals"]),
        ),
        curve_param_tolerance=float(d["curve_param_tolerance"]),
        migration=Migration(
            base_tokens_raw=int(mg["base_tokens_raw"]),
            quote_lamports=int(mg["quote_lamports"]),
            virtual_quote_lamports=int(mg["virtual_quote_lamports"]),
        ),
        swap_api=SwapApi(
            base_url=str(sa["base_url"]),
            user_agent=str(sa["user_agent"]),
            page_limit=int(sa["page_limit"]),
            rps_mac=float(sa["rps_mac"]),
            rps_vps=float(sa["rps_vps"]),
            slot_ms_estimate=int(sa["slot_ms_estimate"]),
            horizon_margin_seconds=int(sa["horizon_margin_seconds"]),
            timeout_seconds=float(sa["timeout_seconds"]),
            max_pages_per_coin=int(sa["max_pages_per_coin"]),
        ),
        sources=Sources(
            attention_db=_resolve(so["attention_db"]),
            pumpportal_raw=_resolve(so["pumpportal_raw"]),
            seed_trade_cache=_resolve(so["seed_trade_cache"]),
        ),
        universe=Universe(
            max_first_seen_age_seconds=float(un["max_first_seen_age_seconds"]),
            coverage_min=float(un["coverage_min"]),
        ),
        prescreen=Prescreen(
            sample_rate_unlikely_quiet=float(ps["sample_rate_unlikely_quiet"]),
            sample_rate_unknown=float(ps["sample_rate_unknown"]),
            fdv_candidate_usd=float(ps["fdv_candidate_usd"]),
            sample_rate_hist_candidate=float(ps["sample_rate_hist_candidate"]),
            sample_rate_hist=float(ps["sample_rate_hist"]),
        ),
        bench=Bench(
            n_per_class=int(be["n_per_class"]),
            image_px=(int(be["image_px"][0]), int(be["image_px"][1])),
        ),
        xgb=dict(d["xgb"]),
        cnn=dict(d["cnn"]),
        metrics=dict(d["metrics"]),
        data_dir=_resolve(d["paths"]["data"]),
        reports_dir=_resolve(d["paths"]["reports"]),
        seed=int(d["seed"]),
        preset=preset,
        raw=d,
    )
