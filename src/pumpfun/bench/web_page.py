"""web_page — the milestone-0 charts as one self-contained page anyone can tap through on a phone.

No labels, no mints, no numbers on the page: just the stripped images in manifest
order, two buttons, progress kept in localStorage, and at the end a compact answer
code (one character per chart: g / b) to paste back. `pf bench import <code> --who <name>`
scores it against the local manifest. Nothing needs a server or a login.
"""

from __future__ import annotations

import base64
import json
import logging
from pathlib import Path

from pumpfun.config import Config
from pumpfun.reports import write_json

log = logging.getLogger(__name__)

PAGE = """<title>Early Chart Benchmark</title>
<style>
  :root { --bg:#f4f4f2; --fg:#1d1d1d; --muted:#6b6b6b; --card:#ffffff; --line:#d9d9d6; --good:#2b7a4b; --bad:#a63d3d; }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg:#141414; --fg:#ececec; --muted:#9a9a9a; --card:#1f1f1f; --line:#333; } }
  :root[data-theme="dark"] { --bg:#141414; --fg:#ececec; --muted:#9a9a9a; --card:#1f1f1f; --line:#333; }
  body { background:var(--bg); color:var(--fg); font:16px/1.45 -apple-system, system-ui, sans-serif; margin:0; }
  main { max-width:720px; margin:0 auto; padding:16px; }
  h1 { font-size:1.15rem; margin:0 0 4px; }
  p.lead { color:var(--muted); margin:0 0 14px; font-size:.95rem; }
  .card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:12px; }
  img { display:block; width:100%; height:auto; border-radius:8px; background:#e9e9e9; }
  .row { display:flex; gap:12px; margin-top:12px; }
  button { flex:1; font:inherit; font-weight:600; padding:16px 0; border-radius:10px; border:1px solid var(--line); background:var(--card); color:var(--fg); cursor:pointer; }
  button.g { border-color:var(--good); color:var(--good); } button.b { border-color:var(--bad); color:var(--bad); }
  button:active { transform:scale(.98); }
  .meta { display:flex; justify-content:space-between; color:var(--muted); font-size:.9rem; margin-top:10px; }
  .small { font-size:.85rem; color:var(--muted); }
  textarea { width:100%; box-sizing:border-box; font:13px/1.4 ui-monospace, Menlo, monospace; height:110px; background:var(--bg); color:var(--fg); border:1px solid var(--line); border-radius:8px; padding:8px; }
  .done h2 { font-size:1.05rem; margin:0 0 8px; }
  a.reset { color:var(--muted); font-size:.85rem; }
</style>
<main>
  <h1>Does this one go?</h1>
  <p class="lead">You see the first five minutes of a new coin: price line on top, volume bars below. Decide if buying at the end of the picture would have paid off within the next hour. Go with your gut — there are no names, no numbers, and nothing to look up.</p>
  <div class="card" id="quiz">
    <img id="chart" alt="chart">
    <div class="row">
      <button class="b" id="btn-b">Doesn't go</button>
      <button class="g" id="btn-g">Goes</button>
    </div>
    <div class="meta"><span id="progress"></span><a class="reset" href="#" id="undo">undo last</a></div>
  </div>
  <div class="card done" id="done" hidden>
    <h2>Done — thank you.</h2>
    <p class="small">Copy this code and send it back (it is just your answers in order):</p>
    <textarea id="code" readonly></textarea>
    <div class="row"><button id="copy">Copy code</button></div>
    <p class="small"><a class="reset" href="#" id="restart">start over</a></p>
  </div>
</main>
<script>
  const SET = __SET_ID__;
  const IMAGES = __IMAGES__;
  const KEY = "bench-" + SET;
  let answers = "";
  try { answers = localStorage.getItem(KEY) || ""; } catch (e) {}
  const chart = document.getElementById("chart");
  const quiz = document.getElementById("quiz"), done = document.getElementById("done");
  const codeBox = document.getElementById("code");
  function save() { try { localStorage.setItem(KEY, answers); } catch (e) {} }
  function render() {
    const i = answers.length;
    if (i >= IMAGES.length) {
      quiz.hidden = true; done.hidden = false;
      codeBox.value = SET + ":" + answers;
      return;
    }
    quiz.hidden = false; done.hidden = true;
    chart.src = IMAGES[i];
    document.getElementById("progress").textContent = (i + 1) + " / " + IMAGES.length;
    if (i + 1 < IMAGES.length) { const pre = new Image(); pre.src = IMAGES[i + 1]; }
  }
  function answer(c) { if (answers.length < IMAGES.length) { answers += c; save(); render(); } }
  document.getElementById("btn-g").onclick = () => answer("g");
  document.getElementById("btn-b").onclick = () => answer("b");
  document.getElementById("undo").onclick = (e) => { e.preventDefault(); answers = answers.slice(0, -1); save(); render(); };
  document.getElementById("restart").onclick = (e) => { e.preventDefault(); answers = ""; save(); render(); };
  document.getElementById("copy").onclick = async () => {
    try { await navigator.clipboard.writeText(codeBox.value); document.getElementById("copy").textContent = "Copied"; } catch (e) { codeBox.select(); }
  };
  document.addEventListener("keydown", (e) => { if (e.key === "g") answer("g"); if (e.key === "b") answer("b"); });
  render();
</script>
"""


def build(cfg: Config) -> Path:
    out = cfg.reports_dir / "charts"
    manifest = json.loads((out / "manifest.json").read_text())
    ids = [m["chart_id"] for m in sorted(manifest, key=lambda m: m["chart_id"])]
    images = []
    for cid in ids:
        b = (out / f"{cid:03d}.png").read_bytes()
        images.append("data:image/png;base64," + base64.b64encode(b).decode())
    set_id = json.dumps(_set_id(manifest))
    html = PAGE.replace("__SET_ID__", set_id).replace("__IMAGES__", json.dumps(images))
    path = out / "bench.html"
    path.write_text(html)
    log.info("page: %d charts, %.1f MB -> %s", len(ids), len(html) / 1e6, path)
    return path


def _set_id(manifest: list[dict]) -> str:
    import hashlib

    h = hashlib.sha1("".join(m["mint"] for m in sorted(manifest, key=lambda m: m["chart_id"])).encode()).hexdigest()
    return h[:8]


def score_code(cfg: Config, code: str, who: str) -> dict:
    from pumpfun.bench.manual_label import score

    out = cfg.reports_dir / "charts"
    manifest = json.loads((out / "manifest.json").read_text())
    set_id, _, answers = code.strip().partition(":")
    if set_id != _set_id(manifest):
        raise SystemExit(f"code is for chart set {set_id!r}, local charts are {_set_id(manifest)!r}")
    ids = [m["chart_id"] for m in sorted(manifest, key=lambda m: m["chart_id"])]
    if len(answers) != len(ids) or set(answers) - {"g", "b"}:
        raise SystemExit(f"expected {len(ids)} g/b characters, got {len(answers)}")
    preds = {cid: (1 if a == "g" else 0) for cid, a in zip(ids, answers, strict=True)}
    result = {"who": who, **score(manifest, preds)}
    dest = cfg.reports_dir / f"human_benchmark_{who}.json"
    write_json(dest, result)
    log.info(
        "%s: accuracy %.3f precision %.3f recall %.3f -> %s",
        who,
        result["all"]["accuracy"],
        result["all"]["precision"] or 0,
        result["all"]["recall"] or 0,
        dest,
    )
    return result
