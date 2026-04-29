# Paper 4 — Frequency Residual Sign Test

## Scope

This note tests population-level sign coherence in `residual_f` across the 220 dataset, using an exact binomial test on the existing residual column. It is not a candidate search and does not produce per-event physical claims. It does not modify scripts, data, YAML, configs, or residuals; the test runs through a permanent script and consumes the existing schema-aligned dataset without recalculation.

## Input

- CSV used: `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv`.
- Permanent script used: `tools/paper4_frequency_sign_test.py`.
- Outputs written to: `runs/paper4_frequency_sign_test_v1/` (`frequency_sign_test_summary.json`, `frequency_sign_test_table.csv`).
- The `residual_f` column already existed in the input CSV. The script does not recalculate `f_kerr_hz`, `sigma_f_hz`, or `residual_f`; it consumes them as-is.

## Method

- For every row with a non-NaN `residual_f`, classify the sign as `+1`, `−1`, or `0`.
- Count `n_total`, `n_positive`, `n_negative`, `n_zero`.
- Test under the null hypothesis `H0: P(residual_f > 0) = 0.5`.
- Compute `p_one_sided_positive = P(K ≥ n_positive | n_total, 0.5)` for the positive-bias alternative.
- Compute `p_two_sided = min(2 · min(P(K ≥ n_positive), P(K ≤ n_positive)), 1)`.
- Implementation uses `math.comb` only; no scipy.
- Zero handling: zeros (`residual_f == 0`) are counted as not-positive and the binomial test uses `n_total` (zeros included in the denominator). With zero exact zeros in this dataset, this convention does not affect the result.

## Results

From `runs/paper4_frequency_sign_test_v1/frequency_sign_test_summary.json`:

- `n_total`: 16
- `n_positive`: 14
- `n_negative`: 2
- `n_zero`: 0
- `p_one_sided_positive`: 0.00209
- `p_two_sided`: 0.00418

The observed split is 14/2 in favor of `residual_f > 0`. Under H0, the probability of observing at least 14 positives out of 16 is `≈ 0.0021`; the symmetric two-sided variant is `≈ 0.0042`.

## Event table

Rows sorted by `residual_f` descending (full 16-row 220 dataset):

| event_id | residual_f | sign_f | source_paper |
|---|---:|---:|---|
| GW190708_232457 | 1.010 | +1 | GWTC-2 TGR |
| GW150914 | 0.863 | +1 | GWTC-2 TGR |
| GW170814 | 0.776 | +1 | GWTC-2 TGR |
| GW190602_175927 | 0.734 | +1 | GWTC-2 TGR |
| GW190521_074359 | 0.645 | +1 | GWTC-2 TGR |
| GW170104 | 0.521 | +1 | GWTC-2 TGR |
| GW190519_153544 | 0.442 | +1 | GWTC-2 TGR |
| GW190828_063405 | 0.429 | +1 | GWTC-2 TGR |
| GW190910_112807 | 0.418 | +1 | GWTC-2 TGR |
| GW190503_185404 | 0.399 | +1 | GWTC-2 TGR |
| GW170823 | 0.294 | +1 | GWTC-2 TGR |
| GW190408_181802 | 0.291 | +1 | GWTC-2 TGR |
| GW190915_235702 | 0.119 | +1 | GWTC-2 TGR |
| GW190513_205428 | 0.022 | +1 | GWTC-2 TGR |
| GW190421_213856 | −0.090 | −1 | GWTC-2 TGR |
| GW190512_180714 | −0.157 | −1 | GWTC-2 TGR |

(`source_paper` abbreviated as "GWTC-2 TGR"; full string: "Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog".)

The two negative residuals are also the two smallest in absolute value among all 16 rows (`|residual_f| = 0.090, 0.157`), close to the noise floor of the test.

## Interpretation

- The 220 dataset shows a population-level sign asymmetry: `f_obs > f_kerr` in 14 of 16 rows, with a one-sided exact binomial p-value of `≈ 0.0021`. This is a frequency residual sign asymmetry at the population level.
- The asymmetry cannot be presented as evidence of beyond-Kerr physics. The same source paper, the same pipeline assumptions, and the same Berti interpolation scheme apply to all rows; correlated systematic offsets are the natural first explanation. The result is a methodological observation, not a physical detection.
- It is also not an individual candidate claim. No single row exceeds 2σ in `|residual_f|`, and the sign pattern is, in itself, sub-1σ in magnitude per row.
- The two negative-sign rows have the smallest absolute residuals in the entire dataset, which is consistent with sign-coherence being driven by a small but persistent bias rather than by isolated outliers.
- Allowed language for this finding: "population-level sign coherence", "frequency residual sign asymmetry", "possible systematic bias". Disallowed: "candidate", "Kerr violation", "evidence for beyond-Kerr physics".

## Systematic caveats

The result must be read against several constraints:

- `N = 16` is small; sign tests gain power slowly with N, and a single source-level systematic can drive the entire pattern.
- All 16 rows derive from the same source paper (GWTC-2 TGR Table IX, IMR column). The events are not independent at the pipeline level: they share the IMR waveform family, the same parameter-estimation conventions, and the same selection of preferred PE run.
- The sign asymmetry could be entirely produced by median-mapping non-commutativity: `omega_re(median(M_f, χ_f))` need not equal `median(omega_re(posterior on M_f, χ_f))`, and the difference can be sign-coherent across events with similar posterior shapes.
- The Kerr prediction uses `M_final_Msun` and `chi_final` point estimates (medians) from the same posteriors that produced `f_hz`. Any systematic in the inferred remnant parameters propagates correlationally into `f_kerr_hz` and so into `residual_f`.
- Sigma propagation in `f_kerr_hz` uses `sigma_M_final_Msun` and `sigma_chi_final` as Gaussian symmetric one-sigmas; asymmetric remnant posteriors are not represented.
- Selection: only events for which LVK reported ringdown estimates are present. Events with weaker constraints are absent, so the population is preselected.
- This audit followed several exploratory Phase 4 decisions (dataset schema, residual definition, branch split). The sign test is reported for the dataset as it stands; it does not retroactively justify those decisions.

## Decision

`sign_asymmetry_detected_methodological`.

The dataset shows a statistically non-trivial sign asymmetry in `residual_f` (`p_one_sided ≈ 0.002`), but the interpretation is restricted to a methodological/systematic observation under the caveats listed above.

## Immediate next step

Single next step: audit whether the sign asymmetry is explained by `M_final_Msun`, `chi_final`, redshift `z`, or `source_paper` choices — i.e., check whether the residual-sign pattern correlates with any of those input fields — before any physical interpretation is even considered. No bridge run, Stage 02/03/04 execution, recalculation, or candidate declaration is required for this step.
