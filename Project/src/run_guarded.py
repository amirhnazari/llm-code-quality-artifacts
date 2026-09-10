#!/usr/bin/env python3
"""
Correctness-guarded feedback loop -- the third method (the Expose's "CI/CD
quality gate").

Same static-analysis feedback as the plain loop, but the MBPP+ oracle now acts
as a GATE on every refactor:

  iteration 0      = baseline generation (identical to run_baseline / run_feedback).
  iterations 1..N  = refactor the LAST ACCEPTED (still-correct) version using the
                     static-analysis findings, then gate on correctness:
      - refactor still passes the oracle  -> ACCEPT: it becomes the new best and
        the loop continues from it.
      - refactor breaks correctness       -> REJECT: roll back to the last accepted
        version, and on the next attempt tell the model its change altered
        behaviour. That note changes the prompt, so at temperature 0 the model
        does NOT deterministically reproduce the same broken refactor (a plain
        roll-back-and-retry with a byte-identical prompt would loop forever).

By construction final correctness never drops below the baseline: the loop can
hold or repair correctness, never lose it. We then measure whether the accepted
final version's maintainability/complexity improved -- i.e. whether gating on
tests buys the complexity reduction WITHOUT the correctness cost the unguarded
runs (v2/v3) paid.

One JSON line per (task, iteration) -> results/feedback_guarded.jsonl:
  passed        -- did THIS iteration's candidate pass the oracle
  accepted      -- was it accepted (kept) or rejected (rolled back)
  best_iteration-- which iteration's code is carried forward after the decision
  metrics       -- structural metrics of THIS candidate
  best_metrics  -- structural metrics of the carried-forward (best) version
  best_passed   -- correctness of the carried-forward version (non-decreasing)
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

GUARD_NOTE = (
    "IMPORTANT: your PREVIOUS refactor was REJECTED by a regression test -- it "
    "changed the function's behaviour and no longer produced the correct output for "
    "every input. Start again from the working solution below and make a SMALLER, "
    "strictly behaviour-preserving change: only simplify control flow you are certain "
    "keeps identical outputs for all inputs. If in doubt, make a minimal edit."
)


def main():
    out = RES / "feedback_guarded.jsonl"
    with out.open("w") as fh:
        for task in TASKS:
            stem = re.sub(r"\W", "_", task["task_id"])
            print(f"\n=== {task['task_id']} ===", flush=True)

            best_code = best_m = best_pmsgs = None
            best_passed = False
            best_iter = 0
            reject_streak = 0

            for it in range(0, MAX_ITERS + 1):
                t0 = time.time()
                if it == 0:
                    resp = base.generate(base.build_prompt(task))
                else:
                    prompt = fb.feedback_prompt(best_code, best_m, best_pmsgs, task)
                    if reject_streak:
                        prompt = f"{GUARD_NOTE}\n(This is retry #{reject_streak}.)\n\n" + prompt
                    resp = base.generate(prompt)

                code = base.extract_code(resp.get("response", ""))
                cp = GEN / f"{stem}_guard_iter{it}.py"
                cp.write_text(code + "\n")

                passed = base.check_correctness(cp, task)["passed"]
                m = base.metrics(cp)
                pmsgs = fb.pylint_messages(cp)

                # --- correctness gate -------------------------------------
                if it == 0:
                    accepted = True                       # baseline is the anchor
                else:
                    # accept unless it regresses correctness: if best is currently
                    # correct, the candidate must stay correct; if best is already
                    # broken, anything is accepted (correctness cannot get worse).
                    accepted = passed or (not best_passed)

                if accepted:
                    best_code, best_m, best_pmsgs, best_passed, best_iter = \
                        code, m, pmsgs, passed, it
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
                    "pylint_symbols": [msg.get("symbol") for msg in pmsgs],
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
