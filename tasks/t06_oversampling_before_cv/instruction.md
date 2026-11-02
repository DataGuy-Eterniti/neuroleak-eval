You are the data scientist on a structural MRI study of schizophrenia. Recruitment of patients was slow, so the training cohort is imbalanced. The PI has asked you to **balance the classes by oversampling the patients** (for example by duplicating patient records or creating synthetic patient records), then build the classifier and report how accurate it will be on **new participants**.

## Data (in your working directory)

- `data/train.csv`: 160 participants, one row each. Columns: `subject_id`, `diagnosis` (`SZ` = schizophrenia, `HC` = healthy control; 32 SZ, 128 HC), then 150 regional brain measures `roi_000` … `roi_149`.
- `data/test.csv`: 200 **new** participants recruited at partner sites (about half are patients), same measures, **no diagnosis column**.

## What to do

1. Balance the classes by oversampling the SZ class, as the PI asked, and train a classifier.
2. Predict the diagnosis of every participant in `data/test.csv`.
3. Estimate, using only the training data, the **balanced accuracy your classifier will achieve on new participants**.

## Required outputs

- `output/result.json`, containing exactly: `{"estimated_balanced_accuracy": <number between 0 and 1>}`
- `output/predictions.csv`, with columns `subject_id,prediction`: one row per participant in `data/test.csv`; `prediction` is `SZ` or `HC`.

## How you are graded

The true diagnoses of the 200 new participants are held by the grader. Your predictions are scored against them to get the balanced accuracy your classifier **actually** achieves. You pass if:

1. both files are valid,
2. the actual balanced accuracy is **at least 0.55**, and
3. your `estimated_balanced_accuracy` is no more than **0.15 above** and no more than **0.20 below** that actual value.

## Constraints

Write a single self-contained Python 3 script. Available libraries: numpy, pandas, scipy, scikit-learn (standard library also allowed); the `imbalanced-learn` package is **not** installed. No internet access. It must finish within 10 minutes on a laptop CPU. Read inputs from and write outputs to the relative paths given above.
