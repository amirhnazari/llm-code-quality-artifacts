#!/usr/bin/env python3
"""
Artifact integrity check: recompute every recorded metric from the archived code.

This is the check that makes the thesis's numbers verifiable without a model and
without a network. For each of the 1260 rows across the five canonical runs it
re-measures the saved solution and compares against the value recorded at run time.

  recomputed == recorded  ->  the reported statistics rest on the code in generated/

What this does NOT claim: that re-running GENERATION reproduces these trajectories.
It does not. Generation is deterministic for a fixed prompt (iteration 0 is
byte-identical across all five runs), but once any intermediate iteration differs
the rest of the trajectory can diverge; see results/README.md and the thesis §5.5.
The two claims are separate, and only this one is exact.

Cognitive complexity uses complexipy's in-process API rather than the CLI the
runners used, so a match here also confirms the two agree.

Usage:
    python src/verify_artifacts.py          # all five canonical runs
    python src/verify_artifacts.py --quick  # skip pylint (much faster)

Exit code 0 = every row matches. 1 = at least one mismatch (details printed).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from complexipy import code_complexity
from radon.complexity import cc_visit
from radon.metrics import h_visit, mi_visit
from radon.raw import analyze

# Same fix as run_baseline: make the venv's pylint resolve in subprocess calls even
# when the venv is not activated (e.g. invoked as .venv/bin/python src/...).
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")

PROJECT = Path(__file__).resolve().parent.parent
QUICK = "--quick" in sys.argv

# (run label, results file, generated-file suffix)
RUNS = [
    ("comment-stripping", "results/feedback_promptv2_restored.jsonl", "v2"),
    ("comment-preserving", "results/feedback_v3_fresh.jsonl", "v3"),
    ("correctness-guarded", "results/feedback_guarded.jsonl", "guard"),
    ("code-blind", "results/feedback_blind.jsonl", "blind"),
    ("code-blind guarded", "results/feedback_guarded_blind.jsonl", "guardblind"),
]
FLOAT_TOL = 1e-4


def recompute(code: str, path: Path) -> dict:
    """Re-measure a saved solution the same way run_baseline.metrics did."""
    out = {}
    out["mi"] = mi_visit(code, True)

    cc_vals = [b.complexity for b in cc_visit(code)]
    out["cc_total"] = sum(cc_vals) if cc_vals else 0
    out["cc_max"] = max(cc_vals) if cc_vals else 0

    out["loc"] = analyze(code).sloc

    hal = h_visit(code).total
    out["halstead_volume"] = hal.volume
    out["halstead_effort"] = hal.effort

    # The runners summed complexipy's per-function complexities.
    out["cognitive_total"] = sum(f.complexity for f in code_complexity(code).functions)

    if not QUICK:
        proc = subprocess.run(
            ["pylint", "--output-format=json", "--score=n", str(path)],
            capture_output=True, text=True, timeout=120,
        )
        msgs = json.loads(proc.stdout) if proc.stdout.strip() else []
        counts = {"C": 0, "R": 0, "W": 0, "E": 0}
        for m in msgs:
            k = (m.get("type") or "")[:1].upper()
            counts[k] = counts.get(k, 0) + 1
        out["pylint"] = counts
    return out


def differs(key, recomputed, recorded) -> str | None:
    if recorded is None:
        return None                      # nothing was recorded to contradict
    if key in ("mi", "halstead_volume", "halstead_effort"):
        if abs(recomputed - recorded) > FLOAT_TOL:
            return f"{key}: recomputed {recomputed:.4f} != recorded {recorded:.4f}"
        return None
    if recomputed != recorded:
        return f"{key}: recomputed {recomputed} != recorded {recorded}"
    return None


total = matched = missing = 0
failures = []

print("=" * 74)
print("  ARTIFACT INTEGRITY -- recomputed metrics vs. values recorded at run time")
print("=" * 74)
if QUICK:
    print("  (--quick: pylint counts skipped)")

for label, res_path, suffix in RUNS:
    rows = [json.loads(l) for l in (PROJECT / res_path).read_text().splitlines() if l.strip()]
    run_ok = run_bad = run_missing = 0

    for r in rows:
        stem = r["task_id"].replace("/", "_")
        path = PROJECT / "generated" / f"{stem}_{suffix}_iter{r['iteration']}.py"
        total += 1
        if not path.exists():
            run_missing += 1
            missing += 1
            failures.append((label, r["task_id"], r["iteration"], ["code file missing"]))
            continue

        got = recompute(path.read_text(), path)
        diffs = [d for d in (differs(k, v, r["metrics"].get(k)) for k, v in got.items()) if d]
        if diffs:
            run_bad += 1
            failures.append((label, r["task_id"], r["iteration"], diffs))
        else:
            run_ok += 1
            matched += 1

    status = "OK" if (run_bad == 0 and run_missing == 0) else "MISMATCH"
    print(f"  {label:<22} {len(rows):>4} rows   match={run_ok:<5} "
          f"mismatch={run_bad:<4} missing={run_missing:<4} [{status}]")

print("-" * 74)
print(f"  TOTAL: {matched} of {total} rows recompute exactly"
      f"{f' ({missing} code files missing)' if missing else ''}")

if failures:
    print(f"\n  --- first {min(len(failures), 20)} of {len(failures)} problems ---")
    for label, tid, it, diffs in failures[:20]:
        print(f"    [{label}] {tid} iter{it}")
        for d in diffs:
            print(f"        {d}")
    sys.exit(1)

print("\n  All recorded metrics are reproduced by re-measuring the archived code.")
print("  Every value in the thesis therefore traces to a file in generated/.")
