"""pf — the command line. One subcommand per pipeline stage; config from config.yaml (+ --preset, --set)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from pumpfun.config import load_config


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pf", description="pumpfun-shape-classifier pipeline")
    p.add_argument("--preset", help="overlay presets/<name>.yaml on config.yaml")
    p.add_argument("--set", action="append", default=[], metavar="KEY=VAL", help="override a config value (dotted path)")
    p.add_argument("-v", "--verbose", action="store_true")
    sub = p.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("universe", help="attention.db snapshot -> data/raw/tokens.parquet + coverage check")
    u.add_argument("--no-strict", action="store_true", help="report low coverage instead of failing")

    sub.add_parser("prescreen", help="drop coins with zero curve inflow; write the fetch queue")

    f = sub.add_parser("fetch", help="fetch trade tapes for the queue (resumable)")
    f.add_argument("--host", choices=["mac", "vps"], required=True)
    f.add_argument("--probe", type=int, metavar="N", help="fetch a seeded random N and write reports/cost_probe.json")
    f.add_argument("--limit", type=int)
    f.add_argument("--force", action="store_true", help="run on the Mac even while the repo's study fetcher is up")
    f.add_argument("--import-seed", action="store_true", help="adopt the trading repo's cached tapes that cover the horizon")
    f.add_argument("--shard", metavar="I/N", help="work only on mints with crc32 %% N == I (own ledger per shard)")
    f.add_argument("--max-minutes", type=float, help="stop cleanly after this long (resumable)")
    f.add_argument("--rps", type=float, help="override the host's requests per second")
    f.add_argument("--queue", type=Path, help="queue parquet (default data/interim/fetch_queue.parquet)")

    g = sub.add_parser("gh-pull", help="download fetch artifacts from GitHub Actions runs and merge them into the local cache")
    g.add_argument("--run-id", action="append", type=int, default=[], help="specific run id(s); default: recent successful runs")
    g.add_argument("--limit", type=int, default=10)
    g.add_argument("--repo", help="pull from a fork, e.g. friendname/pumpfun-shape-classifier")

    md = sub.add_parser(
        "merge-dir", help="merge a folder of tapes+ledgers (e.g. a friend's zipped data/raw) into the local cache"
    )
    md.add_argument("path", type=Path)

    sub.add_parser("to-parquet", help="cached tapes -> data/raw/trades/{yyyy-mm}/*.parquet")
    sub.add_parser("history-merge", help="merge the pulled Bitquery days into tokens.parquet")
    sub.add_parser("fix-launch-times", help="correct hour-floored historical launch times from fetched tapes")
    sub.add_parser("curve-params", help="derive curve constants from the tapes and assert stability")
    sub.add_parser("label", help="triple-barrier labels on realized exits")
    sub.add_parser("features", help="tabular + sequence features, splits")

    c = sub.add_parser("check", help="assertion passes")
    c.add_argument("what", choices=["leakage", "schema"])

    b = sub.add_parser("bench", help="milestone 0")
    b.add_argument("what", choices=["render", "label", "page", "import"])
    b.add_argument("--code", help="import: the answer code from the web page")
    b.add_argument("--who", default="operator", help="import: who answered (file suffix)")

    sub.add_parser("xgb", help="milestone 4")
    sub.add_parser("cnn", help="milestone 5")
    sub.add_parser("cnn-pretrain", help="self-supervised trunk pretraining on every tape (labels untouched)")
    sub.add_parser("ensemble", help="rank-average the saved test scores of ensemble.members")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )
    cfg = load_config(preset=args.preset, overrides=args.set)

    if args.cmd == "universe":
        from pumpfun.ingest import universe

        universe.run(cfg, strict=not args.no_strict)
    elif args.cmd == "prescreen":
        from pumpfun.ingest import prescreen

        prescreen.run(cfg)
    elif args.cmd == "fetch":
        from pumpfun.ingest import fetch_trades

        shard = None
        if args.shard:
            i, n = args.shard.split("/")
            shard = (int(i), int(n))
        fetch_trades.run(
            cfg,
            host=args.host,
            probe_n=args.probe,
            force=args.force,
            limit=args.limit,
            do_import_seed=args.import_seed,
            shard=shard,
            max_seconds=None if args.max_minutes is None else args.max_minutes * 60,
            rps=args.rps,
            queue_path=args.queue,
        )
    elif args.cmd == "gh-pull":
        from pumpfun.ingest import gh_pull

        gh_pull.run(cfg, run_ids=args.run_id, limit=args.limit, repo=args.repo)
    elif args.cmd == "merge-dir":
        from pumpfun.ingest import gh_pull

        tapes, rows = gh_pull.merge_dir(cfg, args.path)
        print(f"merged {tapes} tapes, {rows} ledger rows from {args.path}")
    elif args.cmd == "to-parquet":
        from pumpfun.ingest import to_parquet

        to_parquet.run(cfg)
    elif args.cmd == "history-merge":
        from pumpfun.ingest import bitquery_history

        bitquery_history.merge_into_tokens(cfg)
    elif args.cmd == "fix-launch-times":
        from pumpfun.ingest import bitquery_history

        bitquery_history.fix_launch_times(cfg)
    elif args.cmd == "curve-params":
        from pumpfun.label import curve_params

        curve_params.run(cfg)
    elif args.cmd == "label":
        from pumpfun.label import barriers

        barriers.run(cfg)
    elif args.cmd == "features":
        from pumpfun.features import build

        build.run(cfg)
    elif args.cmd == "check":
        if args.what == "leakage":
            from pumpfun.checks import leakage

            leakage.run(cfg)
        else:
            from pumpfun.checks import schema_check

            schema_check.run(cfg)
    elif args.cmd == "bench":
        if args.what == "render":
            from pumpfun.bench import render_charts

            render_charts.run(cfg)
        elif args.what == "page":
            from pumpfun.bench import web_page

            web_page.build(cfg)
        elif args.what == "import":
            from pumpfun.bench import web_page

            if not args.code:
                raise SystemExit("--code is required")
            web_page.score_code(cfg, args.code, args.who)
        else:
            from pumpfun.bench import manual_label

            manual_label.run(cfg)
    elif args.cmd == "xgb":
        from pumpfun.models import xgb

        xgb.run(cfg)
    elif args.cmd == "cnn":
        from pumpfun.models import cnn

        cnn.run(cfg)
    elif args.cmd == "cnn-pretrain":
        from pumpfun.models import cnn

        cnn.pretrain(cfg)
    elif args.cmd == "ensemble":
        from pumpfun.models import ensemble

        ensemble.run(cfg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
