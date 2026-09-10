#!/usr/bin/env python3
"""
v3 (comment-preserving) feedback loop -- FRESH re-run for the reproducibility
check, with collision-free filenames.

Identical loop to run_feedback.py (same current v3 prompt via fb.feedback_prompt),
but writes to {stem}_v3_iter{it}.py and results/feedback_v3_fresh.jsonl so it
neither reads nor overwrites the original recorded feedback.jsonl / {stem}_iter*.py.

Purpose: run v3 fresh under the SAME current tooling as the fresh v2 run
(run_feedback_v2.py -> feedback_promptv2_restored.jsonl) so the comment-stripping
vs comment-preserving MI contrast can be tested on fully reproducible, archivable
data. See PROGRESS.md question #8.
"""
from __future__ import annotations

import json
import re
import time

import run_baseline as base
import run_feedback as fb

CONFIG = base.CONFIG
TASKS = base.TASKS
GEN = base.GEN_DIR
RES = base.RES_DIR
MAX_ITERS = CONFIG.get("max_iterations", 3)


def main():
    out = RES / "feedback_v3_fresh.jsonl"
    with out.open("w") as fh:
        for task in TASKS:
            stem = re.sub(r"\W", "_", task["task_id"])
            print(f"\n=== {task['task_id']} ===", flush=True)
            code, m, pmsgs = None, None, None
            for it in range(0, MAX_ITERS + 1):
                t0 = time.time()
                if it == 0:
                    resp = base.generate(base.build_prompt(task))
                else:
                    resp = base.generate(fb.feedback_prompt(code, m, pmsgs, task))
                code = base.extract_code(resp.get("response", ""))
                cp = GEN / f"{stem}_v3_iter{it}.py"
                cp.write_text(code + "\n")

                correctness = base.check_correctness(cp, task)
                m = base.metrics(cp)
                pmsgs = fb.pylint_messages(cp)
                row = {
                    "task_id": task["task_id"],
                    "iteration": it,
                    "passed": correctness["passed"],
                    "metrics": m,
                    "pylint_symbols": [msg.get("symbol") for msg in pmsgs],
                    "gen_seconds": round(time.time() - t0, 1),
                }
                fh.write(json.dumps(row) + "\n")
                fh.flush()
                mi = m.get("mi")
                print(
                    f"  iter{it}: pass={correctness['passed']:<5} "
                    f"MI={round(mi, 1) if mi is not None else 'n/a':<6} "
                    f"CC={m.get('cc_total')}  CogC={m.get('cognitive_total')}",
                    flush=True,
                )
    print(f"\nDone -> {out}")


if __name__ == "__main__":
    main()
