# Paper 4 — Multi-Source Paired Comparison

## Scope

This note compares, event by event, the existing 220 `residual_f` values between the phase1 GWTC-2 TGR IMR dataset and the GWTC-4 pSEOBNR dataset, restricted to events present in both. It does not produce per-event candidate language, does not recalculate `f_kerr_hz` or `residual_f`, and does not apply paired statistical tests beyond the descriptive sign-coincidence count. It is the cross-pipeline persistence record for the population-level sign asymmetry already documented in `docs/paper4_frequency_sign_test.md` and reproduced in `docs/paper4_multisource_sign_test_result.md`.

## Inputs

- Phase 1 220 dataset: `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv` (16 rows, GWTC-2 TGR IMR).
- GWTC-4 pSEOBNR 220 dataset: `runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset_220.csv` (9 rows, GWTC-4.0 TGR III Table 3 pSEOBNR).
- Permanent script: `tools/paper4_multisource_paired_comparison.py`.
- Outputs (under `runs/paper4_multisource_paired_comparison_v1/`):
  - `paired_common_events.csv`
  - `paired_comparison_summary.json`
- The `residual_f` and `f_kerr_hz` columns were consumed as-is in both inputs. No recalculation was performed.

## Method

- Filter both inputs to `mode == "220"`.
- Inner join on `event_id`.
- For each common event, record the per-pipeline `residual_f`, `freq_hz`, `sigma_freq_hz`, and `f_kerr_hz`. Compute `delta_residual_f = residual_f_gwtc4 − residual_f_phase1` and `delta_f_hz = freq_hz_gwtc4 − freq_hz_phase1`. Determine `sign_match` from the signs of `residual_f` in each pipeline.
- Report descriptive counts (sign match, both positive) and the medians of `delta_residual_f` and `delta_f_hz`.
- Do not compute paired p-values: with `n_common = 5` and only partial source independence (remnant metadata in both YAMLs shares GWOSC PE provenance, even if `pe_parameter_run` differs per event), formal paired tests would overstate inferential weight. The reported descriptive statistics suffice to establish persistence.

## Results

From `runs/paper4_multisource_paired_comparison_v1/paired_comparison_summary.json`:

- `n_common`: 5
- `n_sign_match`: 5
- `n_both_positive`: 5
- `n_phase1_positive`: 5
- `n_gwtc4_positive`: 5
- `all_common_both_positive`: true
- `median_delta_residual_f`: −0.132
- `median_abs_delta_residual_f`: 0.133
- `median_delta_f_hz`: +5.30 Hz
- `median_abs_delta_f_hz`: 5.30 Hz

All 5 common events keep a positive `residual_f` under both pipelines; the sign coincidence rate is 5/5. The median magnitude of `residual_f` decreases from phase1 to GWTC-4 by ≈ 0.13, consistent with the more conservative `max(|+|, |−|)` sigma convention in GWTC-4 inflating the standardization denominator. The median observed `f_hz` is ≈ 5.3 Hz higher in GWTC-4 pSEOBNR than in phase1 IMR; this is a small descriptive cross-pipeline shift in the observed-side frequency, smaller than typical `sigma_f_hz` for these events.

## Paired table

| event_id | residual_f phase1 | residual_f GWTC-4 | sign_match | delta_residual_f | f_hz phase1 | f_hz GWTC-4 | delta_f_hz |
|---|---:|---:|:-:|---:|---:|---:|---:|
| GW170104 | +0.521 | +0.228 | yes | −0.294 | 287.0 | 284.8 | −2.2 |
| GW190910_112807 | +0.418 | +0.284 | yes | −0.133 | 177.0 | 174.5 | −2.5 |
| GW150914 | +0.863 | +0.731 | yes | −0.132 | 248.0 | 253.3 | +5.3 |
| GW190521_074359 | +0.645 | +0.610 | yes | −0.035 | 198.0 | 204.0 | +6.0 |
| GW190828_063405 | +0.429 | +0.821 | yes | +0.392 | 239.0 | 252.4 | +13.4 |

(rows ordered by `delta_residual_f` ascending)

Across the five overlap events:

- 4/5 events have GWTC-4 `residual_f` of smaller magnitude than phase1; 1/5 (GW190828_063405) is larger in GWTC-4.
- 3/5 events have GWTC-4 `f_hz` higher than phase1 (median +5.3 Hz); 2/5 are slightly lower.
- The `f_kerr_hz` predictions agree exactly in 2/5 events (GW190910_112807, GW190521_074359 — the events whose remnant medians from the two PE runs happen to coincide) and differ by ≤ 5 Hz in the other 3.

## Interpretation

- The same-sign persistence of `residual_f` across pipelines is observed in all 5 common events. Combined with the population-level sign-test reproduction (9/9 in GWTC-4 pSEOBNR), this is a cross-pipeline frequency residual sign coherence record.
- The persistence cannot be attributed to a single source paper or a single pipeline. The observed-side `f_hz` differs by up to 13.4 Hz between IMR and pSEOBNR for the same event, yet the sign of the standardized residual against the corresponding `f_kerr_hz` does not flip in any case.
- The median deflation of `|residual_f|` from phase1 to GWTC-4 (≈ 0.13) is consistent with the documented sigma-convention difference (`max` vs `mean` of asymmetric errors), which inflates the GWTC-4 sigmas. This explains the magnitude shift without requiring any sign-side change.
- The result is methodological. It does not become a candidate, a detection, or evidence for beyond-Kerr physics. Permitted framing is "same-sign persistence across pipelines", "cross-pipeline frequency residual sign coherence", "partial independence only".

## Caveats

- `n_common = 5`. Sign persistence is reported descriptively; no paired p-value is computed.
- Source/pipeline independence is partial. The observed `f_hz` is fully pipeline-independent (pSEOBNR ≠ IMR), but the Kerr-side `f_kerr_hz` uses `M_final_Msun`/`chi_final` from GWOSC PE in both YAMLs (with different `pe_parameter_run` per event). Two events (GW190910_112807, GW190521_074359) inherit identical `f_kerr_hz` values because their remnant medians coincided across PE runs.
- Sigma conventions differ (`mean` in phase1, `max` in GWTC-4 pSEOBNR). The GWTC-4 sigmas are systematically larger; the comparison does not attempt to reconcile them.
- No combined population p-value across pipelines is reported. With non-independent sources (shared remnant provenance), combining the phase1 and GWTC-4 sign tests into a single population p-value would overstate evidence; the two p-values are reported side by side only.
- The result is not interpretable as new physics. The candidate criteria of `docs/paper4_candidate_criteria.md` and the language constraints of `docs/paper4_branch_split_frequency_vs_gamma.md` continue to apply.

## Decision

`paired_sign_persistence_observed`.

All 5 common events retain a positive `residual_f` under both the GWTC-2 TGR IMR baseline and the GWTC-4 pSEOBNR cross-pipeline source. The sign coincidence rate is 5/5; magnitudes are deflated under GWTC-4 in line with its more conservative sigma convention, but no sign flip is observed.

## Immediate next step

Single next step: prepare a methodological synthesis note (`docs/paper4_methodological_synthesis.md`) that integrates, in one place, the four findings of Paper 4 to date — (i) no individual frequency-only outliers above 2σ, (ii) gamma channel systematics-limited, (iii) population-level frequency residual sign asymmetry reproduced across two independent pipelines, (iv) paired common-event sign persistence — without introducing candidate language and without recalculating any quantity. No producer modification, no further runs, and no Stage 02/03/04 execution is required.
