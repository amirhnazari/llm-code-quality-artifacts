#!/usr/bin/env python3
"""
MBPP+ task loading, prompting, and correctness for the real experiment.

Correctness follows the EvalPlus MBPP+ methodology: the candidate function is run
against the base + plus test inputs, and its outputs are compared to the reference
(canonical) solution used as an oracle (with float tolerance `atol`). "Passed" =
matches the reference on every input with no exception.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from evalplus.data import get_mbpp_plus

PROJECT = Path(__file__).resolve().parent.parent
_CACHE = None


def _mbpp():
    global _CACHE
    if _CACHE is None:
        _CACHE = get_mbpp_plus()
    return _CACHE


def load_mbpp_tasks(limit: int = 0) -> list:
    frozen = json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())
    data = _mbpp()
    tasks = []
    for f in frozen:
        t = data.get(f["task_id"])
        if not t:
            continue
        tasks.append({
            "task_id": f["task_id"],
            "kind": "mbpp",
            "entry_point": t["entry_point"],
            "prompt": t["prompt"],
            "canonical_solution": t["canonical_solution"],
            "inputs": list(t.get("base_input", [])) + list(t.get("plus_input", [])),
            "atol": t.get("atol", 0) or 0,
            "stratum": f["stratum"],
            "ref_cc": f["ref_cc"], "ref_loc": f["ref_loc"], "ref_mi": f["ref_mi"],
        })
    return tasks[:limit] if limit else tasks


def build_mbpp_prompt(task: dict) -> str:
    return (
        "You are an expert Python programmer. Complete the following task with a "
        "single self-contained Python function. Respond with ONLY a Python code block.\n\n"
        + task["prompt"].strip()
        + f"\n\nThe function must be named `{task['entry_point']}`."
    )


_HARNESS = r'''
import copy, math, os, signal

# Self-timeout: even if the parent is killed, this child cannot spin forever.
# A pure-Python infinite loop (the failure mode we saw) hits bytecode boundaries,
# so SIGALRM is delivered; the handler force-exits past any candidate try/except.
def _self_timeout(signum, frame):
    print("FAIL")
    os._exit(1)

signal.signal(signal.SIGALRM, _self_timeout)
signal.alarm({alarm})

ENTRY = {entry!r}
ATOL = {atol!r}
INPUTS = {inputs!r}

def _load(path):
    ns = {{}}
    with open(path) as fh:
        exec(compile(fh.read(), path, "exec"), ns)
    return ns[ENTRY]

def _eq(a, b):
    if isinstance(a, float) or isinstance(b, float):
        try:
            return math.isclose(a, b, rel_tol=1e-6, abs_tol=(ATOL or 1e-6))
        except TypeError:
            return a == b
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_eq(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_eq(a[k], b[k]) for k in a)
    return a == b

cand = _load({cand!r})
ref = _load({ref!r})
ok = True
for inp in INPUTS:
    args = list(inp) if isinstance(inp, (list, tuple)) else [inp]
    try:
        expected = ref(*copy.deepcopy(args))
        got = cand(*copy.deepcopy(args))
    except Exception:
        ok = False
        break
    if not _eq(got, expected):
        ok = False
        break
print("PASS" if ok else "FAIL")
'''


def check_mbpp(code_path, task: dict, config: dict) -> dict:
    """Run candidate vs reference oracle over base+plus inputs in a subprocess.

    Hardened against runaway candidate code: the child runs in its own process
    group (``start_new_session``) so a timeout kills the WHOLE group -- no test
    subprocess is left orphaned -- and the harness itself carries a SIGALRM
    self-timeout as a second line of defence.
    """
    rf = tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, dir=str(PROJECT))
    timeout = config.get("test_timeout", 30)
    alarm = max(5, timeout - 3)  # child self-kills just before the parent gives up
    try:
        rf.write(task["canonical_solution"])
        rf.close()
        harness = _HARNESS.format(
            entry=task["entry_point"], atol=task["atol"], inputs=task["inputs"],
            cand=str(code_path), ref=rf.name, alarm=alarm,
        )
        proc = subprocess.Popen(
            [sys.executable, "-c", harness],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            start_new_session=True,  # child becomes its own process-group leader
        )
        try:
            stdout, stderr = proc.communicate(timeout=timeout)
            return {"passed": stdout.strip().endswith("PASS"), "stderr": stderr[-500:]}
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError, OSError):
                pass
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                pass
            return {"passed": False, "stderr": "TIMEOUT"}
    finally:
        try:
            os.unlink(rf.name)
        except OSError:
            pass
