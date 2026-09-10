#!/usr/bin/env python3
"""
Iterative static-analysis feedback loop (the core experiment).

For each task:
  iteration 0  = baseline generation (same as run_baseline)
  iterations 1..N = feed the model its previous code + the static-analysis
                    findings, ask it to refactor (same name + behaviour),
                    re-measure.

One JSON line per (task, iteration) -> results/feedback.jsonl, so the paired
baseline-vs-iteration trajectory for H1/H2/H3 is directly analysable.

Reuses generation / correctness / metric helpers from run_baseline.
"""
from __future__ import annotations

import json
import re
import subprocess
import time

import run_baseline as base

CONFIG = base.CONFIG
TASKS = base.TASKS
GEN = base.GEN_DIR
RES = base.RES_DIR
MAX_ITERS = CONFIG.get("max_iterations", 3)


def pylint_messages(code_path) -> list:
    """Detailed pylint findings (symbol/message/line) for the feedback prompt."""
    try:
        proc = subprocess.run(
            ["pylint", "--output-format=json", "--score=n", str(code_path)],
            capture_output=True, text=True, timeout=60,
        )
        return json.loads(proc.stdout) if proc.stdout.strip() else []
    except Exception:  # noqa: BLE001 - best effort
        return []


def feedback_prompt(prev_code: str, m: dict, pmsgs: list, task: dict) -> str:
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
        "behaviour. Keep any existing docstring and comments -- do not delete them.",
        ("Original task:\n" + task["prompt"].strip()) if task.get("kind") == "mbpp"
        else ("It must still pass these tests:\n" + "\n".join(task["tests"])),
        "",
        "Respond with ONLY a Python code block.",
    ]
    return "\n".join(lines)


def main():
    out = RES / "feedback.jsonl"
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
                    resp = base.generate(feedback_prompt(code, m, pmsgs, task))
                code = base.extract_code(resp.get("response", ""))
                cp = GEN / f"{stem}_iter{it}.py"
                cp.write_text(code + "\n")

                correctness = base.check_correctness(cp, task)
                m = base.metrics(cp)
                pmsgs = pylint_messages(cp)
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
                    f"CC={m.get('cc_total')}  CogC={m.get('cognitive_total')}  "
                    f"pylintC={m.get('pylint', {}).get('C')}",
                    flush=True,
                )
    print(f"\nDone -> {out}")


if __name__ == "__main__":
    main()
