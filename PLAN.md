# 7-day plan: submit by Thu 5 Nov (official deadline Mon 9 Nov, 06:15 Lagos time)

| Day | Date | Goal | Done when |
|---|---|---|---|
| 1 | Fri 30 Oct | Repo on GitHub, Codespace running, grader validated, **pilot T01+T02 on 2 models × 1 trial** | `results/summary.md` exists with real pilot numbers |
| 2 | Sat 31 Oct | Read the pilot transcripts. Decide: keep, harden or drop each trap. Lock T03–T08 specs (below) | Each task has a one-line "why it's hard" you agree with |
| 3 | Sun 1 Nov | Build T03–T05: generator, instruction, reference, leaky solution, alt-correct solution | `validate_graders.py`: 0 false passes, 0 false fails |
| 4 | Mon 2 Nov | Build T06–T08 + validate. **Upload a first complete ZIP to HackerRank** (a safety net; only the latest counts) | First submission saved |
| 5 | Tue 3 Nov | Full run: 3–4 models × 8 tasks × 3 trials. Read every failing transcript | README sections 8–9 filled from real results |
| 6 | Wed 4 Nov | Write the short description, hot take and AI-use section yourself. Record the ≤5-min video | Video link opens in a private browser window |
| 7 | Thu 5 Nov | Clean-room test: fresh Codespace → follow README only → reproduce. Zip and submit | Final upload done; Fri–Sun are spare |

## Task backlog (T03–T08) for review

Each must have: a defensible answer, a leaky solution that fails, and a correct alternative that passes.

1. **T03 Hyperparameter tuning on the test folds.** Null data. Tune C × kernel × k on the same folds used to report accuracy, with no nested CV, so picking the best of many configurations inflates the estimate.
2. **T04 Repeat sessions hidden in IDs.** Some participants were scanned twice (`sub-012_ses-1`, `sub-012_ses-2`). They must be grouped by person, not by scan ID.
3. **T05 Oversampling before splitting.** Imbalanced cohort (about 25 SZ vs 95 HC), with an instruction to "handle the imbalance". Duplicating or SMOTE-ing the minority class before cross-validation puts copies in both train and test folds.
4. **T06 Site confound.** In training, most patients come from site A and most controls from site B. The task is to estimate accuracy at a **new hospital**. A classifier that learns the scanner, not the disease, looks great under random CV but collapses at a new site. This needs leave-site-out reasoning.
5. **T07 Scaling and imputation fitted on all data.** This is usually a small effect, so test it first. Keep it only if the generator makes the effect large enough to grade reliably.
6. **T08 fMRI time windows as samples.** Sliding windows from one person's time series are autocorrelated near duplicates. This is like T02 but in the time domain.

Drop anything whose leaky gap is not clearly separated from the correct gap in validation.

## GitHub (do first)

Repo name suggestion: `NeuroFusion-SZ/neuroleak-eval` (or under your personal account). Keep it **private** until submission, then make it public.
