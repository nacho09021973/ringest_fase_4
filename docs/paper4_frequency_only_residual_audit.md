# Paper 4 — Frequency-Only Residual Audit

## Scope

This is the first descriptive audit under Branch A of the split defined in `docs/paper4_branch_split_frequency_vs_gamma.md`. It ranks the schema-aligned 220 dataset by `|residual_f|` only, using the existing `residual_f` column. It does not modify scripts, data, YAML, configs, or residuals. It does not recalculate Kerr predictions, change thresholds, or declare any candidate. It does not introduce new physical metrics; the only ranking field is `abs_residual_f = |residual_f|`, used as a descriptive sort key.

## Input

- CSV used: `runs/paper4_residual_audit_v1/paper4_220_residuals_descriptive.csv`.
- Schema-aligned dataset that fed the descriptive table: `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv`.
- Active producer (indirect, no execution here): `02c_paper4_literature_to_dataset.py`.
- Repository commit at audit time: `54946d9`.

## Method

- Selected the schema-aligned descriptive 220 table.
- Sorted rows by `|residual_f|` descending, where `residual_f = (f_hz − f_kerr_hz) / sqrt(sigma_f_hz² + sigma_f_kerr_hz²)` is the existing frequency-side standardized residual.
- Did not use `residual_gamma` for the ranking.
- Did not recalculate Kerr predictions, did not change thresholds, did not change any sigma, and did not declare candidates.
- Reported `residual_gamma` only as descriptive context, not as a ranking criterion.

## Frequency-only ranking

Top 10 rows of the 220 descriptive table sorted by `|residual_f|` descending:

| event_id | mode | f_hz | sigma_f_hz | f_kerr_hz | residual_f | abs_residual_f | residual_gamma (context only) | source_paper |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| GW190708_232457 | 220 | 497.0 | 28.0 | 443.564 | 1.010 | 1.010 | 1.569 | GWTC-2 TGR |
| GW150914 | 220 | 248.0 | 7.5 | 233.802 | 0.863 | 0.863 | 1.683 | GWTC-2 TGR |
| GW170814 | 220 | 293.0 | 12.5 | 274.252 | 0.776 | 0.776 | 1.515 | GWTC-2 TGR |
| GW190602_175927 | 220 | 105.0 | 9.5 | 90.274 | 0.734 | 0.734 | 1.008 | GWTC-2 TGR |
| GW190521_074359 | 220 | 198.0 | 7.0 | 185.474 | 0.645 | 0.645 | 1.324 | GWTC-2 TGR |
| GW170104 | 220 | 287.0 | 20.0 | 268.970 | 0.521 | 0.521 | 1.015 | GWTC-2 TGR |
| GW190519_153544 | 220 | 127.0 | 9.0 | 118.229 | 0.442 | 0.442 | 0.788 | GWTC-2 TGR |
| GW190828_063405 | 220 | 239.0 | 10.5 | 224.617 | 0.429 | 0.429 | 0.799 | GWTC-2 TGR |
| GW190910_112807 | 220 | 177.0 | 8.0 | 167.549 | 0.418 | 0.418 | 0.855 | GWTC-2 TGR |
| GW190503_185404 | 220 | 191.0 | 16.0 | 177.385 | 0.399 | 0.399 | 0.644 | GWTC-2 TGR |

(`source_paper` abbreviated as "GWTC-2 TGR" for table fit; full string is "Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog".)

## Observations

Direct counts on the 16-row 220 dataset:

- Rows with `|residual_f| ≥ 3`: 0.
- Rows with `|residual_f| ≥ 2`: 0.
- Rows with `|residual_f| ≥ 1`: 1 (GW190708_232457, at `|residual_f| = 1.010`, marginally above the 1σ mark).
- Maximum `|residual_f|`: 1.010.
- Median `|residual_f|`: 0.423.

Coincidence with the gamma-dominated top rows (cf. `docs/paper4_gamma_systematics_remaining_audit.md`):

- Top-5 frequency rows: GW190708_232457, GW150914, GW170814, GW190602_175927, GW190521_074359.
- Top-5 gamma rows: GW150914, GW190708_232457, GW170814, GW190521_074359, GW170104.
- Four of five rows overlap. The differences are GW190602_175927 (top-5 frequency, #6 in gamma) and GW170104 (top-5 gamma, #6 in frequency). The frequency and gamma rankings are largely the same set of events, in slightly reordered positions. There is no event that becomes a frequency-only outlier without also being gamma-elevated.

Magnitudes:

- The frequency channel does not exhibit any strong outlier: the largest descriptive `|residual_f|` value is 1.010, with all other rows below 1σ. No row reaches 2σ or 3σ on the frequency side.
- The frequency-side ranking is therefore a sub-1σ landscape with one borderline 1σ row, not a population that contains clear physical outliers.

## Interpretation guardrails

- A frequency-only outlier under Branch A is not a candidate. The candidate criteria in `docs/paper4_candidate_criteria.md` and the language constraints fixed in `docs/paper4_branch_split_frequency_vs_gamma.md` continue to apply.
- `residual_gamma` is reported above as context only. Per the branch split, it must not be used as a candidate criterion under either branch.
- Any event with elevated `|residual_f|` would still require a per-event audit of source provenance, mass, spin, and redshift assumptions before any non-descriptive language is permitted.
- The 220 dataset has `N = 16`. Conclusions framed in this audit are limited by this sample size and by the single-source provenance (all rows from GWTC-2 TGR / Table IX IMR).

## Immediate conclusion

`no_frequency_outliers_above_threshold`.

Justification: under conventional standardized-residual thresholds (≥ 2σ for moderate, ≥ 3σ for strong), the 16-row 220 dataset contains zero rows. Even at a 1σ threshold, only a single row (GW190708_232457) is borderline above, and the rest of the table is well below 1σ. The frequency channel does not contain robust descriptive outliers under this audit.

## Next step

Single next step: document that, under Branch A, Paper 4 does not currently have robust frequency-only outliers in the 220 dataset, and therefore no per-event source/mass/spin/redshift audit is triggered by the frequency channel at this stage. No bridge run, Stage 02/03/04 execution, recalculation, or candidate declaration is required for this step.
