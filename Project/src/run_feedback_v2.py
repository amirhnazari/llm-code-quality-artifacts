#!/usr/bin/env python3
"""
v2 (comment-stripping) feedback loop -- RESTORATION runner.

The original v2 run wrote its code to {stem}_iter{it}.py, the same filenames the
later v3 (comment-preserving) run used, so v3 overwrote v2's code on disk. The
exact v2 prompt was an uncommitted intermediate and is not in git. This runner
reconstructs it: the current v3 feedback_prompt STRUCTURE with the comment
instruction reverted to the original comment-DISCOURAGING wording preserved in
commit 35ac065 (which is what drove the model to strip comments -> the large MI
drop that defines the comment-stripping ablation).

It writes to COLLISION-FREE names ({stem}_v2_iter{it}.py) and a separate JSONL
(results/feedback_promptv2_restored.jsonl) so nothing is overwritten. Because
generation is deterministic (temp 0, fixed seed; iteration 0 is byte-identical
across the original v2/v3 runs), a faithful prompt reproduces the recorded v2
metrics exactly -- which is then checked by verify_v2_restore.py.

Only the comment instruction differs from run_feedback.py; everything else
(baseline generation, task set, iteration cap, measurement) is shared via
run_baseline / run_feedback.
"""
from __future__ import annotations

import json
import os
import re
import time

import run_baseline as base
import run_feedback as fb

CONFIG = base.CONFIG
TASKS = base.TASKS
GEN = base.GEN_DIR
RES = base.RES_DIR
MAX_ITERS = CONFIG.get("max_iterations", 3)

# The v2/v3 difference was "comment handling only" (PROGRESS.md). v3 ends its
# refactor instruction with an explicit KEEP-comments sentence; v2 (comment-
# stripping) did not. Two candidate reconstructions of the v2 wording, selectable
# via THESIS_V2_VARIANT so we can test which reproduces the recorded v2 metrics:
#   none       -> v3 minus the keep-comments sentence (minimal change)
#   discourage -> plus an explicit "comments do NOT reduce complexity" sentence
#
# WHICH ONE PRODUCED THE CANONICAL RUN IS NOT RECORDED. The variant used for
# results/feedback_promptv2_restored.jsonl was not logged, and the JSONL rows do not
# store the prompt. The thesis therefore describes this configuration only by what
# both variants share -- it does not instruct the model to preserve comments -- and
# never claims the stronger "actively discourages" wording, which is true of the
# 'discourage' variant only. The label "comment-stripping" is safe either way: it is
# an observed OUTCOME of the archived run, where comment+docstring lines fall from
# 268 at iteration 0 to 78 at iteration 3, against 268 -> 324 for v3.
V2_VARIANT = os.environ.get("THESIS_V2_VARIANT", "none")
_COMMENT_CLAUSE = {
    "none": "",
    "discourage": " Simply adding a docstring or comments does NOT reduce "
                  "complexity and is not sufficient---change the structure of the code.",
}[V2_VARIANT]


def feedback_prompt_v2(prev_code: str, m: dict, pmsgs: list, task: dict) -> str:
    """v3 prompt verbatim EXCEPT the trailing comment instruction (see V2_VARIANT)."""
    mi = m.get("mi")
    lines = [
        "Your previous Python solution was:",
        "```python\n" + prev_code.strip() + "\n```",
        "",
        "A static-analysis tool reported the following on that solution:",
        f"- Maintainability Index: {round(mi, 1) if mi is not None else 'n/a'} (0-100, higher is better)",
        f"- Cyclomatic complexity (total): {m.get('cc_total')} (independent branches; lower is simpler)",
        f"- Cognitive complexity (total): {m.get('cognitive_total')} (penalises deep/nested control flow; lower is easier to follow)",
    ]
    if pmsgs:
        lines.append("- Pylint findings:")
        for msg in pmsgs:
            lines.append(f"    line {msg.get('line')}: {msg.get('symbol')} -- {msg.get('message')}")
    else:
        lines.append("- Pylint findings: none")
    lines += [
        "",
        "Refactor only the internal logic of the function to reduce its cyclomatic and "
        "cognitive complexity: flatten nested loops and conditionals, remove redundant "
        "branches, and use clear idiomatic Python (comprehensions, built-ins, early "
        "returns) where it genuinely simplifies the control flow. "
        "Keep the EXACT same function signature (same name AND parameters) and the same "
        "behaviour." + _COMMENT_CLAUSE,
        ("Original task:\n" + task["prompt"].strip()) if task.get("kind") == "mbpp"
        else ("It must still pass these tests:\n" + "\n".join(task["tests"])),
        "",
        "Respond with ONLY a Python code block.",
    ]
    return "\n".join(lines)


def main():
    out = RES / "feedback_promptv2_restored.jsonl"
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
                    resp = base.generate(feedback_prompt_v2(code, m, pmsgs, task))
                code = base.extract_code(resp.get("response", ""))
                cp = GEN / f"{stem}_v2_iter{it}.py"
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
