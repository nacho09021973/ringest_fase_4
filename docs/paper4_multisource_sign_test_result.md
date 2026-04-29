# Paper 4 — Multi-Source Sign Test Result

## Scope

This note executes the plan fixed in `docs/paper4_multisource_mapping_plan.md`: it runs the active Paper 4 producer on the independent GWTC-4 pSEOBNR YAML and runs the existing sign-test script against the resulting 220 dataset. It then compares the new sign-asymmetry result to the original GWTC-2 TGR IMR result. It does not modify scripts, data, YAML, configs, or any existing outputs. It does not declare candidates.

## Inputs

- External YAML used: `/home/ignac/RINGEST/runs_sync/active/gwtc4_pseobnr_ingest/qnm_events_gwtc4_pseobnr.yml` (17 events, GWTC-4.0 TGR III Table 3 pSEOBNR).
- Producer used (unchanged): `02c_paper4_literature_to_dataset.py`.
- Sign-test script used (unchanged): `tools/paper4_frequency_sign_test.py`.
- Run directories generated:
  - `runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/` (producer output).
  - `runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/` (sign-test output).

## Dataset output

- `qnm_dataset.csv`: 10 rows + header (10 events ingested; 7 events skipped by the producer with reason `M_final_Msun or chi_final is null` for late O4 events GW230628..GW231226 that lack GWOSC PE remnant medians at the time of YAML ingestion).
- `qnm_dataset_220.csv`: 9 rows + header (one ingested event, GW190519_153544, did not pass the producer's existing `is_220_candidate` filter; its `kerr_220_distance` was 0.154, the largest among the ingested cohort).
- N used by sign test: 9.

The 9 events surviving into the 220 dataset are: GW150914, GW170104, GW190521_074359, GW190630_185205, GW190828_063405, GW190910_112807, GW200129_065458, GW200224_222234, GW200311_115853. Five of these (GW150914, GW170104, GW190521_074359, GW190828_063405, GW190910_112807) overlap with the phase1 220 dataset; four (GW190630_185205, GW200129_065458, GW200224_222234, GW200311_115853) are new under this source.

## Sign-test result

From `runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/frequency_sign_test_summary.json`:

- `n_total`: 9
- `n_positive`: 9
- `n_negative`: 0
- `n_zero`: 0
- `p_one_sided_positive`: 0.001953
- `p_two_sided`: 0.003906

Per-event `residual_f` (sorted descending), all positive, magnitudes in `[0.097, 0.821]`:

| event_id | residual_f | sign_f | new vs phase1 |
|---|---:|---:|---|
| GW190828_063405 | 0.821 | +1 | overlap |
| GW150914 | 0.731 | +1 | overlap |
| GW200129_065458 | 0.616 | +1 | new |
| GW200224_222234 | 0.615 | +1 | new |
| GW190521_074359 | 0.610 | +1 | overlap |
| GW200311_115853 | 0.580 | +1 | new |
| GW190910_112807 | 0.284 | +1 | overlap |
| GW170104 | 0.228 | +1 | overlap |
| GW190630_185205 | 0.097 | +1 | new |

## Comparison with GWTC-2 TGR IMR

| source | n_total | n_positive | n_negative | p_one_sided_positive | verdict |
|---|---:|---:|---:|---:|---|
| GWTC-2 TGR IMR (phase1) | 16 | 14 | 2 | 0.00209 | sign asymmetry detected (methodological), source-limited |
| GWTC-4 pSEOBNR | 9 | 9 | 0 | 0.00195 | sign asymmetry reproduced under independent pipeline |

Paired comparison on the 5 overlap events (sign coincidence across pipelines):

| event_id | phase1 residual_f | GWTC-4 pSEOBNR residual_f | sign coincidence |
|---|---:|---:|---|
| GW150914 | +0.863 | +0.731 | yes |
| GW170104 | +0.521 | +0.228 | yes |
| GW190521_074359 | +0.645 | +0.610 | yes |
| GW190828_063405 | +0.429 | +0.821 | yes |
| GW190910_112807 | +0.418 | +0.284 | yes |

5/5 paired events keep a positive sign across pipelines. Magnitudes are typically smaller in GWTC-4 pSEOBNR, consistent with the more conservative `max(|+|, |−|)` sigma convention (which inflates the denominator of `residual_f` and therefore reduces its magnitude without flipping its sign).

## Interpretation

- The population-level positive sign asymmetry in `residual_f` first observed in GWTC-2 TGR IMR (`14/16`, `p_one_sided ≈ 0.0021`) **also appears** in the independent GWTC-4 pSEOBNR source (`9/9`, `p_one_sided ≈ 0.0020`). This is a sign coherence reproduced under an independent pipeline.
- The reproduction holds on the four new events not present in the phase1 dataset. It is therefore not a function of the specific 16-event cohort; the pattern continues into a non-overlapping extension cohort.
- All 5 overlap events keep their positive sign across pipelines. This is consistent with a small population-level offset surviving a pipeline change.
- The result remains methodological. It does not become a candidate, a detection, evidence for beyond-Kerr physics, or a Kerr violation under any branch. The single allowed framing is "population-level sign coherence, reproduced across two independent pipelines".

## Caveats

- Sigma convention differs in the conservative direction. GWTC-4 pSEOBNR uses `sigma = max(|+upper|, |−lower|)` while phase1 used `sigma = mean(+upper, −lower)`. The GWTC-4 sigmas are therefore systematically larger, which mechanically reduces the magnitude of `residual_f` (visible in the comparison table) but does not flip its sign. The reproduction is robust to this deflation.
- Source/pipeline independence is partial. The observed `f_hz` and `tau_ms` are fully pipeline-independent (pSEOBNR ≠ IMR). The Kerr-side prediction `f_kerr_hz` uses `M_final_Msun` and `chi_final` from GWOSC PE in both YAMLs, with different `pe_parameter_run` selections per event. The two sets of remnant point estimates are not identical but share GWOSC PE provenance.
- `N = 9` is small. With 5 overlap and 4 new events, the test is descriptive and individual-event sensitive.
- Event overlap is partial. Out of 17 GWTC-4 pSEOBNR events, 7 were skipped at producer level (missing GWOSC PE remnant medians for late O4 events) and 1 did not pass the existing `is_220_candidate` filter. The 9-event cohort is the maximum currently available without modifying the producer.
- Publication and selection effects persist. Both source papers report only events for which ringdown estimates are deemed reliable; the underlying population is preselected.

## Decision

`sign_asymmetry_reproduced_multisource`.

The positive sign of `residual_f` is observed in 9 of 9 GWTC-4 pSEOBNR events, with `p_one_sided ≈ 0.0020`, matching the GWTC-2 TGR IMR result (`14/16`, `p_one_sided ≈ 0.0021`). All 5 paired overlap events keep a positive sign across the two independent pipelines. The pattern is not pipeline-specific to GWTC-2 TGR IMR.

## Immediate next step

Single next step: write a paired common-event comparison note (`docs/paper4_multisource_paired_comparison.md`) documenting the 5 overlap events as a methodological cross-pipeline coherence record, plus a short statement on the 4 new events. No producer modification, no recalculation, no candidate language, and no Stage 02/03/04 execution is required.
