#!/usr/bin/env python3
"""
Supplementary-metric aggregation for the paper's secondary results table:
LOC, Halstead volume/effort, and Pylint issue counts, baseline vs final, for the
three primary loop configurations. Same paired convention as stats.py (guarded
uses the carried-forward best_metrics as 'final').
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
RUNS = {
    "comment-stripping": ("results/feedback_promptv2_restored.jsonl", "plain"),
    "comment-preserving": ("results/feedback_v3_fresh.jsonl", "plain"),
    "guarded": ("results/feedback_guarded.jsonl", "guarded"),
}


def load(path):
    by = {}
    for l in (PROJECT / path).read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            by.setdefault(r["task_id"], {})[r["iteration"]] = r
    return by


def pair(by, kind, tid):
    its = by[tid]
    b, f = its[min(its)], its[max(its)]
    bm = b["metrics"]
    fm = f["best_metrics"] if kind == "guarded" else f["metrics"]
    return bm, fm


def pylint_total(m):
    p = m.get("pylint") or {}
    return sum(v for v in p.values() if isinstance(v, (int, float)))


def med(vals):
    vals = [v for v in vals if v is not None]
    return round(st.median(vals), 1) if vals else None


FIELDS = [
    ("LOC", lambda m: m.get("loc")),
    ("Halstead volume", lambda m: m.get("halstead_volume")),
    ("Halstead effort", lambda m: m.get("halstead_effort")),
    ("Pylint issues (total)", pylint_total),
]

for name, (path, kind) in RUNS.items():
    by = load(path)
    ids = list(by)
    print(f"\n=== {name}  (n={len(ids)}) ===")
    for label, fn in FIELDS:
        base_vals, final_vals, deltas = [], [], []
        for t in ids:
            bm, fm = pair(by, kind, t)
            bv, fv = fn(bm), fn(fm)
            base_vals.append(bv); final_vals.append(fv)
            if bv is not None and fv is not None:
                deltas.append(fv - bv)
        print(f"  {label:<24} base={med(base_vals)!s:<8} final={med(final_vals)!s:<8} medΔ={med(deltas)}")
