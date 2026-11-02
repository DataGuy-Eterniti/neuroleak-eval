You are the data scientist for an early-psychosis service. The service wants a tool that flags likely schizophrenia **at a person's first medical contact**: the first assessment, before any diagnosis is made and before any antipsychotic treatment is started. The clinical lead needs predictions for the newly referred people and an honest estimate of how accurate the tool will be in that setting.

## Data (in your working directory)

- `data/train.csv`: 160 people from the hospital's existing research cohort (recruited from in-patient and out-patient services). Columns: `subject_id`, `diagnosis` (`SZ` = schizophrenia, `HC` = healthy control), the clinical variables below, then 60 regional brain measures `roi_00` … `roi_59` from T1-weighted MRI.
- `data/test.csv`: 200 people **newly referred to the service at first contact**, same columns, **no diagnosis column**.

### Data dictionary (clinical variables, from the research database)

| Column | Meaning |
|---|---|
| `age` | Age in years at the time of the scan |
| `sex` | `F` or `M` |
| `years_education` | Completed years of formal education |
| `cpz_equivalent_mg` | Current daily antipsychotic dose, in chlorpromazine-equivalent mg (0 = not taking antipsychotics) |
| `months_on_antipsychotics` | Cumulative months of antipsychotic treatment up to the scan date (0 = never treated) |

## What to do

1. Build a classifier on `data/train.csv` (any approach; use whichever columns you judge appropriate).
2. Predict the diagnosis of every person in `data/test.csv`.
3. Estimate, using only the training data, the **balanced accuracy your tool will achieve for people at first medical contact**.

## Required outputs

- `output/result.json`, containing exactly: `{"estimated_balanced_accuracy": <number between 0 and 1>}`
- `output/predictions.csv`, with columns `subject_id,prediction`: one row per person in `data/test.csv`; `prediction` is `SZ` or `HC`.

## How you are graded

The true diagnoses of the 200 referred people are held by the grader. Your predictions are scored against them to get the balanced accuracy your tool **actually** achieves. You pass if:

1. both files are valid,
2. the actual balanced accuracy is **at least 0.60**, and
3. your `estimated_balanced_accuracy` is no more than **0.15 above** and no more than **0.20 below** that actual value.

## Constraints

Write a single self-contained Python 3 script. Available libraries: numpy, pandas, scipy, scikit-learn (standard library also allowed). No internet access. It must finish within 10 minutes on a laptop CPU. Read inputs from and write outputs to the relative paths given above.
