#!/usr/bin/env python3
"""
Task selection for the real experiment.

Pool = MBPP+ (EvalPlus), 378 hand-verified tasks. For each task we measure the
structural complexity of its *reference* solution and keep only tasks with enough
maintainability/complexity headroom for the feedback loop to act on. Trivial
one-liners (which sit at the MI ceiling, as the prototype showed) are excluded.

Filter (tunable): cyclomatic complexity total >= CC_MIN AND sloc >= LOC_MIN,
excluding tasks whose reference solution needs I/O or non-stdlib libraries.

Writes the surviving candidate pool to tasks/mbpp_candidates.json for review.
Nothing is frozen yet — thresholds can be tightened after inspecting the pool.
"""
from __future__ import annotations

import json
import re
import statistics
from pathlib import Path

from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.raw import analyze
from evalplus.data import get_mbpp_plus

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "tasks" / "mbpp_candidates.json"

CC_MIN = 3
LOC_MIN = 5
# crude "needs I/O or non-stdlib" screen (math/re/collections/itertools/heapq stay)
BANNED = re.compile(
    r"\b(open|input|eval|exec)\s*\(|"
    r"\bimport\s+(os|sys|socket|requests|subprocess|urllib|pathlib|shutil)\b|"
    r"\bfrom\s+(os|sys|socket|requests|subprocess|urllib|pathlib|shutil)\b"
)


def measure(code: str) -> dict:
    out = {"cc_total": None, "cc_max": None, "loc": None, "mi": None}
    try:
        blocks = cc_visit(code)
        vals = [b.complexity for b in blocks]
        out["cc_total"] = sum(vals) if vals else 0
        out["cc_max"] = max(vals) if vals else 0
    except Exception:  # noqa: BLE001
        pass
    try:
        out["loc"] = analyze(code).sloc
    except Exception:  # noqa: BLE001
        pass
    try:
        out["mi"] = round(mi_visit(code, True), 1)
    except Exception:  # noqa: BLE001
        pass
    return out


def main():
    data = get_mbpp_plus()
    rows = []
    for tid, t in data.items():
        code = (t.get("canonical_solution") or "").strip()
        if not code:
            continue
        m = measure(code)
        excluded_io = bool(BANNED.search(code))
        keep = (
            not excluded_io
            and m["cc_total"] is not None
            and m["loc"] is not None
            and m["cc_total"] >= CC_MIN
            and m["loc"] >= LOC_MIN
        )
        rows.append({
            "task_id": tid,
            "entry_point": t.get("entry_point"),
            **m,
            "excluded_io": excluded_io,
            "keep": keep,
            "prompt": " ".join((t.get("prompt") or "").split())[:140],
        })

    kept = [r for r in rows if r["keep"]]
    print(f"MBPP+ pool: {len(rows)} tasks")
    print(f"  excluded (I/O / non-stdlib): {sum(r['excluded_io'] for r in rows)}")
    print(f"  trivial (below CC>={CC_MIN} or LOC>={LOC_MIN}): "
          f"{len(rows) - len(kept) - sum(r['excluded_io'] for r in rows)} (approx)")
    print(f"  KEPT: {len(kept)}")
    if kept:
        ccs = [r["cc_total"] for r in kept]
        locs = [r["loc"] for r in kept]
        print(f"  kept CC  -> min {min(ccs)}  median {statistics.median(ccs)}  max {max(ccs)}")
        print(f"  kept LOC -> min {min(locs)} median {statistics.median(locs)} max {max(locs)}")
        # rough complexity strata (for a balanced ~40-task draw later)
        low = [r for r in kept if r["cc_total"] <= 4]
        med = [r for r in kept if 5 <= r["cc_total"] <= 7]
        high = [r for r in kept if r["cc_total"] >= 8]
        print(f"  strata by CC: low(3-4)={len(low)}  med(5-7)={len(med)}  high(8+)={len(high)}")

    OUT.write_text(json.dumps(kept, indent=2))
    print(f"\n-> wrote {len(kept)} candidates to {OUT.relative_to(PROJECT)}")

    print("\n-- top 15 by cyclomatic complexity --")
    for r in sorted(kept, key=lambda x: -x["cc_total"])[:15]:
        print(f"  {r['task_id']:<10} CC={r['cc_total']:<3} LOC={r['loc']:<3} "
              f"MI={r['mi']:<6} {r['entry_point']}")


if __name__ == "__main__":
    main()
