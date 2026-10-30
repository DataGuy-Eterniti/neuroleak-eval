# Grader validation

False fails: **0** / 40 correct runs  
False passes: **0** / 80 wrong runs

| task                          | solution                              | expected   |   runs |   agree |   mean_gap |   min_gap |   max_gap |
|:------------------------------|:--------------------------------------|:-----------|-------:|--------:|-----------:|----------:|----------:|
| t01_feature_selection_leakage | alt_correct/t01_logreg_single_cv.py   | PASS       |     10 |      10 |     -0.051 |    -0.178 |     0.029 |
| t01_feature_selection_leakage | reference/t01_solve.py                | PASS       |     10 |      10 |     -0.031 |    -0.07  |     0.006 |
| t01_feature_selection_leakage | wrong_solutions/broken_outputs.py     | FAIL       |     10 |      10 |    nan     |   nan     |   nan     |
| t01_feature_selection_leakage | wrong_solutions/overclaim_constant.py | FAIL       |     10 |      10 |      0.4   |     0.4   |     0.4   |
| t01_feature_selection_leakage | wrong_solutions/t01_leaky.py          | FAIL       |     10 |      10 |      0.34  |     0.3   |     0.391 |
| t02_slice_level_leakage       | alt_correct/t02_subject_means_rf.py   | PASS       |     10 |      10 |      0.037 |     0.004 |     0.073 |
| t02_slice_level_leakage       | reference/t02_solve.py                | PASS       |     10 |      10 |     -0.053 |    -0.076 |    -0.014 |
| t02_slice_level_leakage       | wrong_solutions/broken_outputs.py     | FAIL       |     10 |      10 |    nan     |   nan     |   nan     |
| t02_slice_level_leakage       | wrong_solutions/honest_constant.py    | FAIL       |     10 |      10 |      0     |     0     |     0     |
| t02_slice_level_leakage       | wrong_solutions/overclaim_constant.py | FAIL       |     10 |      10 |      0.4   |     0.4   |     0.4   |
| t02_slice_level_leakage       | wrong_solutions/t02_leaky.py          | FAIL       |     10 |      10 |      0.213 |     0.192 |     0.223 |
| t02_slice_level_leakage       | wrong_solutions/t02_leaky_linear.py   | FAIL       |     10 |      10 |      0.26  |     0.259 |     0.262 |
