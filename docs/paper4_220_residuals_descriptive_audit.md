# Paper 4 — 220 Residuals Descriptive Audit

## Scope

This is a descriptive audit of Kerr residual columns already present in the schema-aligned Paper 4 QNM dataset. It ranks existing 220 rows by residual size, but it does not identify physical candidates, does not introduce new thresholds, and does not reinterpret any event as a Kerr tension.

## Input

- CSV used: `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv`
- active producer: `02c_paper4_literature_to_dataset.py`
- repository commit: `1eba58e`

## Output

- descriptive table: `runs/paper4_residual_audit_v1/paper4_220_residuals_descriptive.csv`

## Method

- Selected the schema-aligned `qnm_dataset_220.csv`.
- Preserved existing residual columns: `residual_f` and `residual_gamma`.
- Used existing `freq_hz` as output `f_hz`, existing `sigma_freq_hz` as output `sigma_f_hz`, and existing `damping_hz` as output `gamma_hz`.
- Computed only `max_abs_residual = max(abs(residual_f), abs(residual_gamma))` as a descriptive ranking field because both residual columns are present.
- Did not recalculate Kerr predictions.
- Did not change residual definitions, thresholds, row selection, or candidate criteria.

## Coverage

- Rows in descriptive table: 16.
- Residual columns available: `residual_f` and `residual_gamma`.
- Damping residual support is available through `damping_hz`, `gamma_kerr_hz`, and `residual_gamma`.
- The table is sorted by `max_abs_residual` descending.

## Highest-residual events

| event_id | mode | f_hz | f_kerr_hz | residual_f | gamma_hz | gamma_kerr_hz | residual_gamma | max_abs_residual |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| GW150914 | 220 | 248.000 | 233.802 | 0.863 | 238.095 | 203.471 | 1.683 | 1.683 |
| GW190708_232457 | 220 | 497.000 | 443.564 | 1.010 | 476.190 | 391.898 | 1.569 | 1.569 |
| GW170814 | 220 | 293.000 | 274.252 | 0.776 | 270.270 | 226.359 | 1.515 | 1.515 |
| GW190521_074359 | 220 | 198.000 | 185.474 | 0.645 | 185.185 | 155.824 | 1.324 | 1.324 |
| GW170104 | 220 | 287.000 | 268.970 | 0.521 | 285.714 | 244.901 | 1.015 | 1.015 |

## Interpretation guardrails

- These rows are not physical candidates yet.
- Apparent residual ranking requires input and systematic audits before any candidate language is defensible.
- The current schema includes `sigma_M_final_Msun` and `sigma_chi_final`, but their impact on event-level interpretation still needs a dedicated audit; if future rows lack them, that absence must be marked explicitly.
- The sample is small: `N = 16` rows in the 220-filtered table.

## Immediate next step

Audit systematics for the highest-residual events before assigning any preliminary classification.
