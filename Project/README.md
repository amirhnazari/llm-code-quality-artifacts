# Experiment: static-analysis feedback loop for LLM-generated Python

Code and data for the thesis *"Code Quality of LLM-Generated Python Code: Can
Iterative Static-Analysis Feedback Improve Maintainability Without Reducing
Functional Correctness?"*

A local 7B code model generates a Python solution for each of 63 MBPP+ tasks, static
analysis measures the result, the findings are fed back to the model as a re-prompt,
and it refactors — up to three times. Five configurations of that loop were run; all
of their data is in this repository.

## Status: complete

All five runs are archived in `results/`, every solution the model produced is in
`generated/`, and all four figures plus every statistic in the thesis regenerate from
them offline.

## Reproducing the thesis numbers

No model, no network, no API key. Every number in the paper comes out of these five
commands:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt     # versions are pinned; see the note there

python src/verify_artifacts.py      # 1260 rows: recomputed metrics == recorded
python src/verify_oracle.py         # the correctness oracle accepts/rejects correctly
python src/stats.py                 # Wilcoxon + McNemar -> tab:results, tab:blind
python src/supp_metrics.py          # LOC / Halstead / Pylint -> tab:supp
python src/compare_blind.py         # code-blind ablation head-to-head
python src/plots.py                 # the four figures in ../figures/
```

Run the two verifiers first. `verify_artifacts.py` re-measures all 1260 archived
solutions and checks each against the value recorded at run time, which is what makes
the reported statistics traceable to specific files. `verify_oracle.py` checks the
correctness oracle itself, since H3 depends entirely on it: every reference solution
passes its own oracle (63/63), every deliberately corrupted variant is rejected
(63/63), and it reports how much the MBPP+ augmentation adds over the benchmark's
original inputs (193 original vs 6519 augmented; 12 baseline solutions pass the
original inputs but are caught by the augmentation).

## Two different kinds of reproducibility

Worth separating, because only the first is exact:

- **Recomputing from the archived code is exact.** The five commands above are
  deterministic and produce the thesis's numbers to the digit.
- **Re-running generation is approximate.** `src/run_*.py` needs Ollama and will not
  necessarily reproduce these trajectories. Iteration 0 is byte-identical across all
  five runs, so single-shot generation *is* deterministic — but once any intermediate
  iteration differs, the rest of a multi-step trajectory can diverge. The thesis
  therefore reports one archived run per configuration and discusses this in §5.5.

## Model (the object of study)

`Qwen2.5-Coder-7B-Instruct`, served locally by Ollama as `qwen2.5-coder:7b` (Q4_K_M),
`temperature=0`, `seed=42`, `num_ctx=4096` — all pinned in `config.json`. A mid-tier
7B model is competent enough for a real correctness baseline while leaving structural
headroom for the loop to act on. Local hosting means no provider drift and no API cost.

## Metrics

| Metric | Tool | Role |
|---|---|---|
| Functional correctness | EvalPlus (MBPP+ oracle) | primary, H3 |
| Maintainability Index | `radon` | primary, H1 |
| Cyclomatic complexity | `radon` | primary, H2 |
| Cognitive complexity | `complexipy` | primary, H2 |
| Halstead volume/effort, LOC | `radon` | supplementary |
| Linter counts (C/R/W/E) | `pylint` | feedback source, not a primary measure |

## Layout

```
config.json          pinned model + sampling parameters
requirements.txt     pinned tool versions (the paper cites these)
tasks/
  mbpp_tasks.json      the frozen 63-task set with strata
  mbpp_candidates.json the filter's output pool (identical to the above: 63)
  proto_tasks.json     5-task pilot, pre-MBPP+
src/
  select_tasks.py      the task filter (CC >= 3, SLOC >= 5, no I/O)
  mbpp_data.py         MBPP+ loading, prompting, the correctness oracle
  run_baseline.py      generation + measurement helpers used by every runner
  run_feedback_v2.py   comment-stripping loop
  run_feedback_v3.py   comment-preserving loop
  run_guarded.py       correctness-guarded loop
  run_feedback_blind.py / run_guarded_blind.py   code-blind ablation
  verify_artifacts.py  recompute all recorded metrics from archived code
  verify_oracle.py     validate the correctness oracle itself
  stats.py             the significance tests
  supp_metrics.py      supplementary-metric table
  compare_blind.py     code-blind ablation analysis
  plots.py             the four figures
  superseded/          reads the SUPERSEDED runs -- no thesis number comes from here
results/             one JSONL per run -- see results/README.md for which are canonical
generated/           every solution produced -- see generated/README.md for naming
```

`src/run_feedback.py` is the original comment-preserving runner, superseded by
`run_feedback_v3.py` (which writes collision-free filenames). It is kept because the
other runners import their shared feedback prompt from it.

`src/superseded/` holds the two analysis scripts that read the superseded runs:
`analyze.py` (the exploratory pass over the original comment-preserving run) and
`compare_runs.py` (the v2-vs-v3 comparison that produced the **withdrawn** -16.3 MI
figure). Both print a warning banner before their output. They are kept on purpose
rather than deleted: §5.5 of the thesis discloses that a recorded effect did not
survive re-running, and these are what let a reader verify that claim instead of
taking it on trust. Nothing reported in the thesis comes from them.

## Task selection

Tasks come from MBPP+ as distributed with EvalPlus 0.3.1. The filter is applied to
each task's *reference* solution and keeps those with cyclomatic complexity >= 3 and
>= 5 source lines, excluding any whose reference needs file/network I/O or a
non-stdlib import. This is deterministic and yields exactly 63 tasks — there is no
sampling step. They are then split by the reference solution's cyclomatic complexity
into a lower stratum (CC 3–4, n=40) and a higher stratum (CC >= 5, n=23).
