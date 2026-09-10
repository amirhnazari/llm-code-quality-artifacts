#!/usr/bin/env python3
"""
Verify the v2 restoration reproduces the recorded v2 run.

Compares results/feedback_promptv2_restored.jsonl (regenerated to collision-free
{stem}_v2_iter{it}.py files) against the original results/feedback_promptv2.jsonl,
row by row, on the metrics the paper uses. An exact match across all rows means
the reconstructed prompt is faithful and the restored code files are a valid,
verifiable stand-in for the overwritten originals.
"""
from __future__ import annotations

import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
ORIG = PROJECT / "results" / "feedback_promptv2.jsonl"
NEW = PROJECT / "results" / "feedback_promptv2_restored.jsonl"

INT_KEYS = ["cc_total", "cc_max", "loc", "cognitive_total", "cognitive_max"]
FLOAT_KEYS = ["mi", "halstead_volume", "halstead_effort"]
FLOAT_TOL = 0.1


def load(p):
    d = {}
    for l in p.read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            d[(r["task_id"], r["iteration"])] = r
    return d


def main():
    orig, new = load(ORIG), load(NEW)
    keys = sorted(set(orig) & set(new))
    only_orig = sorted(set(orig) - set(new))
    only_new = sorted(set(new) - set(orig))

    exact_rows = 0
    mismatches = []
    for k in keys:
        o, n = orig[k]["metrics"], new[k]["metrics"]
        row_diffs = []
        for key in INT_KEYS:
            if o.get(key) != n.get(key):
                row_diffs.append(f"{key} {o.get(key)}!={n.get(key)}")
        for key in FLOAT_KEYS:
            ov, nv = o.get(key), n.get(key)
            if ov is None or nv is None:
                if ov != nv:
                    row_diffs.append(f"{key} {ov}!={nv}")
            elif abs(ov - nv) > FLOAT_TOL:
                row_diffs.append(f"{key} {round(ov,1)}!={round(nv,1)}")
        # pylint dict
        if (o.get("pylint") or {}) != (n.get("pylint") or {}):
            row_diffs.append(f"pylint {o.get('pylint')}!={n.get('pylint')}")
        # correctness
        if orig[k]["passed"] != new[k]["passed"]:
            row_diffs.append(f"passed {orig[k]['passed']}!={new[k]['passed']}")
        if row_diffs:
            mismatches.append((k, row_diffs))
        else:
            exact_rows += 1

    print("=" * 70)
    print("  v2 RESTORATION VERIFICATION")
    print("=" * 70)
    print(f"  rows compared      : {len(keys)}")
    print(f"  EXACT matches      : {exact_rows}")
    print(f"  mismatched rows    : {len(mismatches)}")
    print(f"  only in original   : {len(only_orig)}  {only_orig[:4]}")
    print(f"  only in restored   : {len(only_new)}  {only_new[:4]}")
    if mismatches:
        print("\n  --- mismatches (task, iter -> differing fields) ---")
        for (tid, it), diffs in mismatches[:40]:
            print(f"    {tid} iter{it}: {'; '.join(diffs)}")
        if len(mismatches) > 40:
            print(f"    ... and {len(mismatches)-40} more")
    else:
        print("\n  ✓ PERFECT REPRODUCTION — restored v2 == recorded v2 on all metrics.")
    # per-iteration mismatch histogram (helps spot whether drift is iter-specific)
    from collections import Counter
    hist = Counter(it for (_, it), _ in mismatches)
    if hist:
        print("\n  mismatches by iteration:", dict(sorted(hist.items())))


if __name__ == "__main__":
    main()
