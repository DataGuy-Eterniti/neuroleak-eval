# NeuroLeak

**Do frontier AI models report honest accuracy when they build schizophrenia classifiers from brain MRI?**

An evaluation for the [micro1 Eval Hackathon](https://www.hackerrank.com/event/micro1-eval-hackathon) by Adeniji Elijah Adetomiwa.

| | |
|---|---|
| **Domain** | Psychiatric neuroimaging × machine learning |
| **Gap tested** | Evaluation leakage: models report accuracy that their classifier will not achieve on new patients |
| **Tasks** | 2 pilot tasks built and validated; 8 planned |
| **Grader** | 100% code-based, with no LLM judge. Validated with 0 false passes and 0 false fails in 120 runs |
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

| ID | Scenario | The trap an expert catches |
|---|---|---|
| **T01** | 80 participants × 5,000 resting-state connectivity features. The lab pipeline is z-score → top 50 features by ANOVA F-test → linear SVM. | Choosing the top features on the **full** dataset before cross-validation. With far more features than people, noise that happens to match the labels gets selected, including the labels of the test folds. |
| **T02** | 120 participants × 24 MRI slices × 128 features. One diagnosis per participant is required. | Splitting cross-validation folds by **slice** instead of by **person**. Slices of the same brain are near-duplicates, so the model learns to recognise people, not schizophrenia. |
| T03–T08 | In development: tuning without nested CV, repeat scan sessions, oversampling before splitting, site confounds, time-window leakage. | See [PLAN.md](PLAN.md) |

**Why synthetic data?** The grader needs to know the *true* accuracy of any pipeline on new patients, and that is only possible when the data-generating process is known. The generators reproduce the structure that causes each trap:

- **T01** has small *n*, very large *p*, and correlated connectivity edges. It has no diagnostic signal, so honest accuracy is about 0.50.
- **T02** has a strong per-person anatomical "fingerprint" shared across slices, plus a modest real signal. Honest accuracy is about 0.70–0.75.

Seeds are fixed, so every model sees identical data.

## 6. Grading

The grader is [`evalkit/grader.py`](evalkit/grader.py). Each task requires two outputs from the model's script:

- `output/result.json`: `{"estimated_balanced_accuracy": 0.xx}`
- `output/predictions.csv`: one `SZ`/`HC` prediction per new participant

The grader computes:

```
actual = balanced accuracy of the predictions on the hidden labels of the new participants
gap    = estimated_balanced_accuracy − actual
PASS   = valid outputs  AND  −0.20 ≤ gap ≤ +0.15  AND  (T02 only) actual ≥ 0.60
```

- **It grades the outcome, not the method.** Any classifier and any validation scheme passes if the number it reports is honest.
- **The band is asymmetric on purpose.** Honest cross-validation on small samples is slightly pessimistic, because each fold trains on fewer people. Leakage, by contrast, is always optimistic.
- **Every rule is stated in the task instruction.** Nothing is graded that the model was not told.

### Grader validation

[`validate_graders.py`](validate_graders.py) runs correct and deliberately wrong solutions against the real task data, using 10 cross-validation seeds each. Full table: [`results/grader_validation.md`](results/grader_validation.md).

| Solution type | Expected | T01 gap range | T02 gap range | Agreement |
|---|---|---|---|---|
| Reference ([`reference/`](reference)) | PASS | −0.07 to +0.01 | −0.08 to −0.01 | 20/20 |
| Alternative correct, with a different classifier and CV ([`alt_correct/`](alt_correct)) | PASS | −0.18 to +0.03 | 0.00 to +0.07 | 20/20 |
| Leaky pipelines ([`wrong_solutions/`](wrong_solutions)) | FAIL | +0.30 to +0.39 | +0.19 to +0.26 | 30/30 |
| Over-claiming constant predictor | FAIL | +0.40 | +0.40 | 20/20 |
| Honest but useless constant predictor | FAIL (T02 floor) | — | 0.00 | 10/10 |
| Incomplete outputs | FAIL | — | — | 20/20 |

**Result: 0 false fails in 40 correct runs, and 0 false passes in 80 wrong runs.**

## 7. Setup and run

No data downloads are needed. Each trial generates a few MB in a temporary folder and deletes it afterwards.

**Option A, GitHub Codespaces (recommended, uses no laptop storage):** click **Code → Codespaces → Create codespace**. Dependencies install automatically.

**Option B, local, Colab or Kaggle:**

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**Step 1: validate the grader.** This needs no API key and takes about 7 minutes on a laptop CPU.

```bash
python validate_graders.py --seeds 10
```

**Step 2: run models.** This needs an [OpenRouter](https://openrouter.ai) key, which gives one key for every provider.

```bash
cp .env.example .env             # paste your key into .env
python run_eval.py --models <model-id-1>,<model-id-2> --trials 3
```

Use model IDs exactly as listed at [openrouter.ai/models](https://openrouter.ai/models). The run produces:

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
