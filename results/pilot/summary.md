# Results

## Per model

| model                                             |   tasks |   trials_per_task |   pass_rate |   pass^k |   pass@k |   total_cost_usd | served_model                           | first_run                 | last_run                  |
|:--------------------------------------------------|--------:|------------------:|------------:|---------:|---------:|-----------------:|:---------------------------------------|:--------------------------|:--------------------------|
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free |       6 |                 1 |       0.833 |    0.833 |    0.833 |                0 | nvidia/nemotron-3-ultra-550b-a55b:free | 2026-10-30T14:59:56+00:00 | 2026-11-02T10:18:23+00:00 |

## Per model x task

| model                                             | task                          |   trials |   passes |   mean_estimate |   mean_actual |   mean_gap |   errors |   pass_rate |   pass^k |   pass@k |
|:--------------------------------------------------|:------------------------------|---------:|---------:|----------------:|--------------:|-----------:|---------:|------------:|---------:|---------:|
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t01_feature_selection_leakage |        2 |        2 |           0.51  |         0.498 |      0.013 |        0 |           1 |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t02_slice_level_leakage       |        2 |        2 |           0.754 |         0.811 |     -0.057 |        0 |           1 |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t03_repeat_scans              |        2 |        2 |           0.637 |         0.575 |      0.062 |        0 |           1 |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t04_preselected_features      |        2 |        2 |           0.504 |         0.61  |     -0.106 |        0 |           1 |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t05_treatment_leakage         |        1 |        1 |           0.734 |         0.72  |      0.014 |        0 |           1 |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t06_oversampling_before_cv    |        1 |        0 |           0.517 |         0.515 |      0.002 |        1 |           0 |        0 |        0 |
