#!/usr/bin/env python3
"""
Deeper look at results/feedback.jsonl:
  (A) best-iteration view (vs final-iteration), since we feed-latest and the loop
      can regress -- "final" may understate what the loop achieved.
  (B) mechanism inspection: the largest MI drops (iter0 vs iter3 code + radon raw
      breakdown) and the correctness regressions.
"""
from __future__ import annotations

import json
import re
import statistics as st
from pathlib import Path

from radon.raw import analyze

PROJECT = Path(__file__).resolve().parent.parent
GEN = PROJECT / "generated"
rows = [json.loads(l) for l in (PROJECT / "results" / "feedback.jsonl").read_text().splitlines() if l.strip()]
strata = {t["task_id"]: t["stratum"] for t in json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())}

by_task: dict = {}
for r in rows:
    by_task.setdefault(r["task_id"], {})[r["iteration"]] = r


def mi(row):
    return row["metrics"].get("mi")


# ---------- (A) best-iteration analysis ----------
print("=" * 60)
print("(A) BEST-ITERATION vs FINAL-ITERATION")
print("=" * 60)


def best_block(ids, label):
    n = len(ids)
    fin_mi_up = best_mi_up = 0
    fin_pass = peak_pass = base_pass = 0
    best_dmi = []
    for tid in ids:
        its = by_task[tid]
        b, f = its[min(its)], its[max(its)]
        base_pass += int(b["passed"]); fin_pass += int(f["passed"])
        peak_pass += int(any(its[i]["passed"] for i in its))
        if mi(b) is not None:
            if mi(f) is not None and mi(f) - mi(b) > 0.5:
                fin_mi_up += 1
            mis = [mi(its[i]) for i in its if mi(its[i]) is not None]
            if mis:
                d = max(mis) - mi(b); best_dmi.append(d)
                if d > 0.5:
                    best_mi_up += 1
    med = round(st.median(best_dmi), 2) if best_dmi else None
    print(f"\n{label} (n={n})")
    print(f"  correctness: baseline {base_pass} | final {fin_pass} | peak(any-iter) {peak_pass}")
    print(f"  MI improved: final {fin_mi_up}/{n}  vs  best-iteration {best_mi_up}/{n}")
    print(f"  best-iteration MI Δ median: {med}")


best_block(list(by_task), "OVERALL")
best_block([t for t in by_task if strata.get(t) == "lower"], "LOWER")
best_block([t for t in by_task if strata.get(t) == "higher"], "HIGHER")

# ---------- (B) mechanism: biggest MI drops ----------
print("\n" + "=" * 60)
print("(B) LARGEST MI DROPS (iter0 -> iter3) + raw breakdown")
print("=" * 60)
drops = []
for tid, its in by_task.items():
    b, f = its[min(its)], its[max(its)]
    if mi(b) is not None and mi(f) is not None:
        drops.append((mi(f) - mi(b), tid))
drops.sort()

for delta, tid in drops[:3]:
    stem = re.sub(r"\W", "_", tid)
    b, f = by_task[tid][0], by_task[tid][3]
    print(f"\n--- {tid}  MI {mi(b)} -> {mi(f)}  (Δ {round(delta,1)}) ---")
    for it in (0, 3):
        code = (GEN / f"{stem}_iter{it}.py").read_text()
        raw = analyze(code)
        print(f"  iter{it}: sloc={raw.sloc} comments={raw.comments} docstring/multi={raw.multi} "
              f"pass={by_task[tid][it]['passed']}")
    print("  --- iter0 code ---")
    print("    " + (GEN / f"{stem}_iter0.py").read_text().replace("\n", "\n    ").rstrip())
    print("  --- iter3 code ---")
    print("    " + (GEN / f"{stem}_iter3.py").read_text().replace("\n", "\n    ").rstrip())

# ---------- (B) correctness regressions ----------
print("\n" + "=" * 60)
print("(B) CORRECTNESS REGRESSIONS (passed baseline, failed final)")
print("=" * 60)
for tid, its in by_task.items():
    b, f = its[min(its)], its[max(its)]
    if b["passed"] and not f["passed"]:
        traj = [int(its[i]["passed"]) for i in sorted(its)]
        print(f"  {tid:<10} ({strata.get(tid)})  pass trajectory {traj}")
