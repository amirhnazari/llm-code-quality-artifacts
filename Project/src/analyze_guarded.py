#!/usr/bin/env python3
"""
Analyse the correctness-guarded run (results/feedback_guarded.jsonl) and put it
head-to-head with the unguarded comment-preserving run
(results/feedback_v3_fresh.jsonl).

FIXED 2026-08-25: the v3 column previously read results/feedback.jsonl, which is
the SUPERSEDED comment-preserving run (see results/README.md) while the guarded
column was already canonical -- so the two halves of the comparison came from
different generations. Both columns now read canonical files. This changes no
number reported in the thesis: canonical v3 gives the same 16 CC reductions cited
in evaluation.tex, and the CogC-reduced count it also shifts (31 -> 30) is not
cited anywhere.

Guarded semantics: baseline = iteration 0; "final" = the carried-forward BEST
version at the last iteration (best_metrics / best_passed). By construction the
guard cannot regress correctness, so the interesting questions are:
  - does correctness hold (regressed should be 0 by design)?           [H3]
  - do MI / CC / CogC of the accepted final version improve?           [H1/H2]
  - how often is a refactor actually accepted vs rejected?             (gate rate)

v3 (unguarded): baseline = iter0; final = last iteration (feed-latest).
"""
from __future__ import annotations

import json
import statistics as st
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
strata = {t["task_id"]: t["stratum"] for t in json.loads((PROJECT / "tasks" / "mbpp_tasks.json").read_text())}


def load(path):
    by = {}
    for l in (PROJECT / path).read_text().splitlines():
        if l.strip():
            r = json.loads(l)
            by.setdefault(r["task_id"], {})[r["iteration"]] = r
    return by


def med(xs):
    return round(st.median(xs), 1) if xs else None


def guarded_stats(by, ids):
    n = len(ids); bp = fp = reg = rep = 0
    acc = rej = 0
    dmi, dcc, dcog = [], [], []
    for t in ids:
        its = by[t]
        b = its[min(its)]
        last = its[max(its)]
        base_pass = b["passed"]
        final_pass = last["best_passed"]          # carried-forward correctness
        bp += base_pass; fp += final_pass
        reg += base_pass and not final_pass
        rep += (not base_pass) and final_pass
        bm, fm = b["metrics"], last["best_metrics"]
        if bm.get("mi") is not None and fm.get("mi") is not None:
            dmi.append(fm["mi"] - bm["mi"])
        if bm.get("cc_total") is not None and fm.get("cc_total") is not None:
            dcc.append(fm["cc_total"] - bm["cc_total"])
        if bm.get("cognitive_total") is not None and fm.get("cognitive_total") is not None:
            dcog.append(fm["cognitive_total"] - bm["cognitive_total"])
        for i in its:
            if i == 0:
                continue
            acc += int(its[i]["accepted"]); rej += int(not its[i]["accepted"])
    return dict(n=n, base=bp, final=fp, reg=reg, rep=rep,
                mi=med(dmi), cc=med(dcc), cog=med(dcog),
                cc_red=sum(1 for x in dcc if x < 0), cog_red=sum(1 for x in dcog if x < 0),
                acc=acc, rej=rej)


def v3_stats(by, ids):
    n = len(ids); bp = fp = reg = rep = 0
    dmi, dcc, dcog = [], [], []
    for t in ids:
        its = by[t]; b, f = its[min(its)], its[max(its)]
        bp += b["passed"]; fp += f["passed"]
        reg += b["passed"] and not f["passed"]; rep += (not b["passed"]) and f["passed"]
        bm, fm = b["metrics"], f["metrics"]
        if bm.get("mi") is not None and fm.get("mi") is not None: dmi.append(fm["mi"] - bm["mi"])
        if bm.get("cc_total") is not None: dcc.append(fm["cc_total"] - bm["cc_total"])
        if bm.get("cognitive_total") is not None and fm.get("cognitive_total") is not None:
            dcog.append(fm["cognitive_total"] - bm["cognitive_total"])
    return dict(n=n, base=bp, final=fp, reg=reg, rep=rep,
                mi=med(dmi), cc=med(dcc), cog=med(dcog),
                cc_red=sum(1 for x in dcc if x < 0), cog_red=sum(1 for x in dcog if x < 0),
                acc=None, rej=None)


v3 = load("results/feedback_v3_fresh.jsonl")
guard = load("results/feedback_guarded.jsonl")
groups = [("OVERALL", list(strata)),
          ("LOWER", [t for t in strata if strata[t] == "lower"]),
          ("HIGHER", [t for t in strata if strata[t] == "higher"])]

for label, ids in groups:
    gids = [t for t in ids if t in guard]
    vids = [t for t in ids if t in v3]
    print(f"\n===== {label} (n={len(gids)}) =====")
    print(f"{'metric':<28}{'v3 (unguarded)':>16}{'guarded':>16}")
    a, b = v3_stats(v3, vids), guarded_stats(guard, gids)
    print(f"{'correctness base->final':<28}{str(a['base'])+'->'+str(a['final']):>16}{str(b['base'])+'->'+str(b['final']):>16}")
    print(f"{'  regressed / repaired':<28}{str(a['reg'])+'/'+str(a['rep']):>16}{str(b['reg'])+'/'+str(b['rep']):>16}")
    print(f"{'MI median delta   [H1]':<28}{str(a['mi']):>16}{str(b['mi']):>16}")
    print(f"{'CC median delta   [H2]':<28}{str(a['cc']):>16}{str(b['cc']):>16}")
    print(f"{'CogC median delta [H2]':<28}{str(a['cog']):>16}{str(b['cog']):>16}")
    print(f"{'  #CC red / #CogC red':<28}{str(a['cc_red'])+'/'+str(a['cog_red']):>16}{str(b['cc_red'])+'/'+str(b['cog_red']):>16}")
    if b['acc'] is not None:
        print(f"{'  refactors acc / rej':<28}{'-':>16}{str(b['acc'])+'/'+str(b['rej']):>16}")
