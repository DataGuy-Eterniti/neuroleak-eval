"""NeuroLeak eval harness.

For each (model, task, trial):
  1. build a fresh workspace with the task data (hidden labels stay in memory),
  2. send the task instruction to the model (any OpenAI-compatible API, see PROVIDERS),
  3. extract the Python script from the reply and run it in the workspace,
  4. if the script crashes, send the error back once and run the repaired script,
  5. grade the outputs, save the full transcript, append a row to results/runs.jsonl.

Models are written as  provider:model-id  (no prefix = openrouter). Free tiers:
    gemini:<id>      Google AI Studio key            -> GEMINI_API_KEY
    openrouter:<id>  OpenRouter ("...:free" models)   -> OPENROUTER_API_KEY
    groq:<id>        Groq                             -> GROQ_API_KEY
    nvidia:<id>      NVIDIA build.nvidia.com          -> NVIDIA_API_KEY

Examples:
    python run_eval.py --models gemini:gemini-2.5-flash --trials 1 --sleep 10
    python run_eval.py --models nvidia:moonshotai/kimi-k2.6,openrouter:nvidia/nemotron-3-ultra-550b-a55b:free --trials 3
    python run_eval.py --summarize          # rebuild results/summary.md from runs.jsonl

Copy model IDs exactly from each provider's model list.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import time
from pathlib import Path

import pandas as pd

from evalkit.generators import GENERATORS
from evalkit.grader import grade
from evalkit.sandbox import build_workspace, run_script

ROOT = Path(__file__).parent
RESULTS = ROOT / "results"
TRANSCRIPTS = ROOT / "transcripts"

SYSTEM = ("You are an expert data scientist. Solve the task by writing one complete, "
          "runnable Python 3 script. Reply with your reasoning if you wish, then exactly "
          "one fenced code block marked ```python containing the full script.")
REPAIR = ("Your script failed when run in the working directory. Error output (last lines):\n\n"
          "```\n{err}\n```\n\nReply with one corrected, complete script in a single ```python block.")


def extract_code(text: str) -> str | None:
    blocks = re.findall(r"```(?:python|py)\s*\n(.*?)```", text or "", flags=re.S)
    return blocks[-1] if blocks else None


PROVIDERS = {  # name: (OpenAI-compatible base URL, environment variable holding the key)
    "openrouter": ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY"),
    "gemini": ("https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY"),
    "groq": ("https://api.groq.com/openai/v1", "GROQ_API_KEY"),
    "nvidia": ("https://integrate.api.nvidia.com/v1", "NVIDIA_API_KEY"),
}


def split_model(spec: str) -> tuple[str, str]:
    prov, sep, model = spec.partition(":")
    if sep and prov in PROVIDERS:
        return prov, model
    return "openrouter", spec


def make_client(provider: str):
    from openai import OpenAI
    base, env = PROVIDERS[provider]
    key = os.environ.get(env)
    if not key:
        raise SystemExit(f"Set {env} (Codespaces secret or .env) to use provider '{provider}'.")
    return OpenAI(base_url=base, api_key=key, timeout=900, max_retries=0)


def chat(client, model, messages, temperature, max_tokens, provider="openrouter"):
    kwargs = dict(model=model, messages=messages, max_tokens=max_tokens)
    if provider == "openrouter":
        kwargs["extra_body"] = {"usage": {"include": True}}
    if temperature is not None:
        kwargs["temperature"] = temperature
    for attempt in range(6):
        try:
            t0 = time.time()
            r = client.chat.completions.create(**kwargs)
            u = r.usage.model_dump() if r.usage else {}
            return {"text": r.choices[0].message.content or "", "served_model": r.model,
                    "usage": u, "cost_usd": u.get("cost"), "latency_s": round(time.time() - t0, 1)}
        except Exception as e:  # noqa: BLE001  (free tiers often return 429: back off)
            if attempt == 5:
                raise
            wait = 20 * (attempt + 1)
            print(f"   API error ({str(e)[:160]}); retrying in {wait}s")
            time.sleep(wait)


def run_trial(client, spec, task, trial, a):
    provider, model = split_model(spec)
    instruction = (ROOT / "tasks" / task / "instruction.md").read_text()
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": instruction}]
    ws, hidden = build_workspace(task)
    turns, execs, cost = [], [], 0.0
    try:
        for turn in range(1 + a.repairs):
            if turn and a.sleep:
                time.sleep(a.sleep)
            resp = chat(client, model, messages, a.temperature, a.max_tokens, provider)
            cost += resp["cost_usd"] or 0.0
            turns.append(resp)
            messages.append({"role": "assistant", "content": resp["text"]})
            code = extract_code(resp["text"])
            if code is None:
                ex = {"returncode": None, "stderr": "no ```python block in reply", "stdout": ""}
            else:
                for f in (ws / "output").glob("*"):
                    f.unlink()
                ex = run_script(code, ws, timeout=a.timeout)
            execs.append(ex)
            if ex["returncode"] == 0:
                break
            messages.append({"role": "user", "content": REPAIR.format(err=ex["stderr"][-2500:])})
        g = grade(task, ws, hidden)
    finally:
        shutil.rmtree(ws, ignore_errors=True)
    rec = {"model": spec, "provider": provider, "served_model": turns[-1]["served_model"],
           "task": task, "trial": trial,
           "date_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "temperature": a.temperature, "max_tokens": a.max_tokens, "repairs_used": len(turns) - 1,
           "cost_usd": round(cost, 5), **g}
    tdir = TRANSCRIPTS / spec.replace("/", "__").replace(":", "--") / task
    tdir.mkdir(parents=True, exist_ok=True)
    (tdir / f"trial_{trial}.json").write_text(json.dumps(
        {"record": rec, "messages": messages, "turns": turns, "executions": execs}, indent=2))
    with open(RESULTS / "runs.jsonl", "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    return rec


def summarize():
    path = RESULTS / "runs.jsonl"
    if not path.exists():
        print("no runs yet"); return
    df = pd.DataFrame([json.loads(l) for l in path.read_text().splitlines() if l.strip()])
    per_task = (df.groupby(["model", "task"])
                  .agg(trials=("pass", "size"), passes=("pass", "sum"),
                       mean_estimate=("estimate", "mean"), mean_actual=("actual", "mean"),
                       mean_gap=("gap", "mean"), errors=("error", lambda s: s.notna().sum()))
                  .reset_index())
    per_task["pass_rate"] = per_task.passes / per_task.trials
    per_task["pass^k"] = (per_task.passes == per_task.trials).astype(int)
    per_task["pass@k"] = (per_task.passes > 0).astype(int)
    per_model = (per_task.groupby("model")
                   .agg(tasks=("task", "size"), trials_per_task=("trials", "min"),
                        pass_rate=("pass_rate", "mean"), **{"pass^k": ("pass^k", "mean"),
                        "pass@k": ("pass@k", "mean")})
                   .reset_index())
    cost = df.groupby("model").agg(total_cost_usd=("cost_usd", "sum"),
                                   served_model=("served_model", "last"),
                                   first_run=("date_utc", "min"), last_run=("date_utc", "max"))
    per_model = per_model.merge(cost, on="model")
    md = ["# Results", "", "## Per model", "", per_model.round(3).to_markdown(index=False), "",
          "## Per model x task", "", per_task.round(3).to_markdown(index=False), ""]
    (RESULTS / "summary.md").write_text("\n".join(md))
    per_task.to_csv(RESULTS / "summary_per_task.csv", index=False)
    print("\n".join(md))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--models", default="", help="comma-separated provider:model-id list")
    ap.add_argument("--tasks", default=",".join(GENERATORS), help="comma-separated task IDs")
    ap.add_argument("--trials", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=None,
                    help="omit to use each provider's default (recorded as null)")
    ap.add_argument("--max-tokens", type=int, default=16000)
    ap.add_argument("--repairs", type=int, default=1, help="crash-repair turns allowed")
    ap.add_argument("--timeout", type=int, default=600, help="seconds per script run")
    ap.add_argument("--sleep", type=float, default=0, help="seconds to wait between API calls (use 5-15 on free tiers)")
    ap.add_argument("--summarize", action="store_true")
    a = ap.parse_args()
    RESULTS.mkdir(exist_ok=True)
    if a.summarize:
        summarize(); return

    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
    models = [m.strip() for m in a.models.split(",") if m.strip()]
    tasks = [t.strip() for t in a.tasks.split(",") if t.strip()]
    if not models:
        raise SystemExit("Pass --models")
    for spec in models:
        client = make_client(split_model(spec)[0])
        for task in tasks:
            for trial in range(1, a.trials + 1):
                print(f"{spec} | {task} | trial {trial}")
                rec = run_trial(client, spec, task, trial, a)
                if a.sleep:
                    time.sleep(a.sleep)
                print(f"   pass={rec['pass']} estimate={rec['estimate']} actual={rec['actual']} "
                      f"gap={rec['gap']} err={rec['error']} cost=${rec['cost_usd']}")
    summarize()


if __name__ == "__main__":
    main()
