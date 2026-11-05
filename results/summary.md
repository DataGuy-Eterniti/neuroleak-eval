# Results

## Per model

| model                                             |   tasks |   trials_per_task |   pass_rate |   pass^k |   pass@k |   total_cost_usd | served_model                           | first_run                 | last_run                  |
|:--------------------------------------------------|--------:|------------------:|------------:|---------:|---------:|-----------------:|:---------------------------------------|:--------------------------|:--------------------------|
| groq:openai/gpt-oss-120b                          |       6 |                 3 |       0.611 |      0.5 |    0.667 |                0 | openai/gpt-oss-120b                    | 2026-11-05T09:42:58+00:00 | 2026-11-05T09:49:25+00:00 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free |       6 |                 1 |       0.611 |      0.5 |    0.833 |                0 | nvidia/nemotron-3-ultra-550b-a55b:free | 2026-11-05T09:50:11+00:00 | 2026-11-05T10:23:35+00:00 |

## Per model x task

| model                                             | task                          |   trials |   passes |   mean_estimate |   mean_actual |   mean_gap |   errors |   pass_rate |   pass^k |   pass@k |
|:--------------------------------------------------|:------------------------------|---------:|---------:|----------------:|--------------:|-----------:|---------:|------------:|---------:|---------:|
| groq:openai/gpt-oss-120b                          | t01_feature_selection_leakage |        3 |        3 |           0.51  |         0.498 |      0.013 |        0 |       1     |        1 |        1 |
| groq:openai/gpt-oss-120b                          | t02_slice_level_leakage       |        3 |        3 |           0.751 |         0.731 |      0.02  |        0 |       1     |        1 |        1 |
| groq:openai/gpt-oss-120b                          | t03_repeat_scans              |        3 |        3 |           0.631 |         0.581 |      0.05  |        0 |       1     |        1 |        1 |
| groq:openai/gpt-oss-120b                          | t04_preselected_features      |        3 |        0 |           0.869 |         0.608 |      0.261 |        0 |       0     |        0 |        0 |
| groq:openai/gpt-oss-120b                          | t05_treatment_leakage         |        3 |        2 |           0.804 |         0.64  |      0.164 |        1 |       0.667 |        0 |        1 |
| groq:openai/gpt-oss-120b                          | t06_oversampling_before_cv    |        3 |        0 |           0.511 |         0.513 |     -0.002 |        3 |       0     |        0 |        0 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t01_feature_selection_leakage |        3 |        3 |           0.499 |         0.498 |      0.002 |        0 |       1     |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t02_slice_level_leakage       |        3 |        3 |           0.825 |         0.753 |      0.072 |        0 |       1     |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t03_repeat_scans              |        3 |        3 |           0.673 |         0.59  |      0.083 |        0 |       1     |        1 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t04_preselected_features      |        3 |        1 |           0.669 |         0.576 |      0.093 |        1 |       0.333 |        0 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t05_treatment_leakage         |        3 |        1 |           0.628 |         0.645 |     -0.018 |        2 |       0.333 |        0 |        1 |
| openrouter:nvidia/nemotron-3-ultra-550b-a55b:free | t06_oversampling_before_cv    |        1 |        0 |           0.781 |         0.63  |      0.151 |        0 |       0     |        0 |        0 |
