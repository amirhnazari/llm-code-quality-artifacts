#!/usr/bin/env python3
"""
First-look analysis of the feedback-loop collection (results/feedback.jsonl).

READS A SUPERSEDED RUN. NOT A SOURCE OF ANY NUMBER IN THE THESIS.

results/feedback.jsonl is the original comment-preserving run, superseded by
results/feedback_v3_fresh.jsonl after the filename-collision incident disclosed
in the thesis's §5.5 (see results/README.md). Kept for the audit trail: this was
the exploratory pass over that run, retained so the sequence of analysis is
inspectable rather than reconstructed.

Joins each (task, iteration) row with its complexity stratum and reports, overall
and per stratum: dataset integrity, correctness dynamics (H3), and baseline->final
deltas for MI (H1), cyclomatic + cognitive complexity (H2).

Not the final stats (no significance tests here) -- a sanity check + signal read.
For the reported numbers use src/stats.py on the canonical five runs.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from pathlib import Path

BANNER = """\
==============================================================================
  SUPERSEDED DATA -- these are NOT the thesis's numbers
==============================================================================
  Reads results/feedback.jsonl, superseded by feedback_v3_fresh.jsonl after the
  filename-collision incident disclosed in §5.5.

  For the reported numbers: python src/stats.py   (see results/README.md)
==============================================================================
"""
print(BANNER, file=sys.stderr)
print(BANNER)

PROJECT = Path(__file__).resolve().parent.parent.parent
rows = [json.loads(l) for l in (PROJECT / "results" / "feedback.jsonl").read_text().splitlines() if l.strip()]
strata = {t["task_id"]: t["stratum"] for t in json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())}

# group by task -> {iteration: row}
by_task: dict = {}
for r in rows:
    by_task.setdefault(r["task_id"], {})[r["iteration"]] = r

# ---- integrity ----
iters = sorted({r["iteration"] for r in rows})
none_mi = sum(1 for r in rows if r["metrics"].get("mi") is None)
print("== integrity ==")
print(f"rows={len(rows)}  tasks={len(by_task)}  iterations={iters}")
print(f"expected rows = {len(by_task)} tasks x {len(iters)} iters = {len(by_task)*len(iters)}")
print(f"rows with MI=None (unparseable code): {none_mi}")


def summarize(task_ids, label):
    n = len(task_ids)
    base_pass = fin_pass = repaired = regressed = 0
    dmi, dcc, dcog = [], [], []
    imp_mi = red_cc = red_cog = 0
    for tid in task_ids:
        its = by_task[tid]
        b = its[min(its)]
        f = its[max(its)]
        base_pass += int(b["passed"])
        fin_pass += int(f["passed"])
        repaired += int((not b["passed"]) and f["passed"])
        regressed += int(b["passed"] and (not f["passed"]))
        bm, fm = b["metrics"], f["metrics"]
        if bm.get("mi") is not None and fm.get("mi") is not None:
            d = fm["mi"] - bm["mi"]; dmi.append(d); imp_mi += int(d > 0.5)
        if bm.get("cc_total") is not None and fm.get("cc_total") is not None:
            d = fm["cc_total"] - bm["cc_total"]; dcc.append(d); red_cc += int(d < 0)
        if bm.get("cognitive_total") is not None and fm.get("cognitive_total") is not None:
            d = fm["cognitive_total"] - bm["cognitive_total"]; dcog.append(d); red_cog += int(d < 0)
    med = lambda xs: round(st.median(xs), 2) if xs else None
    print(f"\n== {label} (n={n}) ==")
    print(f"  correctness: baseline {base_pass}/{n} -> final {fin_pass}/{n}   "
          f"(repaired {repaired}, regressed {regressed})   [H3]")
    print(f"  MI  Δ(base→final): median {med(dmi)}   improved(>0.5): {imp_mi}/{n}   [H1]")
    print(f"  CC  Δ: median {med(dcc)}   reduced: {red_cc}/{n}   [H2]")
    print(f"  CogC Δ: median {med(dcog)}  reduced: {red_cog}/{n}   [H2]")


all_ids = list(by_task)
summarize(all_ids, "OVERALL")
summarize([t for t in all_ids if strata.get(t) == "lower"], "LOWER complexity (CC 3-4)")
summarize([t for t in all_ids if strata.get(t) == "higher"], "HIGHER complexity (CC>=5)")
