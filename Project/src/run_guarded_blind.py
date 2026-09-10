#!/usr/bin/env python3
"""
Correctness-guarded, code-BLIND feedback loop.

Combines the correctness gate of run_guarded.py with the code-blind prompt of
run_feedback_blind.py. It tests the payoff the unguarded blind run implied: the
blind loop matched the code-aware loop on cognitive complexity but churned
correctness more (8 regressions and 3 repairs, against the canonical code-aware
run's 7 and 1). If the gate rolls those regressions back while keeping the CogC
reductions, blind regeneration becomes safe.

  iteration 0      = baseline generation (identical to the other runners).
  iterations 1..N  = show the model ONLY the scalar findings of the LAST ACCEPTED
                     (still-correct) version -- never its code -- and ask for a new,
                     simpler solution, then gate on correctness:
      - candidate still passes the oracle -> ACCEPT: becomes the new best.
      - candidate breaks correctness      -> REJECT: roll back to the last accepted
        version; the next attempt is told its change altered behaviour (a blind
        guard note), which perturbs the prompt so temperature 0 does not
        deterministically reproduce the same broken output.

By construction final correctness never drops below the baseline. Because the
model is code-blind, the "best" version is carried forward only as its SCORES,
not its source (consistent with the unguarded blind arm).

One JSON line per (task, iteration) -> results/feedback_guarded_blind.jsonl, with
the same fields as run_guarded.py so stats.py can read it as a "guarded"-kind run.
"""
from __future__ import annotations

import json
import re
import time

import run_baseline as base
import run_feedback_blind as fbb

CONFIG = base.CONFIG
TASKS = base.TASKS
GEN = base.GEN_DIR
RES = base.RES_DIR
MAX_ITERS = CONFIG.get("max_iterations", 3)

GUARD_NOTE = (
    "IMPORTANT: your PREVIOUS attempt was REJECTED by a regression test -- it "
    "changed the function's behaviour and no longer produced the correct output for "
    "every input. Produce a NEW solution that preserves the EXACT behaviour and "
    "function signature; simplify only control flow you are certain keeps identical "
    "outputs for all inputs. If in doubt, keep it straightforward and correct."
)


def main():
    out = RES / "feedback_guarded_blind.jsonl"
    with out.open("w") as fh:
        for task in TASKS:
            stem = re.sub(r"\W", "_", task["task_id"])
            print(f"\n=== {task['task_id']} ===", flush=True)

            best_m = None            # scores of the last accepted version (no code)
            best_passed = False
            best_iter = 0
            reject_streak = 0

            for it in range(0, MAX_ITERS + 1):
                t0 = time.time()
                if it == 0:
                    resp = base.generate(base.build_prompt(task))
                else:
                    prompt = fbb.blind_prompt(best_m, task)
                    if reject_streak:
                        prompt = f"{GUARD_NOTE}\n(This is retry #{reject_streak}.)\n\n" + prompt
                    resp = base.generate(prompt)

                code = base.extract_code(resp.get("response", ""))
                cp = GEN / f"{stem}_guardblind_iter{it}.py"
                cp.write_text(code + "\n")

                passed = base.check_correctness(cp, task)["passed"]
                m = base.metrics(cp)

                # --- correctness gate (identical policy to run_guarded) -------
                if it == 0:
                    accepted = True                       # baseline is the anchor
                else:
                    # accept unless it regresses correctness: if best is currently
                    # correct the candidate must stay correct; if best is already
                    # broken, anything is accepted (correctness cannot get worse).
                    accepted = passed or (not best_passed)

                if accepted:
                    best_m, best_passed, best_iter = m, passed, it
                    reject_streak = 0
                else:
                    reject_streak += 1                     # keep best_* untouched

                row = {
                    "task_id": task["task_id"],
                    "iteration": it,
                    "passed": passed,
                    "accepted": accepted,
                    "best_iteration": best_iter,
                    "metrics": m,
                    "best_metrics": best_m,
                    "best_passed": best_passed,
                    "gen_seconds": round(time.time() - t0, 1),
                }
                fh.write(json.dumps(row) + "\n")
                fh.flush()

                mi = m.get("mi")
                tag = "base " if it == 0 else ("ACCEPT" if accepted else "REJECT")
                print(
                    f"  iter{it} [{tag}]: pass={passed!s:<5} "
                    f"MI={round(mi, 1) if mi is not None else 'n/a':<6} "
                    f"CC={m.get('cc_total')}  CogC={m.get('cognitive_total')}  "
                    f"-> best=iter{best_iter}(pass={best_passed})",
                    flush=True,
                )
    print(f"\nDone -> {out}")


if __name__ == "__main__":
    main()
