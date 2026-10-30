# Grader validation

False fails: **0** / 12 correct runs  
False passes: **0** / 24 wrong runs

| task                          | solution                              | expected   |   runs |   agree |   mean_gap |   min_gap |   max_gap |
|:------------------------------|:--------------------------------------|:-----------|-------:|--------:|-----------:|----------:|----------:|
| t01_feature_selection_leakage | alt_correct/t01_logreg_single_cv.py   | PASS       |      3 |       3 |     -0.066 |    -0.107 |    -0.018 |
| t01_feature_selection_leakage | reference/t01_solve.py                | PASS       |      3 |       3 |     -0.041 |    -0.07  |    -0.016 |
| t01_feature_selection_leakage | wrong_solutions/broken_outputs.py     | FAIL       |      3 |       3 |    nan     |   nan     |   nan     |
| t01_feature_selection_leakage | wrong_solutions/overclaim_constant.py | FAIL       |      3 |       3 |      0.4   |     0.4   |     0.4   |
| t01_feature_selection_leakage | wrong_solutions/t01_leaky.py          | FAIL       |      3 |       3 |      0.326 |     0.309 |     0.343 |
| t02_slice_level_leakage       | alt_correct/t02_subject_means_rf.py   | PASS       |      3 |       3 |      0.039 |     0.02  |     0.073 |
| t02_slice_level_leakage       | reference/t02_solve.py                | PASS       |      3 |       3 |     -0.056 |    -0.063 |    -0.049 |
| t02_slice_level_leakage       | wrong_solutions/broken_outputs.py     | FAIL       |      3 |       3 |    nan     |   nan     |   nan     |
| t02_slice_level_leakage       | wrong_solutions/honest_constant.py    | FAIL       |      3 |       3 |      0     |     0     |     0     |
| t02_slice_level_leakage       | wrong_solutions/overclaim_constant.py | FAIL       |      3 |       3 |      0.4   |     0.4   |     0.4   |
| t02_slice_level_leakage       | wrong_solutions/t02_leaky.py          | FAIL       |      3 |       3 |      0.218 |     0.212 |     0.223 |
| t02_slice_level_leakage       | wrong_solutions/t02_leaky_linear.py   | FAIL       |      3 |       3 |      0.26  |     0.259 |     0.26  |
