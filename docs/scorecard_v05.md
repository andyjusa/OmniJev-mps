# OmniJev v0.5 scorecard

Held-out rows only (row-hash bucket never trained on). **Serving path** = the exact code the API and demos run (mso.infer.MSO1, calibrated temperatures noul 2.57 / choice 2.60 / score 2.42); **batch** = the per-question batch evaluator, whose old build rendered the data's 'none of the above' as a text option the model never trained on (fixed 09-23 14:55; batch numbers are lower bounds on questions with that option). v0.4 and the 2B are batch numbers. Qwen3.5-0.8B = branch-path model trained for 2,500 steps on five families, scored on the same 1,500-question samples as a 4B re-run. Zero-shot = Qwen3-VL-4B-Instruct letter-logprob probe on a subset of the same questions.

| benchmark | n | **4B v0.5 (serving)** | 4B v0.5 (batch) | v0.4 | 2B | 0.8B / 4B on same 1,500 | zero-shot 4B | ECE (serving, calibrated) | Brier | abstain / should |
|---|---|---|---|---|---|---|---|---|---|---|
| LIBERO-10 long-horizon robot (held-out episodes) _(zero-shot probe 1,000 q)_ | 11288 | **0.821** | 0.820 | 0.758 | 0.765 | 0.652 / 0.810 | 0.438 | 0.081 | 0.259 | 0.00 / 0.00 |
| Mind2Web test task/website/domain _(serving path on an 8,000-q sample; batch on all 30,260; zero-shot probe 1,000 q)_ | 8000 | **0.770** | 0.761 | 0.724 | 0.673 | - | 0.549 | 0.075 | 0.327 | 0.00 / 0.04 |
| Grid pointing, 96 cells (web + phone) _(serving path on the web half only; batch on both halves; zero-shot probe 1,000 q (web half))_ | 2178 | **0.729** | 0.690 | 0.600 | 0.588 | - | 0.487 | 0.108 | 0.394 | 0.00 / 0.00 |
| Wiki navigation _(batch evaluator only (data not on the A100))_ | 5744 | - | 0.701 | 0.700 | 0.697 | - | 0.556 | 0.066 | 0.345 | 0.82 / 0.12 |
| Long video / planning / spatial / LIBERO-Spatial (v0.2 families) _(batch only; zero-shot probe 2,338 q)_ | 3328 | - | 0.686 | 0.676 | 0.548 | - | 0.556 | 0.078 | 0.419 | 0.14 / 0.08 |
| LongVideoBench val (500) _(zero-shot probe 366 q)_ | 500 | **0.588** | 0.576 | 0.550 | 0.506 | - | 0.604 | 0.095 | 0.557 | 0.00 / 0.00 |
| OK-VQA answer pool (2,000) _(zero-shot probe 1,000 q)_ | 2000 | **0.893** | 0.851 | - | 0.802 | - | 0.927 | 0.029 | 0.161 | 0.00 / 0.00 |
| Mixed decision set (self-built): regions, existence, phone ops, chess, 4-frame video _(batch only; zero-shot probe 1,724 q)_ | 6661 | - | 0.819 | 0.805 | 0.745 | - | 0.656 | 0.054 | 0.258 | 0.10 / 0.07 |
| Charades-STA video events _(zero-shot probe 1,000 q)_ | 2635 | **0.864** | 0.851 | - | 0.845 | 0.751 / 0.868 | 0.550 | 0.072 | 0.223 | 0.00 / 0.00 |
| Catch game frames _(zero-shot probe 1,000 q)_ | 3764 | **0.885** | 0.884 | - | 0.833 | 0.653 / 0.870 | 0.314 | 0.037 | 0.175 | 0.00 / 0.00 |
| HaGRID gestures + fire/smoke/weapons _(zero-shot probe 1,000 q)_ | 3835 | **0.974** | 0.883 | - | 0.967 | 0.919 / 0.989 | 0.760 | 0.017 | 0.044 | 0.00 / 0.00 |

