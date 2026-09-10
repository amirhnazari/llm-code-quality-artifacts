#!/usr/bin/env python3
"""
Ablation analysis: code-BLIND feedback (feedback_blind.jsonl) vs code-AWARE
feedback (feedback_v3_fresh.jsonl, the canonical comment-preserving run) and the
baseline. The comment-preserving arm is the fair comparison because the blind prompt
is also comment-friendly (it asks for a docstring), so the contrast isolates whether
the model is shown its own code rather than how comments are handled.

Answers, per metric (MI / CC / CogC) and for correctness:
  1. Does the code-blind loop move the metric at all? (Wilcoxon vs its own iter-0)
  2. How does its effect SIZE compare to the code-aware loop? (median deltas side by side)
  3. Does correctness churn more under blind regeneration? (baseline->final counts,
     McNemar exact, and pass->fail / fail->pass breakdown)
  4. Head-to-head: is the blind-vs-aware per-task difference itself significant?

Same paired final-baseline convention as stats.py; zero diffs dropped by Wilcoxon.
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

from scipy.stats import binomtest, wilcoxon

PROJECT = Path(__file__).resolve().parent.parent
strata = {t["task_id"]: t["stratum"] for t in json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())}
METRICS = [("MI", "mi"), ("CC", "cc_total"), ("CogC", "cognitive_total")]


def load(path):
    by = {}
    p = PROJECT / path
    if not p.exists():
        return None
    for l in p.read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            by.setdefault(r["task_id"], {})[r["iteration"]] = r
    return by


def pair(by, tid, kind="plain"):
    """(baseline_metrics, final_metrics, base_pass, final_pass).
    guarded kind uses the carried-forward best_* as the final."""
    its = by[tid]
    b, f = its[min(its)], its[max(its)]
    if kind == "guarded":
        return b["metrics"], f["best_metrics"], b["passed"], f["best_passed"]
    return b["metrics"], f["metrics"], b["passed"], f["passed"]


def deltas(by, ids, key, kind="plain"):
    ds = []
    for t in ids:
        bm, fm, *_ = pair(by, t, kind)
        if bm.get(key) is not None and fm.get(key) is not None:
            ds.append(fm[key] - bm[key])
    return ds


def wilcox(ds):
    nz = [d for d in ds if d != 0]
    med = round(st.median(ds), 2) if ds else None
    if len(nz) < 1:
        return f"med Δ={med}  (no non-zero pairs -> n/a)"
    w, p = wilcoxon(ds)
    star = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    return f"med Δ={med:<6} n(≠0)={len(nz):<3} W={w:<7.1f} p={p:.4f} [{star}]"


def mcnemar(by, ids, kind="plain"):
    b_pf = c_fp = base = final = 0
    for t in ids:
        _, _, bp, fp = pair(by, t, kind)
        base += bp; final += fp
        if bp and not fp:
            b_pf += 1
        elif (not bp) and fp:
            c_fp += 1
    n = b_pf + c_fp
    if n == 0:
        return f"base→final {base}→{final}  discordant 0 -> p=1.000"
    p = binomtest(min(b_pf, c_fp), n, 0.5, alternative="two-sided").pvalue
    star = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    return f"base→final {base}→{final}  pass→fail={b_pf}  fail→pass={c_fp}  McNemar p={p:.4f} [{star}]"


# (name, path, kind). aware = v3 code-aware comment-preserving (fair blind match).
ARMS = [
    ("blind        ", "results/feedback_blind.jsonl", "plain"),
    ("aware (v3)    ", "results/feedback_v3_fresh.jsonl", "plain"),
    ("guarded-blind ", "results/feedback_guarded_blind.jsonl", "guarded"),
    ("guarded-aware ", "results/feedback_guarded.jsonl", "guarded"),
]
loaded = [(n, load(p), k) for n, p, k in ARMS]
present = [(n, by, k) for n, by, k in loaded if by is not None]
missing = [n.strip() for n, by, k in loaded if by is None]
if missing:
    print(f"[note] not yet present, skipped: {', '.join(missing)}")

# common task set across all present arms + the strata
ids = [t for t in strata if all(t in by for _, by, _ in present)]

print("=" * 74)
print(f"  BLIND ablation -- all arms   (n={len(ids)} common tasks)")
print("=" * 74)

print("\n-- Correctness (H3): baseline->final, discordant pairs, McNemar --")
for n, by, k in present:
    print(f"  {n}: {mcnemar(by, ids, k)}")

for label, key in METRICS:
    print(f"\n-- {label} (paired final-baseline) --")
    for n, by, k in present:
        print(f"  {n}: {wilcox(deltas(by, ids, key, k))}")

# head-to-head that isolates the code-vs-noCode factor within each guard setting
def head_to_head(a, b, key, ka, kb):
    d = []
    for t in ids:
        _, af, *_ = pair(a, t, ka)
        _, bf, *_ = pair(b, t, kb)
        if af.get(key) is not None and bf.get(key) is not None:
            d.append(af[key] - bf[key])
    return wilcox(d)

by_map = {n.strip(): (by, k) for n, by, k in present}
print("\n" + "-" * 74)
print("Head-to-head (per-task final vs final; >0 on CC/CogC = LEFT more complex):")
if "blind" in by_map and "aware (v3)" in by_map:
    for label, key in METRICS:
        (ba, ka), (aa, kaw) = by_map["blind"], by_map["aware (v3)"]
        print(f"  blind − aware        {label:<5}: {head_to_head(ba, aa, key, ka, kaw)}")
if "guarded-blind" in by_map and "guarded-aware" in by_map:
    for label, key in METRICS:
        (gb, kgb), (ga, kga) = by_map["guarded-blind"], by_map["guarded-aware"]
        print(f"  gBlind − gAware      {label:<5}: {head_to_head(gb, ga, key, kgb, kga)}")

print("\n" + "-" * 74)
print("Wilcoxon two-sided, zero diffs dropped. * p<.05 ** p<.01 *** p<.001.")
print("Guarded arms use the carried-forward best_* as 'final' (correctness never drops).")
