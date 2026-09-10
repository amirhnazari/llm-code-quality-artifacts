#!/usr/bin/env python3
"""
Code-BLIND static-analysis feedback loop (feedback-content ablation).

This is the variant Prof. Doehring asked for. It is identical to run_feedback.py
EXCEPT that the model is NOT shown its previous code between iterations. It sees
only the task and the SCALAR static-analysis findings of the previous attempt
(MI / CC / CogC totals + Pylint counts by category), and is asked to produce a
fresh, simpler solution. The line-anchored Pylint messages are dropped on purpose:
"line 7: too-many-branches" is meaningless without the code it points at.

So the contrast against run_feedback.py isolates ONE factor:
  run_feedback.py        = code-aware "refactor THIS code" (code + findings)
  run_feedback_blind.py  = code-blind  "regenerate, but simpler" (findings only)

For each task:
  iteration 0     = baseline generation (identical to run_baseline / run_feedback)
  iterations 1..N = feed the task + the previous attempt's scalar findings (no
                    code), ask for a new solution, re-measure.

"final" = last iteration (feed-latest), so this is an UNGUARDED, "plain"-kind run
in stats.py terms -- directly comparable to feedback.jsonl / feedback_promptv2.jsonl.

One JSON line per (task, iteration) -> results/feedback_blind.jsonl.
Reuses generation / correctness / metric helpers from run_baseline.
"""
from __future__ import annotations

import json
import re
import time

import run_baseline as base

CONFIG = base.CONFIG
TASKS = base.TASKS
GEN = base.GEN_DIR
RES = base.RES_DIR
MAX_ITERS = CONFIG.get("max_iterations", 3)


def blind_prompt(m: dict, task: dict) -> str:
    """Feedback prompt WITHOUT the previous code -- only the scalar findings."""
    mi = m.get("mi")
    pl = m.get("pylint", {}) or {}
    lines = [
        "A previous attempt at the task below was analysed by a static-analysis "
        "tool. You are NOT shown that previous code -- only its measured scores:",
        f"- Maintainability Index: {round(mi, 1) if mi is not None else 'n/a'} (0-100, higher is better)",
        f"- Cyclomatic complexity (total): {m.get('cc_total')} (independent branches; lower is simpler)",
        f"- Cognitive complexity (total): {m.get('cognitive_total')} (penalises deep/nested control flow; lower is easier to follow)",
        f"- Pylint issue counts: {pl.get('C', 0)} convention, {pl.get('R', 0)} refactor, "
        f"{pl.get('W', 0)} warning, {pl.get('E', 0)} error",
        "",
        "Write a NEW solution to the task that is simpler than that previous attempt: "
        "lower cyclomatic and cognitive complexity. Flatten nested loops and "
        "conditionals, remove redundant branches, and use clear idiomatic Python "
        "(comprehensions, built-ins, early returns) where it genuinely simplifies the "
        "control flow. Keep the EXACT same function signature (same name AND parameters) "
        "and the same behaviour. Include a short docstring.",
        ("Task:\n" + task["prompt"].strip()) if task.get("kind") == "mbpp"
        else ("It must pass these tests:\n" + "\n".join(task["tests"])),
        "",
        "Respond with ONLY a Python code block.",
    ]
    return "\n".join(lines)


def main():
    out = RES / "feedback_blind.jsonl"
    with out.open("w") as fh:
        for task in TASKS:
            stem = re.sub(r"\W", "_", task["task_id"])
            print(f"\n=== {task['task_id']} ===", flush=True)
            m = None
            for it in range(0, MAX_ITERS + 1):
                t0 = time.time()
                if it == 0:
                    resp = base.generate(base.build_prompt(task))
                else:
                    resp = base.generate(blind_prompt(m, task))
                code = base.extract_code(resp.get("response", ""))
                cp = GEN / f"{stem}_blind_iter{it}.py"
                cp.write_text(code + "\n")

                correctness = base.check_correctness(cp, task)
                m = base.metrics(cp)
                row = {
                    "task_id": task["task_id"],
                    "iteration": it,
                    "passed": correctness["passed"],
                    "metrics": m,
                    "gen_seconds": round(time.time() - t0, 1),
                }
                fh.write(json.dumps(row) + "\n")
                fh.flush()
                mi = m.get("mi")
                print(
                    f"  iter{it}: pass={correctness['passed']:<5} "
                    f"MI={round(mi, 1) if mi is not None else 'n/a':<6} "
                    f"CC={m.get('cc_total')}  CogC={m.get('cognitive_total')}  "
                    f"pylintC={m.get('pylint', {}).get('C')}",
                    flush=True,
                )
    print(f"\nDone -> {out}")


if __name__ == "__main__":
    main()
