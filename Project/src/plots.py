#!/usr/bin/env python3
"""
Phase 4 figures for the Results section. Writes vector PDFs into ../figures/:

  fig_delta_boxplots.pdf  -- per-task paired delta (final - baseline) for MI, CC,
                             CogC, one box per run (v2 / v3 / guarded). The core
                             H1/H2 figure: shows MI drifting negative while CogC
                             concentrates below zero (reductions).
  fig_correctness.pdf     -- baseline vs final #passed per run (H3): the unguarded
                             runs lose solutions; the guarded run does not.
  fig_cogc_scatter.pdf    -- guarded run, baseline vs final cognitive complexity
                             per task. Points below the diagonal = safe reductions;
                             colour = still-correct vs not.

Figures are greyscale/print-friendly. Matched to stats.py so numbers agree.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

PROJECT = Path(__file__).resolve().parent.parent
FIGDIR = PROJECT.parent / "figures"
FIGDIR.mkdir(exist_ok=True)
strata = {t["task_id"]: t["stratum"] for t in json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())}

# Canonical runs (v2/v3 = fresh reproducible re-runs; guarded = recorded, intact).
RUNS = {
    "v2": ("results/feedback_promptv2_restored.jsonl", "plain"),
    "v3": ("results/feedback_v3_fresh.jsonl", "plain"),
    "guarded": ("results/feedback_guarded.jsonl", "guarded"),
}

# The RUNS keys are internal run identifiers and must stay as they are -- they select
# the carry-forward semantics ("plain" vs "guarded") and index the marker/linestyle
# maps below. They are NOT reader-facing: "v2"/"v3" appear nowhere in the thesis. Every
# chart label therefore goes through DISPLAY, which uses the same short names as
# tab:supp so a reader can map figure to table without a key.
DISPLAY = {"v2": "strip", "v3": "preserve", "guarded": "guarded"}
plt.rcParams.update({"font.size": 10, "axes.grid": True, "grid.alpha": 0.3,
                     "figure.dpi": 150, "savefig.bbox": "tight"})


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
    if kind == "guarded":
        return bm, f["best_metrics"], b["passed"], f["best_passed"]
    return bm, f["metrics"], b["passed"], f["passed"]


def deltas(by, kind, key):
    ds = []
    for t in by:
        bm, fm, *_ = pair(by, kind, t)
        if bm.get(key) is not None and fm.get(key) is not None:
            ds.append(fm[key] - bm[key])
    return ds


runs = {name: (load(path), kind) for name, (path, kind) in RUNS.items()}
names = list(runs)
labels = [DISPLAY[n] for n in names]

# ---------- Figure 1: paired-delta boxplots ----------
metrics = [("Maintainability Index", "mi", "H1"),
           ("Cyclomatic Complexity", "cc_total", "H2"),
           ("Cognitive Complexity", "cognitive_total", "H2")]
fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.6))
for ax, (title, key, hyp) in zip(axes, metrics):
    data = [deltas(by, kind, key) for name, (by, kind) in runs.items()]
    bp = ax.boxplot(data, tick_labels=labels, showmeans=True, widths=0.6,
                    medianprops=dict(color="black", lw=1.5),
                    meanprops=dict(marker="D", markerfacecolor="white",
                                   markeredgecolor="black", markersize=5),
                    flierprops=dict(marker=".", markersize=4, alpha=0.5))
    for patch in bp["boxes"]:
        patch.set_alpha(0.6)
    ax.axhline(0, color="red", lw=1, ls="--", alpha=0.7)
    ax.set_title(f"{title}  [{hyp}]")
    ax.set_ylabel("Δ  (final − baseline)")
fig.suptitle("Per-task paired change after 3 feedback iterations (n=63)", y=1.02)
fig.tight_layout()
fig.savefig(FIGDIR / "fig_delta_boxplots.pdf")
plt.close(fig)

# ---------- Figure 2: correctness base vs final ----------
fig, ax = plt.subplots(figsize=(5.2, 3.4))
base_vals, final_vals = [], []
for name, (by, kind) in runs.items():
    b = f = 0
    for t in by:
        _, _, bp, fp = pair(by, kind, t)
        b += bp; f += fp
    base_vals.append(b); final_vals.append(f)
x = range(len(names)); w = 0.38
ax.bar([i - w / 2 for i in x], base_vals, w, label="baseline", color="0.6", edgecolor="black")
ax.bar([i + w / 2 for i in x], final_vals, w, label="final", color="0.3", edgecolor="black")
for i, (bv, fv) in enumerate(zip(base_vals, final_vals)):
    ax.text(i - w / 2, bv + 0.3, str(bv), ha="center", fontsize=9)
    ax.text(i + w / 2, fv + 0.3, str(fv), ha="center", fontsize=9)
ax.set_xticks(list(x)); ax.set_xticklabels(labels)
ax.set_ylabel("# tasks passing MBPP+  (of 63)")
ax.set_title("Functional correctness: baseline vs final  [H3]")
ax.legend()
fig.savefig(FIGDIR / "fig_correctness.pdf")
plt.close(fig)

# ---------- Figure 3: guarded CogC baseline vs final scatter ----------
by, kind = runs["guarded"]
fig, ax = plt.subplots(figsize=(4.8, 4.6))
for correct, color, lab in [(True, "0.2", "correct (final)"), (False, "0.65", "incorrect (final)")]:
    xs, ys = [], []
    for t in by:
        bm, fm, _, fp = pair(by, kind, t)
        if bm.get("cognitive_total") is not None and fm.get("cognitive_total") is not None and fp == correct:
            xs.append(bm["cognitive_total"]); ys.append(fm["cognitive_total"])
    ax.scatter(xs, ys, s=32, c=color, edgecolor="black", lw=0.4, label=lab, alpha=0.85)
lim = max(ax.get_xlim()[1], ax.get_ylim()[1])
ax.plot([0, lim], [0, lim], "r--", lw=1, alpha=0.7, label="no change")
ax.set_xlim(0, lim); ax.set_ylim(0, lim)
ax.set_xlabel("baseline cognitive complexity")
ax.set_ylabel("final cognitive complexity")
ax.set_title("Guarded loop: CogC per task\n(below diagonal = simplified, safely)")
ax.legend(fontsize=8, loc="upper left")
fig.savefig(FIGDIR / "fig_cogc_scatter.pdf")
plt.close(fig)

# ---------- Figure 4: iteration trajectory (mean metric vs iteration) ----------
def series(by, kind, key):
    """Mean metric value at each iteration 0..3 (best-so-far for guarded)."""
    out = []
    for it in range(4):
        vals = []
        for t, its in by.items():
            r = its.get(it)
            if not r:
                continue
            m = r["best_metrics"] if (kind == "guarded" and "best_metrics" in r) else r["metrics"]
            if m.get(key) is not None:
                vals.append(m[key])
        out.append(sum(vals) / len(vals) if vals else None)
    return out


markers = {"v2": "o", "v3": "s", "guarded": "^"}
# Drawn at the paper's actual column width (3.34 in) so LaTeX renders it 1:1.
# It was previously 9.0 in wide and scaled down by ~2.7x at \columnwidth, which
# shrank the 10 pt tick labels to under 4 pt and made the panel unreadable in print.
# Font sizes below are therefore the true printed sizes -- do not enlarge the
# figsize without shrinking them to match.
with plt.rc_context({"font.size": 7, "axes.titlesize": 7.5, "axes.labelsize": 7,
                     "xtick.labelsize": 6.5, "ytick.labelsize": 6.5}):
    fig, axes = plt.subplots(1, 2, figsize=(3.34, 1.85))
    for ax, (title, key) in zip(axes, [("Cognitive complexity", "cognitive_total"),
                                       ("Maintainability Index", "mi")]):
        for name, (by, kind) in runs.items():
            ys = series(by, kind, key)
            ax.plot(range(4), ys, marker=markers[name], color="black",
                    ls={"v2": ":", "v3": "--", "guarded": "-"}[name],
                    label=DISPLAY[name], markerfacecolor="white", markersize=3.2, lw=1.0)
        ax.set_xticks(range(4))
        ax.set_xlabel("iteration")
        ax.set_title(title)
    axes[0].set_ylabel("mean over 63 tasks")
    axes[0].legend(fontsize=5.8, handlelength=2.2, borderpad=0.3, labelspacing=0.25)
    fig.tight_layout(pad=0.3, w_pad=0.8)
    fig.savefig(FIGDIR / "fig_trajectory.pdf")
    plt.close(fig)

# convergence stat: of CogC-changed tasks, fraction reaching final value by iter1
print("CogC convergence (of tasks whose CogC changed, share final by iter1):")
for name, (by, kind) in runs.items():
    changed = reach1 = 0
    for t, its in by.items():
        def cog(it):
            r = its.get(it)
            if not r:
                return None
            m = r["best_metrics"] if (kind == "guarded" and "best_metrics" in r) else r["metrics"]
            return m.get("cognitive_total")
        c0, c1, c3 = cog(0), cog(1), cog(3)
        if None in (c0, c1, c3) or c3 == c0:
            continue
        changed += 1
        reach1 += (c1 == c3)
    print(f"  {name}: {reach1}/{changed}")

print("Wrote:")
for f in ("fig_delta_boxplots.pdf", "fig_correctness.pdf", "fig_cogc_scatter.pdf", "fig_trajectory.pdf"):
    print(f"  figures/{f}")