Reading the table: accuracy is temperature-free; ECE/Brier use the served temperatures. The 0.8B column is a small-model / short-run point on the ladder, not a tuned result.

## LIBERO-10 long-horizon robot (held-out episodes)

| question | n | acc |
|---|---|---|
| which instruction (`r2_instr`) | 1411 | 0.994 |
| which sub-task now (`r2_phase`) | 1411 | 0.837 |
| gripper direction (6-way) (`r2_dir`) | 1411 | 0.456 |
| grasp within 2 s (`r2_grasp`) | 1411 | 0.873 |
| holding an object (`r2_hold`) | 1411 | 0.818 |
| first part done (`r2_first`) | 1411 | 0.926 |
| task done (`r2_done`) | 1411 | 0.924 |
| progress level (`r2_prog`) | 1411 | 0.743 |

## Mind2Web test task/website/domain

| question | n | acc |
|---|---|---|
| operation type (`w2`) | 1600 | 0.873 |
| action as stated? (`w3`) | 1600 | 0.876 |
| last step? (`w4`) | 1600 | 0.896 |
| progress level (`w5`) | 1600 | 0.646 |
| which element (`w1`) | 1460 | 0.614 |
| which element (100+ candidates) (`w1a`) | 140 | 0.000 |

## Grid pointing, 96 cells (web + phone)

| question | n | acc |
|---|---|---|
| coarse cell (96) (`pt_coarse`) | 515 | 0.433 |
| target inside proposed? (`pt_in_coarse`) | 515 | 0.812 |
| target outside? (`pt_out_coarse`) | 509 | 0.943 |
| fine cell (96) (`pt_fine`) | 214 | 0.416 |
| target inside (fine)? (`pt_in_fine`) | 214 | 0.874 |
| target outside (fine)? (`pt_out_fine`) | 211 | 0.900 |

## Wiki navigation (batch evaluator)

| question | n | acc |
|---|---|---|
| n1 (`n1`) | 1436 | 0.290 |
| n2 (`n2`) | 1436 | 1.000 |
| n3 (`n3`) | 1436 | 0.829 |
| n4 (`n4`) | 1436 | 0.685 |

## Long video / planning / spatial / LIBERO-Spatial (v0.2 families) (batch evaluator)

| question | n | acc |
|---|---|---|
| s1 (`s1`) | 250 | 0.744 |
| s2 (`s2`) | 166 | 0.319 |
| c1_0 (`c1_0`) | 109 | 0.156 |
| c1_1 (`c1_1`) | 109 | 0.193 |
| c2_p0 (`c2_p0`) | 109 | 0.798 |
| c2_n0 (`c2_n0`) | 109 | 0.817 |
| c2_n1 (`c2_n1`) | 109 | 0.789 |
| c3_p (`c3_p`) | 109 | 0.807 |
| c3_n (`c3_n`) | 109 | 0.844 |
| c5 (`c5`) | 109 | 1.000 |
| c6 (`c6`) | 109 | 0.569 |
| c7 (`c7`) | 109 | 0.303 |
| p1_0 (`p1_0`) | 109 | 0.505 |
| p1_1 (`p1_1`) | 109 | 0.587 |
| p2_0 (`p2_0`) | 109 | 0.908 |
| p2_1 (`p2_1`) | 109 | 0.899 |
| p4 (`p4`) | 109 | 0.550 |
| l1_0 (`l1_0`) | 108 | 0.815 |
| l1_1 (`l1_1`) | 108 | 0.750 |
| c2_p1 (`c2_p1`) | 104 | 0.846 |
| c4 (`c4`) | 75 | 0.733 |
| p5 (`p5`) | 75 | 0.707 |
| s4_0 (`s4_0`) | 59 | 0.814 |
| c1_neg (`c1_neg`) | 39 | 0.949 |

## LongVideoBench val (500)

| question | n | acc |
|---|---|---|
| q (`q`) | 500 | 0.588 |

