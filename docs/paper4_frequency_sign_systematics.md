# Paper 4 — Frequency Sign Systematics Audit

## Scope

This audit asks whether the population-level sign asymmetry detected in `docs/paper4_frequency_sign_test.md` (`14/16 residual_f > 0`, `p_one_sided ≈ 0.002`) can be explained by association with physical or provenance variables already present in the dataset. It produces only descriptive statistics; it does not search for candidates, does not recalculate `f_kerr_hz` or `residual_f`, and does not change thresholds. All numeric results come from a permanent, versionable script.

## Input

- Schema-aligned dataset: `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv`.
- Sign-test event table: `runs/paper4_frequency_sign_test_v1/frequency_sign_test_table.csv`.
- Permanent script: `tools/paper4_frequency_sign_systematics.py`.
- Outputs (under `runs/paper4_frequency_sign_systematics_v1/`):
  - `frequency_sign_systematics_summary.json`
  - `frequency_sign_systematics_numeric.csv`
  - `frequency_sign_systematics_by_sign.csv`
  - `frequency_sign_systematics_sources.csv`
- The `residual_f` column was consumed as-is. No recalculation of any column was performed.

## Method

- Joined the schema-aligned 220 dataset with the sign-test event table on `event_id`.
- For each numeric variable available (`z`, `M_final_Msun`, `chi_final`, `f_kerr_hz`, `freq_hz`, `sigma_freq_hz`, `M_final_detector_Msun`), computed Pearson and Spearman correlations against `residual_f` and against `sign_f` (`+1`/`−1`). Spearman uses pandas `rank(method="average")` and Pearson on the resulting ranks.
- For each numeric variable, computed per-sign mean and standard deviation (population `std(ddof=0)`).
- For categorical provenance variables (`source_paper`, `pole_source`), counted unique values and per-sign tallies.
- No correlation p-values are computed; only point estimates. With `N = 16`, moderate `|r|` can occur by chance and the audit is descriptive.

## Results

Source uniqueness:

- `source_paper`: 1 unique value across all 16 rows. The dataset is fully single-source.
- `pole_source`: 1 unique value across all 16 rows.
- Both fields resolve to the same string: "Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog".

Largest absolute correlations across all `(variable × metric)` pairs:

| variable | metric | value | abs |
|---|---|---:|---:|
| `chi_final` | spearman_sign_f | 0.538 | 0.538 |
| `chi_final` | pearson_sign_f | 0.455 | 0.455 |
| `sigma_freq_hz` | pearson_sign_f | −0.447 | 0.447 |
| `sigma_freq_hz` | spearman_residual_f | −0.422 | 0.422 |
| `sigma_freq_hz` | pearson_residual_f | −0.407 | 0.407 |

Per-sign means and population standard deviations for the audited numeric variables:

| variable | sign | n | mean | std |
|---|---:|---:|---:|---:|
| `z` | −1 | 2 | 0.263 | 0.093 |
| `z` | +1 | 14 | 0.292 | 0.135 |
| `M_final_Msun` | −1 | 2 | 52.4 | 18.1 |
| `M_final_Msun` | +1 | 14 | 63.4 | 20.7 |
| `chi_final` | −1 | 2 | 0.655 | 0.005 |
| `chi_final` | +1 | 14 | 0.704 | 0.034 |
| `f_kerr_hz` | −1 | 2 | 278.0 | 112.9 |
| `f_kerr_hz` | +1 | 14 | 224.8 | 83.5 |
| `freq_hz` | −1 | 2 | 271.5 | 109.5 |
| `freq_hz` | +1 | 14 | 239.4 | 92.0 |
| `sigma_freq_hz` | −1 | 2 | 25.75 | 11.75 |
| `sigma_freq_hz` | +1 | 14 | 14.54 | 6.56 |
| `M_final_detector_Msun` | −1 | 2 | 67.86 | 27.73 |
| `M_final_detector_Msun` | +1 | 14 | 83.89 | 36.66 |

Single-variable correlations against `residual_f` and `sign_f` are below `|r| = 0.55` for every variable audited; most are below `|r| = 0.30`.

## Interpretation

- The sign asymmetry is **source-limited**. All 16 rows share the same `source_paper` and the same `pole_source`. There is no within-dataset way to distinguish a source-/pipeline-driven systematic from a physical effect.
- Among the available numeric variables, **`chi_final`** shows the largest descriptive association with `sign_f` (Spearman ≈ 0.54). The two negative-sign rows have a noticeably lower mean `chi_final` (0.655) than the positive-sign rows (0.704). This is a possible systematic association, not a clean explanation: the difference is built from `n = 2` events on the negative side, and a Spearman of 0.54 with `N = 16` is moderate, not decisive.
- **`sigma_freq_hz`** also shows a notable association: the two negative-sign events have, on average, ~76% larger `sigma_freq_hz` than the positive-sign events (25.75 Hz vs 14.54 Hz). The interpretation is mostly mechanical — large measurement sigma scales `residual_f` down toward zero in the denominator and lets the sign flip more easily — and is not a physical explanation by itself. It is consistent with a small population-level offset being drowned by noise at the lowest-precision events.
- `z`, `M_final_Msun`, `f_kerr_hz`, `freq_hz`, and `M_final_detector_Msun` show only low correlations (`|r| ≤ 0.27`). There is no obvious redshift dependence, no obvious mass dependence, and no obvious frequency-scale dependence in the sign pattern.
- No single variable provides a clean explanation. The result is a small-N descriptive audit with a possible weak `chi_final` association and a consistency check on `sigma_freq_hz` as the noise floor of the sign indicator.
- Allowed language: "possible systematic association", "no obvious single-variable explanation", "source-limited", "small-N descriptive audit". Disallowed: "detection", "evidence", "new physics", "Kerr violation".

## Decision

`source_limited` and `no_single_variable_explanation_found` and `inconclusive_small_N`.

Justification:
- **source_limited**: a single `source_paper` and a single `pole_source` apply to all 16 rows; the audit cannot separate source-driven from non-source-driven systematics within this dataset.
- **no_single_variable_explanation_found**: no audited numeric variable yields `|r|` above 0.55. The largest correlation (`chi_final` × `sign_f`, Spearman 0.54) is moderate and rests on `n = 2` negative-sign events.
- **inconclusive_small_N**: with `N = 16` and `n_negative = 2`, both correlation point estimates and per-sign means are sensitive to a single event flipping sign or being added to the dataset.

## Immediate next step

Single next step: because the dataset is source-limited and no obvious single-variable explanation emerges, the productive direction is multi-source comparison — locate or construct a second-source dataset for the same events (for example by reusing `data/phase1_data/qnm_events_capano2023.yml` or `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml` already present in the repository, or by checking what events overlap between sources) and audit whether the residual_f sign pattern is reproduced under an independent reporting pipeline. No bridge run, Stage 02/03/04 execution, recalculation, or candidate declaration is required for this step.
