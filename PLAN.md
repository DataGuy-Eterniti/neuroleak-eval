# Plan: submit by Thu 5 Nov (official deadline Mon 9 Nov, 06:15 Lagos time)

## Done (Day 1, Fri 30 Oct)

- Repo, Codespace, harness and code-based grader built.
- Grader reproduced in a clean Codespace (identical gap values to 4 decimals).
- Free providers wired in (NVIDIA, OpenRouter `:free`).
- Pilot: Nemotron 3 Ultra passed T01 and T02. Strong models know the *textbook* traps.
- Design change: tasks are now **matched pairs** (signposted control vs leakage hidden in provenance or metadata). T03 and T04 built and validated.

## Next

| Day | Date | Goal | Done when |
|---|---|---|---|
| 2 | Sat 31 Oct | Push the T03/T04 update. Pilot all 4 tasks on the working free models (1 trial each). Read the transcripts. Review T03/T04 as the domain expert: are the dictionary and analyst notes realistic? | Pilot table for T01–T04 |
| 3 | Sun 1 Nov | Decide the remaining tasks from the pilot. Build T05 (site confound, see below) and at most one more | `validate_graders.py`: 0 false passes, 0 false fails |
| 4 | Mon 2 Nov | **Upload a first complete ZIP to HackerRank** (safety net). Start full runs | First submission saved |
| 5 | Tue 3 Nov | Full runs: every working model × all tasks × 3 trials. Read every failing transcript | README sections 8–9 filled from real results |
| 6 | Wed 4 Nov | Write the description, hot take and AI-use section yourself. Record the ≤ 5-min video | Video link opens in a private window |
| 7 | Thu 5 Nov | Clean-room test (fresh Codespace, README only). Zip and submit | Final upload done; Fri–Sun spare |

## Backlog

1. **T05 Site confound.** Diagnosis confounded with scanner site; deployment at a new hospital. My first draft used 2 training sites, and honest estimates were too unstable to grade fairly, so it was not shipped. Next version: 4 training sites with differing case mix, where leave-one-site-out CV is the honest estimate.
2. **T06 Oversampling before splitting.** Imbalanced cohort; the PI asks to "balance the classes".
3. **T07 Tuning without nested CV.** Many hyperparameter configurations scored on the same folds.

Drop anything whose leaky gap is not clearly separated from the correct gap in validation.

## Provider notes

- **Working, free:** `openrouter:nvidia/nemotron-3-ultra-550b-a55b:free`, `nvidia:mistralai/mistral-large-4-1t-a52b` (use `--max-tokens 4096`), `openrouter:google/gemma-4-31b-it:free` (untested).
- **Not usable:** Gemini (free tier not available for the project; needs billing). GitHub Models (retired July 2026). On NVIDIA, Kimi K2.6 and Nemotron Ultra 253B are not enabled for the account, and DeepSeek V4.1 Flash timed out.
