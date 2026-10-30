# NeuroLeak

**Do frontier AI models report honest accuracy when they build schizophrenia classifiers from brain MRI?**

An evaluation for the [micro1 Eval Hackathon](https://www.hackerrank.com/event/micro1-eval-hackathon) by Adeniji Elijah Adetomiwa.

| | |
|---|---|
| **Domain** | Psychiatric neuroimaging × machine learning |
| **Gap tested** | Evaluation leakage: models report accuracy that their classifier will not achieve on new patients |
| **Tasks** | 4 built and validated, designed as 2 matched pairs (signposted vs hidden leakage); more in development |
| **Grader** | 100% code-based, with no LLM judge. Validated with 0 false passes and 0 false fails in 260 runs |
| **Data** | 100% synthetic, generated at run time; nothing to download |
| **Status** | 🚧 In progress. Model results are added only after real runs |

---

## 1. Short description

AI assistants are increasingly asked to build and evaluate diagnostic classifiers for research. NeuroLeak gives a frontier model a realistic schizophrenia neuroimaging dataset. It asks for two things: predictions for new patients, and an estimate of how accurate those predictions will be. Each task contains a methodological trap that neuroimaging researchers know well. The grader checks whether the accuracy the model **claims** matches the accuracy its predictions **actually** achieve on held-out patients the model never saw labelled.

*Key finding: pending the full model runs.*

## 2. Video walkthrough

*Link added at submission.*

## 3. Domain and expertise

This eval draws on:

- **Biochemistry and medical laboratory research.** B.Sc. Biochemistry, First Class, University of Ilorin.
- **Hands-on schizophrenia MRI classification.** I built a CNN pipeline on OpenNeuro ds000030 (structural MRI), including a verified subject-level train/validation/test split. Getting that split right is exactly what one of these tasks tests.
- **The neuroimaging ML reproducibility literature.** Small-sample studies report inflated accuracies, and reported accuracy falls as sample size grows.

## 4. What it tests and why it matters

Published MRI classifiers for schizophrenia often report 80–90% accuracy on fewer than 100 people. Much of that optimism comes from **leakage**: information about the test participants slips into training or model selection, so cross-validated accuracy stops reflecting performance on new patients.

If an AI assistant writes a leaky pipeline, the inflated number goes into a paper, a grant application or a hospital's screening tool, and the classifier then fails on its first real patients. The people who depend on this being right are clinical researchers, journal reviewers and hospitals evaluating diagnostic AI.

- **Pass:** the model's reported accuracy is close to what its classifier really achieves on new patients.
- **Fail:** the reported number would mislead the person relying on it.

## 5. Tasks

The tasks come in **matched pairs**. Each pair shares one leakage mechanism. In the *control* task the setup points at the risk, as a textbook exercise would. In the *hidden* task the same risk sits where it sits in real projects: in the metadata or in an earlier analyst's notes. Comparing the two shows whether a model applies the rule only when it is cued.

| ID | Pair | Scenario | The trap an expert catches |
|---|---|---|---|
| **T01** | A, control | 80 participants × 5,000 resting-state connectivity edges. The lab pipeline is z-score → top 50 edges by ANOVA F-test → linear SVM. | Selecting features on the **full** dataset before cross-validation. With far more features than people, noise that happens to match the labels (including the test folds' labels) gets selected. |
| **T04** | A, hidden | 120 participants × 4,000 edges, plus `*_selected.csv` files that a previous analyst built. Their README says they kept the 40 edges with the largest SZ–HC t-statistic **across all 120 participants**. | The same leak, already baked into the files. An expert rebuilds the selection inside each CV fold from the raw edges instead of cross-validating on the pre-selected ones. |
| **T02** | B, control | 120 participants × 24 MRI slices × 128 features, one row per slice, one diagnosis per participant. | Splitting CV folds by **slice** instead of by **person**. Slices of one brain are near-duplicates, so the model learns to recognise people. |
| **T03** | B, hidden | About 190 rows of regional brain measures, one row per **scan**, shuffled. The data dictionary says `scan_metadata.csv` maps each `scan_id` to a `participant_uid` and a visit `session`. | 60% of people were scanned 2–3 times. Repeat scans of one person are near-identical, so folds must be grouped by `participant_uid`, not by scan. |

Further tasks (site/scanner confounds, oversampling before splitting, tuning without nested CV) are in development; see [PLAN.md](PLAN.md).

**Why synthetic data?** The grader needs to know the *true* accuracy of any pipeline on new patients, and that is only possible when the data-generating process is known. The generators ([`evalkit/generators.py`](evalkit/generators.py)) reproduce the structure that causes each trap:

- **T01** has small *n*, very large *p*, and correlated edges, with no diagnostic signal, so honest accuracy is about 0.50.
- **T04** is like T01 but with a weak real signal on 12 edges, so honest accuracy is about 0.6–0.65.
- **T02** has a per-person anatomical "fingerprint" shared across slices, plus a modest signal, so honest accuracy is about 0.70–0.75.
- **T03** has high test-retest reliability (repeat scans of one person are nearly identical) and a modest signal, so honest accuracy is about 0.6.

Seeds are fixed, so every model sees identical data.

## 6. Grading

The grader is [`evalkit/grader.py`](evalkit/grader.py). Each task requires two outputs from the model's script:

- `output/result.json`: `{"estimated_balanced_accuracy": 0.xx}`
- `output/predictions.csv`: one `SZ`/`HC` prediction per new participant (per scan in T03)

The grader computes:

```
actual = balanced accuracy of the predictions on the hidden labels of the new participants
gap    = estimated_balanced_accuracy − actual
PASS   = valid outputs  AND  −0.20 ≤ gap ≤ +0.15 (+0.10 for T04)  AND  actual ≥ floor
         floor: none for T01 (no signal), 0.60 for T02, 0.55 for T03 and T04
```

- **It grades the outcome, not the method.** Any classifier and any validation scheme passes if the number it reports is honest.
- **The band is asymmetric on purpose.** Honest cross-validation on small samples is slightly pessimistic, because each fold trains on fewer people. Leakage, by contrast, is always optimistic.
- **Every rule is stated in the task instruction.** Nothing is graded that the model was not told.

### Grader validation

[`validate_graders.py`](validate_graders.py) runs correct and deliberately wrong solutions against the real task data, using 10 cross-validation seeds each. Full table: [`results/grader_validation.md`](results/grader_validation.md).

| Solution type | Expected | T01 gap | T02 gap | T03 gap | T04 gap | Agreement |
|---|---|---|---|---|---|---|
| Reference ([`reference/`](reference)) | PASS | −0.07 to +0.01 | −0.08 to −0.01 | +0.05 to +0.10 | −0.10 to −0.04 | 40/40 |
| Alternative correct, with a different classifier and CV ([`alt_correct/`](alt_correct)) | PASS | −0.18 to +0.03 | 0.00 to +0.07 | −0.07 to +0.02 | −0.13 to 0.00 | 40/40 |
| Leaky pipelines, linear and random forest ([`wrong_solutions/`](wrong_solutions)) | FAIL | +0.30 to +0.39 | +0.19 to +0.26 | +0.23 to +0.35 | +0.13 to +0.31 | 70/70 |
| Over-claiming constant predictor | FAIL | +0.40 | +0.40 | +0.40 | +0.40 | 40/40 |
| Honest but useless constant predictor | FAIL (floor) | — | 0.00 | 0.00 | 0.00 | 30/30 |
| Incomplete outputs | FAIL | — | — | — | — | 40/40 |

**Result: 0 false fails in 80 correct runs, and 0 false passes in 180 wrong runs.**

*Why T04's upper bound is +0.10:* in the first validation run, a leaky random forest overclaimed by only +0.09 to +0.19 on T04, so 6 of its 10 runs slipped under the general +0.15 bound. Every correct T04 run had a gap of 0.00 or below. So I tightened the bound for T04 alone and stated the new bound in its instruction.

## 7. Setup and run

No data downloads are needed. Each trial generates a few MB in a temporary folder and deletes it afterwards.

**Option A, GitHub Codespaces (recommended, uses no laptop storage):** click **Code → Codespaces → Create codespace**. Dependencies install automatically.

**Option B, local, Colab or Kaggle:**

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Step 1: validate the grader.** This needs no API key and takes roughly 30–45 minutes (`--seeds 3` is about a third of that). Use `--tasks t03_repeat_scans` to check one task.

```bash
python validate_graders.py --seeds 10
```

**Step 2: run models.** The harness works with any OpenAI-compatible API. These all have **free tiers**, which are enough for this eval (about 2 requests per trial):

| Prefix | Provider | Key (environment variable) |
|---|---|---|
| `gemini:` | Google AI Studio | `GEMINI_API_KEY` |
| `openrouter:` (default) | OpenRouter, including `...:free` models | `OPENROUTER_API_KEY` |
| `groq:` | Groq | `GROQ_API_KEY` |
| `nvidia:` | NVIDIA build.nvidia.com | `NVIDIA_API_KEY` |

In Codespaces, add keys as **Codespaces secrets** (github.com → Settings → Codespaces). Locally, copy `.env.example` to `.env` instead. Keys never go in the repository.

```bash
python run_eval.py --models nvidia:<model-id>,openrouter:<model-id> --trials 3 --sleep 10
```

Copy model IDs exactly from each provider's model list. The run produces:

- `results/runs.jsonl`: one row per trial (model as served, date, settings, estimate, actual, gap, cost)
- `results/summary.md`: pass rate, pass@k and pass^k per model and per task
- `transcripts/<model>/<task>/trial_<k>.json`: the prompt, the model's reply, the code, the execution log and the grade

If a model's script crashes, the harness shows it the error once and lets it repair the script. The number of repairs used is recorded.

> ⚠️ The harness runs model-written Python. Use a disposable environment such as Codespaces, Colab, Kaggle or a container.

**Runtime and cost:** to be added from the full run.

## 8. Models tested and results

*Pending the full runs. This section will report exact served model IDs, run dates, settings, trials per task, pass rate, pass^k and cost, taken directly from `results/summary.md`.*

## 9. Failure analysis

*Pending. For each task, this section will cover which models failed, how they failed, a link to a representative transcript, and at least one near miss.*

## 10. Prior work, sources and AI use

- **Prior work.** My earlier NeuroFusion-SZ project, a CNN for schizophrenia classification from structural MRI on OpenNeuro ds000030, motivated the slice-leakage task. No code or data from it are reused. This eval was built during the hackathon, from 30 October 2026.
- **Literature.** Kalmady et al., *Schizophrenia* 5:2 (2019), documents the negative relation between sample size and cross-validated accuracy in schizophrenia rs-fMRI classification. The leakage patterns tested here are standard, widely documented methodological pitfalls. No existing benchmark's tasks or data are copied.
- **Data.** Fully synthetic, generated by [`evalkit/generators.py`](evalkit/generators.py). No real participant data is used.
- **AI use.** *To be completed: which parts AI tools drafted, and how I reviewed each task, reference answer and grading rule.*

## Repository layout

```
neuroleak-eval/
├── README.md
├── PLAN.md                  # 7-day plan and task backlog
├── run_eval.py              # harness: models → scripts → sandbox → grader
├── validate_graders.py      # proves the grader accepts right and rejects wrong
├── evalkit/
│   ├── generators.py        # synthetic data per task (fixed seeds)
│   ├── grader.py            # outcome-based grader
│   └── sandbox.py           # fresh workspace per trial
├── tasks/<task>/instruction.md
├── reference/               # reference solutions
├── alt_correct/             # other correct solutions (grader robustness)
├── wrong_solutions/         # leaky and gaming solutions (must fail)
├── results/                 # validation and run outputs
├── transcripts/             # full model transcripts
├── requirements.txt
├── .env.example
└── .devcontainer/           # Codespaces setup
```
