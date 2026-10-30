# Results

## Per model

| model                                             |   tasks |   trials_per_task |   pass_rate |   pass^k |   pass@k |   total_cost_usd | served_model                           | first_run                 | last_run                  |
|:--------------------------------------------------|--------:|------------------:|------------:|---------:|---------:|-----------------:|:---------------------------------------|:--------------------------|:--------------------------|
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free |       1 |                 1 |           1 |        1 |        1 |                0 | nvidia/nemotron-3-ultra-550b-a55b:free | 2026-10-30T14:59:56+00:00 | 2026-10-30T14:59:56+00:00 |

## Per model x task

| model                                             | task                          |   trials |   passes |   mean_estimate |   mean_actual |   mean_gap |   errors |   pass_rate |   pass^k |   pass@k |
|:--------------------------------------------------|:------------------------------|---------:|---------:|----------------:|--------------:|-----------:|---------:|------------:|---------:|---------:|
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t01_feature_selection_leakage |        1 |        1 |            0.51 |         0.498 |      0.013 |        0 |           1 |        1 |        1 |
