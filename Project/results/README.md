# Results: which files the thesis uses

One JSON line per `(task_id, iteration)`. Iteration 0 is the no-feedback baseline;
iterations 1–3 are feedback iterations. The loop never stops early, so every task
has exactly four rows in every run.

## Canonical runs (these five produce every number in the paper)

| File | Paper's name for it | `stats.py` kind |
|---|---|---|
| `feedback_promptv2_restored.jsonl` | Unguarded, comment-stripping | `plain` |
| `feedback_v3_fresh.jsonl` | Unguarded, comment-preserving | `plain` |
| `feedback_guarded.jsonl` | Correctness-guarded | `guarded` |
| `feedback_blind.jsonl` | Code-blind, unguarded (secondary) | `plain` |
| `feedback_guarded_blind.jsonl` | Code-blind, guarded (secondary) | `guarded` |

`plain` runs take the **last** iteration as the final version. `guarded` runs take
the **carried-forward accepted** version (`best_metrics` / `best_passed`), which is
why correctness can never fall below the baseline there.

## Superseded — kept for the audit trail, used by nothing

| File | Why it is not used |
|---|---|
| `feedback.jsonl` | Original comment-preserving run. Its saved code files (`generated/{stem}_iter*.py`) overwrote the v2 run's files, so v2 could no longer be checked against its own code. Superseded by `feedback_v3_fresh.jsonl`. |
| `feedback_promptv2.jsonl` | Original comment-stripping run. Its code files were the ones overwritten; the exact prompt was never committed. Superseded by `feedback_promptv2_restored.jsonl`. |
| `baseline.jsonl` | 5-task prototype from the pilot stage, before the MBPP+ harness. Not part of the experiment. |
| `guarded_run.log` | Console log of the guarded run. |

The two analysis scripts that read these superseded files live in
`src/superseded/` (`analyze.py`, `compare_runs.py`) and print a warning banner
before their output, so a stale number cannot be mistaken for a reported one.
`compare_runs.py` is what reproduces the withdrawn -16.3 MI figure — kept
deliberately, as the evidence for the §5.5 disclosure.

Both runners wrote to `{stem}_iter{it}.py`, which is how the collision happened.
The replacement runners write collision-free names (`_v2_`, `_v3_`). The incident and
its consequence — a previously reported effect that did not reproduce — are disclosed
in the thesis (§5.5).

`verify_v2_restore.py` compares the restored v2 against the original recording:
**185 of 252 rows match exactly.** Generation is deterministic for a fixed prompt
(iteration 0 is byte-identical across all runs), but a multi-step trajectory can
diverge once any intermediate iteration differs. This is why the thesis reports a
single archived run per configuration.

## Reproducing the paper's numbers

Exact, offline, no model required — recomputes the metrics from the archived code
and re-runs the statistics:

```bash
python src/verify_artifacts.py   # 1260 rows: recomputed == recorded
python src/stats.py              # every p-value in tab:results and tab:blind
python src/supp_metrics.py       # tab:supp
python src/compare_blind.py      # tab:blind head-to-head
python src/plots.py              # the four figures
```

Re-running *generation* (`src/run_*.py`) needs Ollama and will not necessarily
reproduce these trajectories — see above.
