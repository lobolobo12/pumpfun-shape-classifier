.PHONY: sync check test lint universe prescreen probe fetch label bench-render bench-label features leakage xgb cnn daily pull

sync:
	uv sync --group dev --extra models

lint:
	uv run ruff check src tests

test:
	uv run pytest -q

check: lint test

universe:
	uv run pf universe

prescreen:
	uv run pf prescreen

probe:
	uv run pf fetch --probe 500 --host mac

fetch:
	uv run pf fetch --host mac

label:
	uv run pf label

bench-render:
	uv run pf bench render

bench-label:
	uv run pf bench label

features:
	uv run pf features

leakage:
	uv run pf check leakage

xgb:
	uv run pf xgb

cnn:
	uv run pf cnn

daily:
	scripts/daily.sh

pull:
	uv run pf gh-pull && uv run pf to-parquet && uv run pf curve-params && uv run pf label
