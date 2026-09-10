#!/usr/bin/env python3
"""
Phase 4 -- significance tests on the paired baseline->final data, for all three
runs (v2, v3 unguarded; guarded).

  H1 (MI) / H2 (CC, CogC):  Wilcoxon signed-rank test on the per-task paired
                            difference final - baseline (two-sided). Non-parametric
                            + paired = correct for these bounded, non-normal metrics.
  H3 (correctness):         McNemar exact test on the 2x2 of (baseline pass,
                            final pass); the discordant pairs (pass->fail vs
                            fail->pass) carry the signal.

"final" = last iteration for v2/v3 (feed-latest); the carried-forward BEST version
(best_metrics / best_passed) for the guarded run.

Caveat printed at the end: n is small (63; higher=23), one model. This is a family
of twelve primary tests (3 runs x [MI, CC, CogC, correctness]); p-values are
reported raw here, but the paper additionally assesses them against a Bonferroni-
corrected threshold alpha* = 0.05/12 ~ 0.004 to control the family-wise error rate.
The per-stratum results are secondary/exploratory.
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

from scipy.stats import binomtest, wilcoxon

PROJECT = Path(__file__).resolve().parent.parent
strata = {t["task_id"]: t["stratum"] for t in json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())}
# CANONICAL runs. v2/v3 use the FRESH re-runs (collision-free files, current
# tooling, fully reproducible+archivable). The original recorded feedback_promptv2/
# feedback jsonl are superseded: v2's original code was overwritten by v3 and its
# exact prompt was never committed, and on fresh runs the comment-stripping MI
# effect did NOT reproduce (see PROGRESS.md #8). Guarded keeps its recorded run
# (its code files are intact on disk and match its JSONL).
RUNS = {
    "v2 (unguarded)": ("results/feedback_promptv2_restored.jsonl", "plain"),
    "v3 (unguarded)": ("results/feedback_v3_fresh.jsonl", "plain"),
    "guarded": ("results/feedback_guarded.jsonl", "guarded"),
}
# Secondary ablation: code-BLIND feedback (findings only, no code shown). Kept in a
# SEPARATE family from the 12 primary tests -- it answers a different question ("does
# the model need its own code?") and carries its own Bonferroni correction.
SECONDARY_RUNS = {
    "blind (unguarded)": ("results/feedback_blind.jsonl", "plain"),
    "guarded-blind": ("results/feedback_guarded_blind.jsonl", "guarded"),
}
METRICS = [("MI  [H1]", "mi"), ("CC  [H2]", "cc_total"), ("CogC[H2]", "cognitive_total")]


def load(path):
    by = {}
    for l in (PROJECT / path).read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            by.setdefault(r["task_id"], {})[r["iteration"]] = r
    return by


def pair(by, kind, tid):
    """Return (baseline_row_metrics, final_metrics, base_pass, final_pass)."""
    its = by[tid]
    b, f = its[min(its)], its[max(its)]
    bm = b["metrics"]
    if kind == "guarded":
        fm, fp = f["best_metrics"], f["best_passed"]
    else:
        fm, fp = f["metrics"], f["passed"]
    return bm, fm, b["passed"], fp


def deltas(by, kind, ids, key):
    ds = []
    for t in ids:
        bm, fm, *_ = pair(by, kind, t)
        if bm.get(key) is not None and fm.get(key) is not None:
            ds.append(fm[key] - bm[key])
    return ds


def wilcox(ds):
    nz = [d for d in ds if d != 0]
    med = round(st.median(ds), 2) if ds else None
    if len(nz) < 1:
        return f"med Δ={med}  (no non-zero pairs -> n/a)"
    try:
        w, p = wilcoxon(ds)  # default drops zero-diffs
        star = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
        return f"med Δ={med:<6} n(≠0)={len(nz):<3} W={w:<7.1f} p={p:.4f} [{star}]"
    except ValueError as e:
        return f"med Δ={med}  (wilcoxon: {e})"


def mcnemar(by, kind, ids):
    # 2x2: rows = baseline pass?, cols = final pass?
    b_pf = c_fp = 0  # b = pass->fail (regression), c = fail->pass (repair)
    base = final = 0
    for t in ids:
        _, _, bp, fp = pair(by, kind, t)
        base += bp; final += fp
        if bp and not fp:
            b_pf += 1
        elif (not bp) and fp:
            c_fp += 1
    n = b_pf + c_fp
    if n == 0:
        return f"base→final {base}→{final}  discordant: 0 (pass→fail={b_pf}, fail→pass={c_fp})  no discordant pairs -> p=1.000"
    p = binomtest(min(b_pf, c_fp), n, 0.5, alternative="two-sided").pvalue
    star = "***" if p < 0.001 else "**" if p < 0.01 else "*" if p < 0.05 else "ns"
    return f"base→final {base}→{final}  pass→fail={b_pf}  fail→pass={c_fp}  McNemar exact p={p:.4f} [{star}]"


runs = {name: (load(path), kind) for name, (path, kind) in RUNS.items()}
groups = [("OVERALL", list(strata)),
          ("LOWER", [t for t in strata if strata[t] == "lower"]),
          ("HIGHER", [t for t in strata if strata[t] == "higher"])]

def report(title, run_map):
    for label, ids in groups:
        print("\n" + "=" * 78)
        print(f"  {title} -- {label}  (n={len(ids)})")
        print("=" * 78)
        for name, (by, kind) in run_map.items():
            gids = [t for t in ids if t in by]
            print(f"\n  --- {name}  (n={len(gids)}) ---")
            print(f"    H3 correctness  : {mcnemar(by, kind, gids)}")
            for mlabel, key in METRICS:
                print(f"    {mlabel} : {wilcox(deltas(by, kind, gids, key))}")


report("PRIMARY", runs)

# Secondary ablation family, only if the blind runs have been produced.
secondary = {name: (load(path), kind) for name, (path, kind) in SECONDARY_RUNS.items()
             if (PROJECT / path).exists()}
if secondary:
    report("SECONDARY (code-blind ablation)", secondary)

print("\n" + "-" * 78)
print("Wilcoxon signed-rank (two-sided) on paired final-baseline; zero diffs dropped.")
print("McNemar exact (binomial on discordant pairs). * p<.05  ** p<.01  *** p<.001.")
print("CAVEAT: n=63 (higher=23), single model (qwen2.5-coder:7b), one seed. PRIMARY")
print("family = 12 tests (3 runs x [MI,CC,CogC,correctness]); Bonferroni alpha* =")
print("0.05/12 ~ 0.004. Under it CogC (all runs), MI (all runs), and comment-stripping")
print("CC survive; guarded/preserving CC do not. The code-blind runs form a SEPARATE")
print("SECONDARY family = 8 tests (2 runs x 4); its own Bonferroni alpha* = 0.05/8 ~")
print("0.006, under which blind and guarded-blind CogC survive (p=.0007 / .005) and")
print("blind MI survives. Per-stratum results are secondary/exploratory.")
