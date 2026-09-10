# Generated code: every solution the model produced

Each file is exactly what the model returned for one `(task, configuration,
iteration)`, after the surrounding prose was stripped and the code block extracted
(`run_baseline.extract_code`). Nothing here was edited by hand. The metrics recorded
in `../results/*.jsonl` were computed from these files, and
`../src/verify_artifacts.py` recomputes all 1260 of them to confirm the match.

## Naming

`Mbpp_<id>_<config>_iter<n>.py` — `iter0` is the no-feedback baseline, `iter1`–`iter3`
the feedback iterations.

| `<config>` | Configuration | Result file |
|---|---|---|
| `v2` | Unguarded, comment-stripping | `feedback_promptv2_restored.jsonl` |
| `v3` | Unguarded, comment-preserving | `feedback_v3_fresh.jsonl` |
| `guard` | Correctness-guarded | `feedback_guarded.jsonl` |
| `blind` | Code-blind, unguarded | `feedback_blind.jsonl` |
| `guardblind` | Code-blind, guarded | `feedback_guarded_blind.jsonl` |

`iter0` is byte-identical across all five configurations — generation is
deterministic at temperature 0 with a fixed seed, and all five share one baseline.

## Not part of the experiment

- `Mbpp_<id>_iter<n>.py` — the superseded original run. These are the files the
  filename collision produced: two runners both wrote this pattern, so the second
  overwrote the first. Kept for the audit trail; no reported number depends on them.
  See `../results/README.md`.
- `proto_*.py` — 5-task pilot from before the MBPP+ harness existed.

## Reading the guarded runs

In a guarded run a file may exist for an iteration whose refactor was **rejected**.
The rejected candidate is still saved (that is how the 13 rejections can be
inspected), but it is not the version carried forward. `accepted` and
`best_iteration` in the JSONL say which file the reported metrics came from.
