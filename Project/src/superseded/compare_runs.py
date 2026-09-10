#!/usr/bin/env python3
"""Compare two feedback runs (v2 vs v3 prompt) on H1/H2/H3, overall + by stratum.

READS THE SUPERSEDED RUNS. NOT A SOURCE OF ANY NUMBER IN THE THESIS.

This script is kept deliberately, as the evidence behind the disclosure in the
thesis's §5.5. Both runners originally wrote their generated code to the same
filename pattern, so the second overwrote the first's saved solutions; the
affected arms were re-run under collision-free names. On the fresh runs the large
Maintainability-Index effect recorded here for the comment-stripping arm did NOT
reproduce -- it fell from roughly -16 points to the -3.0 the thesis reports, and
the strip-vs-preserve difference became non-significant. That figure and the
ablation argument built on it were withdrawn.

So the -16.3 this script prints is the WITHDRAWN figure, not a thesis result. It
is reproducible here on purpose: §5.5 claims a number did not survive re-running,
and this is what lets a reader check that claim rather than take it on trust.

For the numbers actually reported, use the canonical five runs -- see
results/README.md, and src/stats.py / src/supp_metrics.py / src/compare_blind.py.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
strata = {t["task_id"]: t["stratum"] for t in json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())}
RUNS = {"v2": "results/feedback_promptv2.jsonl", "v3": "results/feedback.jsonl"}

BANNER = """\
==============================================================================
  SUPERSEDED DATA -- these are NOT the thesis's numbers
==============================================================================
  Reads results/feedback_promptv2.jsonl + results/feedback.jsonl, both of which
  were superseded after the filename-collision incident disclosed in §5.5.

  The MI effect below (~-16 for v2) is the WITHDRAWN figure. It did not
  reproduce on the re-run; the thesis reports -3.0 from
  feedback_promptv2_restored.jsonl instead.

  For the reported numbers: python src/stats.py   (see results/README.md)
==============================================================================
"""
print(BANNER, file=sys.stderr)
print(BANNER)


def load(path):
    by = {}
    for l in (PROJECT / path).read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            by.setdefault(r["task_id"], {})[r["iteration"]] = r
    return by


def stats(by, ids):
    n = len(ids); bp = fp = reg = rep = 0
    dmi, dcc, dcog = [], [], []
    for t in ids:
        its = by[t]; b, f = its[min(its)], its[max(its)]
        bp += b["passed"]; fp += f["passed"]
        reg += b["passed"] and not f["passed"]; rep += (not b["passed"]) and f["passed"]
        bm, fm = b["metrics"], f["metrics"]
        if bm.get("mi") is not None and fm.get("mi") is not None: dmi.append(fm["mi"] - bm["mi"])
        if bm.get("cc_total") is not None: dcc.append(fm["cc_total"] - bm["cc_total"])
        if bm.get("cognitive_total") is not None and fm.get("cognitive_total") is not None:
            dcog.append(fm["cognitive_total"] - bm["cognitive_total"])
    m = lambda xs: round(st.median(xs), 1) if xs else None
    return dict(n=n, base=bp, final=fp, reg=reg, rep=rep,
                mi=m(dmi), cc=m(dcc), cog=m(dcog),
                cc_red=sum(1 for x in dcc if x < 0), cog_red=sum(1 for x in dcog if x < 0))


runs = {k: load(v) for k, v in RUNS.items()}
groups = [("OVERALL", list(strata)),
          ("LOWER", [t for t in strata if strata[t] == "lower"]),
          ("HIGHER", [t for t in strata if strata[t] == "higher"])]

for label, ids in groups:
    print(f"\n===== {label} (n={len(ids)}) =====")
    print(f"{'metric':<26}{'v2':>12}{'v3':>12}")
    a, b = stats(runs["v2"], ids), stats(runs["v3"], ids)
    print(f"{'correctness base→final':<26}{a['base']}→{a['final']:<10}{b['base']}→{b['final']}")
    print(f"{'  regressed / repaired':<26}{str(a['reg'])+'/'+str(a['rep']):>12}{str(b['reg'])+'/'+str(b['rep']):>12}")
    print(f"{'MI median Δ  [H1]':<26}{str(a['mi']):>12}{str(b['mi']):>12}")
    print(f"{'CC median Δ  [H2]':<26}{str(a['cc']):>12}{str(b['cc']):>12}")
    print(f"{'CogC median Δ  [H2]':<26}{str(a['cog']):>12}{str(b['cog']):>12}")
    print(f"{'  #CC reduced / #CogC red':<26}{str(a['cc_red'])+'/'+str(a['cog_red']):>12}{str(b['cc_red'])+'/'+str(b['cog_red']):>12}")
