#!/usr/bin/env python3
"""
Baseline (no-feedback) runner for the thesis experiment.

For each task: generate Python code ONCE with a local Ollama model, check
functional correctness against the task's asserts, then measure structural
quality (Maintainability Index, Cyclomatic Complexity, Cognitive Complexity,
Pylint counts, LOC). Each task -> one JSON line in results/baseline.jsonl.

This is the Week 1-2 baseline arm. No feedback loop yet (that is Week 3-4).
Stdlib only for the core; radon / pylint / complexipy are invoked as subprocesses.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import mbpp_data

# Ensure venv-installed tools (radon/pylint/complexipy) resolve in subprocess
# calls even when the venv is not "activated" (e.g. invoked via .venv/bin/python).
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ.get("PATH", "")

PROJECT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((PROJECT / "config.json").read_text())


def load_tasks():
    """Task source: 'mbpp' (frozen MBPP+ set) or 'proto' (prototype asserts).
    Override via env: THESIS_TASK_SET, THESIS_TASK_LIMIT (0 = all)."""
    task_set = os.environ.get("THESIS_TASK_SET", CONFIG.get("task_set", "proto"))
    limit = int(os.environ.get("THESIS_TASK_LIMIT", "0") or 0)
    if task_set == "mbpp":
        return mbpp_data.load_mbpp_tasks(limit)
    tasks = json.loads((PROJECT / "tasks" / "proto_tasks.json").read_text())
    for t in tasks:
        t["kind"] = "asserts"
    return tasks[:limit] if limit else tasks


TASKS = load_tasks()
GEN_DIR = PROJECT / "generated"
RES_DIR = PROJECT / "results"
GEN_DIR.mkdir(exist_ok=True)
RES_DIR.mkdir(exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate(prompt: str) -> dict:
    """Call the local Ollama model once. Returns the full response JSON."""
    body = {
        "model": CONFIG["model"],
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": CONFIG["temperature"],
            "seed": CONFIG["seed"],
            "num_ctx": CONFIG["num_ctx"],
        },
    }
    req = urllib.request.Request(
        OLLAMA_URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=CONFIG.get("gen_timeout", 300)) as r:
        return json.loads(r.read())


def extract_code(text: str) -> str:
    """Pull the first ```python ...``` (or ``` ```) block; else return raw text."""
    m = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
    return (m.group(1) if m else text).strip()


def build_prompt(task: dict) -> str:
    if task.get("kind") == "mbpp":
        return mbpp_data.build_mbpp_prompt(task)
    tests = "\n".join(task["tests"])
    return (
        "You are an expert Python programmer. Write a single self-contained "
        "Python function that solves the task. Respond with ONLY a Python code "
        "block, no explanation.\n\n"
        f"Task: {task['prompt']}\n\n"
        f"Your function must pass these tests:\n{tests}\n"
    )


def check_correctness(code_path: Path, task: dict) -> dict:
    """MBPP tasks -> EvalPlus-style oracle check; prototype -> assert execution."""
    if task.get("kind") == "mbpp":
        return mbpp_data.check_mbpp(code_path, task, CONFIG)
    harness = code_path.read_text() + "\n\n" + "\n".join(task["tests"]) + "\n"
    try:
        proc = subprocess.run(
            [sys.executable, "-c", harness],
            capture_output=True, text=True, timeout=CONFIG.get("test_timeout", 30),
        )
        return {"passed": proc.returncode == 0, "stderr": proc.stderr[-500:]}
    except subprocess.TimeoutExpired:
        return {"passed": False, "stderr": "TIMEOUT"}


def _run_json(cmd: list) -> dict | list | None:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return json.loads(proc.stdout) if proc.stdout.strip() else None
    except Exception as e:  # noqa: BLE001 - best-effort metric collection
        return {"error": str(e)}


def metrics(code_path: Path) -> dict:
    """Collect structural metrics. Best-effort: failures are recorded, not fatal."""
    p = str(code_path)
    out = {}

    # radon: Maintainability Index
    mi = _run_json(["radon", "mi", "-j", p])
    out["mi"] = (mi or {}).get(p, {}).get("mi") if isinstance(mi, dict) else None

    # radon: Cyclomatic Complexity (per function) -> record total + max
    cc = _run_json(["radon", "cc", "-j", p])
    blocks = (cc or {}).get(p, []) if isinstance(cc, dict) else []
    cc_vals = [b.get("complexity", 0) for b in blocks] if isinstance(blocks, list) else []
    out["cc_total"] = sum(cc_vals) if cc_vals else 0
    out["cc_max"] = max(cc_vals) if cc_vals else 0

    # radon: raw LOC metrics
    raw = _run_json(["radon", "raw", "-j", p])
    out["loc"] = (raw or {}).get(p, {}).get("sloc") if isinstance(raw, dict) else None

    # radon: Halstead volume & effort (file total)
    hal = _run_json(["radon", "hal", "-j", p])
    total = (hal or {}).get(p, {}).get("total") if isinstance(hal, dict) else None
    if isinstance(total, dict):
        out["halstead_volume"] = total.get("volume")
        out["halstead_effort"] = total.get("effort")
    else:
        out["halstead_volume"] = None
        out["halstead_effort"] = None

    # complexipy: Cognitive Complexity. Writes complexipy-results.json into cwd.
    try:
        subprocess.run(
            ["complexipy", p, "--output-format", "json", "-q"],
            capture_output=True, text=True, timeout=60, cwd=str(PROJECT),
        )
        cj = PROJECT / "complexipy-results.json"
        if cj.exists():
            data = json.loads(cj.read_text())
            cj.unlink()
            vals = [d.get("complexity", 0) for d in data] if isinstance(data, list) else []
            out["cognitive_total"] = sum(vals) if vals else 0
            out["cognitive_max"] = max(vals) if vals else 0
        else:
            out["cognitive_total"] = None
    except Exception as e:  # noqa: BLE001
        out["cognitive_error"] = str(e)

    # pylint: counts by message type (C/R/W/E)
    pl = _run_json(["pylint", "--output-format=json", "--score=n", p])
    counts = {"C": 0, "R": 0, "W": 0, "E": 0}
    if isinstance(pl, list):
        for msg in pl:
            counts[msg.get("type", "")[:1].upper()] = counts.get(msg.get("type", "")[:1].upper(), 0) + 1
    out["pylint"] = counts
    return out


def main():
    runfile = RES_DIR / "baseline.jsonl"
    with runfile.open("w") as fh:
        for task in TASKS:
            print(f"[{task['task_id']}] generating...", flush=True)
            t0 = time.time()
            resp = generate(build_prompt(task))
            code = extract_code(resp.get("response", ""))
            # snake_case the filename so pylint's module-name check doesn't flag
            # our own naming (e.g. "proto-3" -> "proto_3"); measure the code, not the file.
            stem = re.sub(r"\W", "_", task["task_id"])
            code_path = GEN_DIR / f"{stem}.py"
            code_path.write_text(code + "\n")

            correctness = check_correctness(code_path, task)
            m = metrics(code_path)
            row = {
                "task_id": task["task_id"],
                "model": CONFIG["model"],
                "options": {k: CONFIG[k] for k in ("temperature", "seed", "num_ctx")},
                "gen_seconds": round(time.time() - t0, 1),
                "passed": correctness["passed"],
                "metrics": m,
                "stderr": correctness["stderr"],
            }
            fh.write(json.dumps(row) + "\n")
            fh.flush()
            print(f"  passed={row['passed']}  MI={m.get('mi')}  CC_total={m.get('cc_total')}  pylint={m.get('pylint')}", flush=True)
    print(f"\nDone -> {runfile}")


if __name__ == "__main__":
    main()
