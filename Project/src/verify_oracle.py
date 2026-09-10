#!/usr/bin/env python3
"""
Oracle validation: evidence that the correctness check itself is sound.

H3 rests entirely on the MBPP+ oracle in mbpp_data.check_mbpp, so the oracle's own
correctness is worth establishing rather than assuming. Three properties are checked
across all 63 frozen tasks:

  1. NO FALSE NEGATIVES. Each task's canonical reference solution is submitted to the
     oracle as if it were a candidate. It must pass. A reference that failed its own
     oracle would mean the harness rejects correct code.

  2. NO FALSE POSITIVES. A deliberately broken mutant of each reference (its return
     value is corrupted) is submitted. It must fail. An oracle that accepted these
     would not be testing anything.

  3. THE AUGMENTED INPUTS DISCRIMINATE. MBPP+ adds generated inputs on top of the
     benchmark's originals. This reports how many of each the 63 tasks carry, and
     how many of the archived baseline solutions pass on the original inputs but
     fail once the augmented ones are included -- i.e. how many would have been
     scored correct by the weaker check the original benchmark ships with.

Property 3 is a measurement, not a pass/fail assertion: it quantifies what the
augmentation buys rather than asserting a threshold.

Needs no model and no network -- only the MBPP+ data and the archived solutions.

Usage:  python src/verify_oracle.py
Exit 0 = properties 1 and 2 hold for every task.
"""
from __future__ import annotations

import json
import re
import sys
import tempfile
from pathlib import Path

import mbpp_data

PROJECT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((PROJECT / "config.json").read_text())
TASKS = mbpp_data.load_mbpp_tasks()


def run_oracle(code: str, task: dict) -> bool:
    """Submit a source string to the real oracle as if it were a candidate."""
    tmp = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir=str(PROJECT))
    try:
        tmp.write(code)
        tmp.close()
        return mbpp_data.check_mbpp(Path(tmp.name), task, CONFIG)["passed"]
    finally:
        try:
            Path(tmp.name).unlink()
        except OSError:
            pass


def break_it(code: str, entry: str) -> str | None:
    """Append an override that returns a value the reference cannot produce.

    Redefining the entry point after the original definition shadows it, so the
    oracle sees a function with the right name and the wrong behaviour.
    """
    if not re.search(rf"def\s+{re.escape(entry)}\s*\(", code):
        return None
    return code + (
        f"\n\ndef {entry}(*args, **kwargs):  # deliberately broken mutant\n"
        f"    return '__WRONG__'\n"
    )


print("=" * 74)
print("  ORACLE VALIDATION -- does the correctness check accept and reject correctly?")
print("=" * 74)

# --- Property 1: the reference passes its own oracle -----------------------
ref_pass, ref_fail = 0, []
for t in TASKS:
    if run_oracle(t["canonical_solution"], t):
        ref_pass += 1
    else:
        ref_fail.append(t["task_id"])
print(f"\n  1. Reference solution passes its own oracle : {ref_pass}/{len(TASKS)}")
if ref_fail:
    print(f"     FAILED on: {ref_fail[:10]}")

# --- Property 2: a broken mutant is rejected -------------------------------
mut_reject, mut_accept, mut_skip = 0, [], 0
for t in TASKS:
    mutant = break_it(t["canonical_solution"], t["entry_point"])
    if mutant is None:
        mut_skip += 1
        continue
    if run_oracle(mutant, t):
        mut_accept.append(t["task_id"])
    else:
        mut_reject += 1
print(f"  2. Broken mutant rejected                   : "
      f"{mut_reject}/{len(TASKS) - mut_skip}"
      f"{f'  ({mut_skip} skipped: entry point not found)' if mut_skip else ''}")
if mut_accept:
    print(f"     WRONGLY ACCEPTED: {mut_accept[:10]}")

# --- Property 3: what the augmented inputs add -----------------------------
raw = mbpp_data._mbpp()
n_base = sum(len(raw[t["task_id"]].get("base_input", []) or []) for t in TASKS)
n_plus = sum(len(raw[t["task_id"]].get("plus_input", []) or []) for t in TASKS)
print(f"\n  3. Test inputs over the 63 tasks            : "
      f"{n_base} original + {n_plus} augmented = {n_base + n_plus}")

# How many archived baselines pass on the original inputs alone but fail overall?
by = {}
for line in (PROJECT / "results" / "feedback_guarded.jsonl").read_text().splitlines():
    if line.strip():
        r = json.loads(line)
        by.setdefault(r["task_id"], {})[r["iteration"]] = r

caught = base_only_pass = 0
for t in TASKS:
    row = by.get(t["task_id"], {}).get(0)
    if row is None:
        continue
    stem = t["task_id"].replace("/", "_")
    path = PROJECT / "generated" / f"{stem}_guard_iter0.py"
    if not path.exists():
        continue
    base_only = dict(t, inputs=list(raw[t["task_id"]].get("base_input", []) or []))
    passes_base = run_oracle(path.read_text(), base_only)
    if passes_base:
        base_only_pass += 1
        if not row["passed"]:
            caught += 1

print(f"     Baseline solutions passing the ORIGINAL inputs only : {base_only_pass}/63")
print(f"     Of those, caught out by the augmented inputs        : {caught}")
print(f"     (i.e. {caught} solutions the original benchmark would have scored correct)")

print("\n" + "-" * 74)
if ref_fail or mut_accept:
    print("  FAILED: the oracle does not behave as required.")
    sys.exit(1)
print("  Properties 1 and 2 hold for every task: the oracle accepts every correct")
print("  reference and rejects every deliberately broken mutant.")