## OK-VQA answer pool (2,000)

| question | n | acc |
|---|---|---|
| OK-VQA pool choice (`vqa`) | 2000 | 0.893 |

## Mixed decision set (self-built): regions, existence, phone ops, chess, 4-frame video (batch evaluator)

| question | n | acc |
|---|---|---|
| t0 (`t0`) | 498 | 0.922 |
| t1 (`t1`) | 498 | 0.920 |
| t2 (`t2`) | 498 | 0.888 |
| t3 (`t3`) | 498 | 0.882 |
| t4 (`t4`) | 498 | 0.894 |
| t5 (`t5`) | 498 | 0.890 |
| a0 (`a0`) | 166 | 0.892 |
| c0 (`c0`) | 166 | 0.843 |
| d0 (`d0`) | 166 | 0.741 |
| c1 (`c1`) | 165 | 0.812 |
| a1 (`a1`) | 150 | 0.820 |
| i1 (`i1`) | 132 | 0.864 |
| a2 (`a2`) | 130 | 0.731 |
| b0 (`b0`) | 126 | 0.278 |
| b1 (`b1`) | 126 | 0.651 |
| a3 (`a3`) | 94 | 0.691 |
| i2_0 (`i2_0`) | 82 | 0.963 |
| i2_1 (`i2_1`) | 82 | 0.988 |
| i2_2 (`i2_2`) | 82 | 0.976 |
| i3 (`i3`) | 82 | 0.976 |
| a4 (`a4`) | 81 | 0.741 |
| g1 (`g1`) | 81 | 0.951 |
| g2 (`g2`) | 81 | 0.975 |
| g3 (`g3`) | 81 | 0.975 |
| g6 (`g6`) | 81 | 0.519 |
| g7 (`g7`) | 81 | 0.926 |
| g4_0 (`g4_0`) | 78 | 0.756 |
| g4_1 (`g4_1`) | 78 | 0.859 |
| g5 (`g5`) | 78 | 0.705 |
| i2_3 (`i2_3`) | 76 | 0.974 |
| h2_0 (`h2_0`) | 72 | 0.556 |
| h2_1 (`h2_1`) | 72 | 0.833 |
| h2_2 (`h2_2`) | 72 | 0.736 |
| h2_3 (`h2_3`) | 72 | 0.750 |
| h4 (`h4`) | 72 | 0.319 |
| a5 (`a5`) | 68 | 0.647 |
| a6 (`a6`) | 60 | 0.667 |
| h1 (`h1`) | 55 | 0.309 |
| a7 (`a7`) | 48 | 0.646 |
| a8 (`a8`) | 41 | 0.585 |
| a9 (`a9`) | 35 | 0.429 |

## Charades-STA video events

| question | n | acc |
|---|---|---|
| did the event happen (`e1`) | 527 | 0.850 |
| which frame it starts (`e2`) | 527 | 0.767 |
| person still in view (`e3`) | 527 | 0.964 |
| whole action shown (`e4`) | 527 | 0.901 |
| what is being done (`e5`) | 527 | 0.837 |

## Catch game frames

| question | n | acc |
|---|---|---|
| paddle move (`g_act`) | 756 | 0.671 |
| bomb about to hit (`g_bomb`) | 756 | 0.996 |
| a ball was missed (`g_miss`) | 756 | 0.828 |
| score standing (`g_score`) | 756 | 0.992 |
| next ball cell (`g_ball`) | 740 | 0.941 |

## HaGRID gestures + fire/smoke/weapons

| question | n | acc |
|---|---|---|
| which gesture (`hg1`) | 637 | 0.987 |
| gesture yes/no (`hg2`) | 637 | 0.986 |
| device command (`hg3`) | 637 | 0.975 |
| fire or smoke? (`hz1`) | 481 | 1.000 |
| urgency (`hz3`) | 481 | 0.979 |
| hazard kind (`hz4`) | 481 | 1.000 |
| which region (`hz2`) | 481 | 0.881 |
