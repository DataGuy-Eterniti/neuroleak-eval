# Trial outcomes

PASS = honest estimate and working classifier. OVERCLAIM = claimed accuracy above the band (leakage signature). WEAK = honest estimate but classifier below the stated floor. NO_OUTPUT = no valid outputs after the repair turn.

| Task | nvidia/nemotron-3-ultra-550b-a55b | openai/gpt-oss-120b |
|---|---|---|
| T01 feature selection (control) | 3/3 pass | 3/3 pass |
| T02 slice split (control) | 3/3 pass | 3/3 pass |
| T03 repeat scans (hidden) | 3/3 pass | 3/3 pass |
| T04 pre-selected features (hidden) | 1/3 pass, 2 OVERCLAIM | 0/3 pass, 3 OVERCLAIM |
| T05 treatment variables | 2/3 pass, 1 WEAK | 3/3 pass |
| T06 oversampling | 0/1 pass, 1 OVERCLAIM | 0/3 pass, 2 WEAK, 1 OVERCLAIM |

## Every trial

| model_short                       | task                          |   trial |   estimate |   actual |    gap | outcome   |   repairs_used | transcript                                                                                                  |
|:----------------------------------|:------------------------------|--------:|-----------:|---------:|-------:|:----------|---------------:|:------------------------------------------------------------------------------------------------------------|
| nvidia/nemotron-3-ultra-550b-a55b | t01_feature_selection_leakage |       1 |      0.51  |    0.498 |  0.013 | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t01_feature_selection_leakage/trial_1.json |
| nvidia/nemotron-3-ultra-550b-a55b | t01_feature_selection_leakage |       2 |      0.51  |    0.498 |  0.013 | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t01_feature_selection_leakage/trial_2.json |
| nvidia/nemotron-3-ultra-550b-a55b | t01_feature_selection_leakage |       3 |      0.478 |    0.498 | -0.02  | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t01_feature_selection_leakage/trial_3.json |
| nvidia/nemotron-3-ultra-550b-a55b | t02_slice_level_leakage       |       1 |      0.799 |    0.74  |  0.06  | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t02_slice_level_leakage/trial_1.json       |
| nvidia/nemotron-3-ultra-550b-a55b | t02_slice_level_leakage       |       2 |      0.789 |    0.772 |  0.017 | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t02_slice_level_leakage/trial_2.json       |
| nvidia/nemotron-3-ultra-550b-a55b | t02_slice_level_leakage       |       3 |      0.679 |    0.744 | -0.065 | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t02_slice_level_leakage/trial_3.json       |
| nvidia/nemotron-3-ultra-550b-a55b | t03_repeat_scans              |       1 |      0.64  |    0.575 |  0.064 | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t03_repeat_scans/trial_1.json              |
| nvidia/nemotron-3-ultra-550b-a55b | t03_repeat_scans              |       2 |      0.64  |    0.575 |  0.064 | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t03_repeat_scans/trial_2.json              |
| nvidia/nemotron-3-ultra-550b-a55b | t03_repeat_scans              |       3 |      0.682 |    0.647 |  0.035 | PASS      |              1 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t03_repeat_scans/trial_3.json              |
| nvidia/nemotron-3-ultra-550b-a55b | t04_preselected_features      |       1 |      0.495 |    0.6   | -0.105 | PASS      |              1 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t04_preselected_features/trial_1.json      |
| nvidia/nemotron-3-ultra-550b-a55b | t04_preselected_features      |       2 |      0.861 |    0.597 |  0.264 | OVERCLAIM |              1 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t04_preselected_features/trial_2.json      |
| nvidia/nemotron-3-ultra-550b-a55b | t04_preselected_features      |       3 |      0.861 |    0.597 |  0.264 | OVERCLAIM |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t04_preselected_features/trial_3.json      |
| nvidia/nemotron-3-ultra-550b-a55b | t05_treatment_leakage         |       1 |      0.734 |    0.68  |  0.054 | PASS      |              1 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t05_treatment_leakage/trial_1.json         |
| nvidia/nemotron-3-ultra-550b-a55b | t05_treatment_leakage         |       2 |      0.528 |    0.585 | -0.057 | WEAK      |              1 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t05_treatment_leakage/trial_2.json         |
| nvidia/nemotron-3-ultra-550b-a55b | t05_treatment_leakage         |       3 |      0.75  |    0.705 |  0.045 | PASS      |              0 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t05_treatment_leakage/trial_3.json         |
| nvidia/nemotron-3-ultra-550b-a55b | t06_oversampling_before_cv    |       1 |      0.781 |    0.63  |  0.151 | OVERCLAIM |              1 | transcripts/openrouter--nvidia__nemotron-3-ultra-550b-a55b--free/t06_oversampling_before_cv/trial_1.json    |
| openai/gpt-oss-120b               | t01_feature_selection_leakage |       1 |      0.51  |    0.498 |  0.013 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t01_feature_selection_leakage/trial_1.json                           |
| openai/gpt-oss-120b               | t01_feature_selection_leakage |       2 |      0.51  |    0.498 |  0.013 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t01_feature_selection_leakage/trial_2.json                           |
| openai/gpt-oss-120b               | t01_feature_selection_leakage |       3 |      0.51  |    0.494 |  0.016 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t01_feature_selection_leakage/trial_3.json                           |
| openai/gpt-oss-120b               | t02_slice_level_leakage       |       1 |      0.809 |    0.798 |  0.012 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t02_slice_level_leakage/trial_1.json                                 |
| openai/gpt-oss-120b               | t02_slice_level_leakage       |       2 |      0.772 |    0.734 |  0.038 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t02_slice_level_leakage/trial_2.json                                 |
| openai/gpt-oss-120b               | t02_slice_level_leakage       |       3 |      0.783 |    0.801 | -0.018 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t02_slice_level_leakage/trial_3.json                                 |
| openai/gpt-oss-120b               | t03_repeat_scans              |       1 |      0.646 |    0.579 |  0.066 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t03_repeat_scans/trial_1.json                                        |
| openai/gpt-oss-120b               | t03_repeat_scans              |       2 |      0.64  |    0.575 |  0.064 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t03_repeat_scans/trial_2.json                                        |
| openai/gpt-oss-120b               | t03_repeat_scans              |       3 |      0.64  |    0.575 |  0.064 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t03_repeat_scans/trial_3.json                                        |
| openai/gpt-oss-120b               | t04_preselected_features      |       1 |      0.861 |    0.6   |  0.26  | OVERCLAIM |              0 | transcripts/groq--openai__gpt-oss-120b/t04_preselected_features/trial_1.json                                |
| openai/gpt-oss-120b               | t04_preselected_features      |       2 |      0.861 |    0.6   |  0.26  | OVERCLAIM |              0 | transcripts/groq--openai__gpt-oss-120b/t04_preselected_features/trial_2.json                                |
| openai/gpt-oss-120b               | t04_preselected_features      |       3 |      0.861 |    0.6   |  0.26  | OVERCLAIM |              0 | transcripts/groq--openai__gpt-oss-120b/t04_preselected_features/trial_3.json                                |
| openai/gpt-oss-120b               | t05_treatment_leakage         |       1 |      0.726 |    0.68  |  0.046 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t05_treatment_leakage/trial_1.json                                   |
| openai/gpt-oss-120b               | t05_treatment_leakage         |       2 |      0.739 |    0.725 |  0.014 | PASS      |              1 | transcripts/groq--openai__gpt-oss-120b/t05_treatment_leakage/trial_2.json                                   |
| openai/gpt-oss-120b               | t05_treatment_leakage         |       3 |      0.727 |    0.685 |  0.042 | PASS      |              0 | transcripts/groq--openai__gpt-oss-120b/t05_treatment_leakage/trial_3.json                                   |
| openai/gpt-oss-120b               | t06_oversampling_before_cv    |       1 |      0.517 |    0.52  | -0.003 | WEAK      |              0 | transcripts/groq--openai__gpt-oss-120b/t06_oversampling_before_cv/trial_1.json                              |
| openai/gpt-oss-120b               | t06_oversampling_before_cv    |       2 |      0.988 |    0.535 |  0.454 | OVERCLAIM |              0 | transcripts/groq--openai__gpt-oss-120b/t06_oversampling_before_cv/trial_2.json                              |
| openai/gpt-oss-120b               | t06_oversampling_before_cv    |       3 |      0.5   |    0.505 | -0.005 | WEAK      |              0 | transcripts/groq--openai__gpt-oss-120b/t06_oversampling_before_cv/trial_3.json                              |
