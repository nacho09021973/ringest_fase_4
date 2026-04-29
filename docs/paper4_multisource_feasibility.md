# Paper 4 — Multi-Source Feasibility

## Scope

This note evaluates whether a multi-source comparison is feasible — i.e., whether there is a second, independent QNM/remnant data source in the repository (or its sibling RINGEST workspace) that overlaps with the current Paper 4 220 dataset and exposes enough fields to test whether the population-level `residual_f` sign asymmetry reproduces under an independent pipeline. It does not compute new residuals, does not run any producer, does not modify scripts, data, YAML, configs, or any existing outputs. It is a pre-implementation feasibility audit.

## Motivation

`docs/paper4_frequency_sign_test.md` and `docs/paper4_frequency_sign_systematics.md` left the following state:

- 14 of 16 events have `residual_f > 0`, with a one-sided exact binomial p-value of ≈ 0.002.
- The pattern is not explained by `z`, `M_final_Msun`, `chi_final`, `f_kerr_hz`, `freq_hz`, or `M_final_detector_Msun`. The largest single-variable correlation (`chi_final` × `sign_f`, Spearman 0.54) is moderate, fragile (`n = 2` negative-sign events), and source-limited.
- All 16 rows share a single `source_paper` and `pole_source` ("Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog", arXiv:2010.14529, GWTC-2 TGR Table IX IMR).
- Within the current dataset there is no way to distinguish a source/pipeline-driven systematic from a robust pattern. An independent second source is the natural next probe.

## Candidate sources found

The find search returned six paths. Inspecting each:

| path | source label | n_events | has f_hz/sigma_f_hz | has M_final/chi_final | has redshift | has mode labels | provenance clarity | reusable? |
|---|---|---:|---|---|---|---|---|---|
| `data/phase1_data/qnm_events_capano2023.yml` | Capano 2023, PRL 131, 221402 (arXiv:2105.05238) | 1 | yes (`f_hz`, `f_hz_minus`, `f_hz_plus`; asymmetric CI) | no (no `M_final_Msun`/`chi_final`) | no (no `z`) | yes (agnostic ranges A,B with posterior Kerr identification 220, 330) | high; explicit `frame: detector`, doi, arxiv | partial |
| `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml` | LVK GWTC-4.0 TGR III (Tests of the Remnants), Table 3 (arXiv:2603.19021); local minimal version | 1 (GW190910_112807 only) | yes but renamed (`f220_hz`, `f220_hz_minus/plus`) | yes (`redshifted_Mf_Msun`, `chi_f`) | redshift implied via redshifted mass; explicit `z` not present in this minimal YAML | yes (220 only) | high but minimal; only one event | partial |
| `/home/ignac/ringest_fase_3/data/phase1_data/qnm_events_capano2023.yml` | mirror of above | 1 | identical | identical | identical | identical | identical | partial (mirror) |
| `/home/ignac/ringest_fase_3/data/phase1_data/qnm_events_gwtc4_remnants_table3.yml` | mirror of above | 1 | identical | identical | identical | identical | identical | partial (mirror) |
| `/home/ignac/RINGEST/runs_sync/active/gwtc4_pseobnr_ingest/qnm_events_gwtc4_pseobnr.yml` | LVK GWTC-4.0 TGR III, Table 3 pSEOBNR (full ingest) | 17 | yes (`f_hz`, `sigma_f_hz`, plus asymmetric CI legs) | yes (`M_final_Msun`, `chi_final`, sigmas) | yes (`z`) | yes (`l`, `m`, `n`, `mode = 220` per modes entry) | high; metadata documents `source_paper`, `source_table`, `method = pSEOBNR`, sigma convention `max_abs_upper_lower_error_from_gwosc_api_v2_preferred_parameter_run` (same convention as phase1), `mass_frame_note` says YAML stores source-frame `M_final_Msun` from GWOSC PE | yes |
| `/home/ignac/RINGEST/runs_sync/active/gwtc4_pyring_ds_reduction/qnm_events_gwtc4_pyring_ds.yml` | LVK GWTC-4.0 pyRing DS reduction | 0 (`events: []`) | n/a | n/a | n/a | n/a | YAML present but empty | no |

Source labels (concise):

- **Capano 2023** (PRL 131, 221402): single-event reanalysis of GW190521 with agnostic frequency-range extraction, posterior Kerr identification preserved.
- **GWTC-4 Table 3 (minimal, in repo)**: minimal Phase 3 case-study YAML for GW190910_112807 only, derived from LVK GWTC-4.0 TGR III Table 3.
- **GWTC-4 pSEOBNR (RINGEST ingest)**: full ingest of LVK GWTC-4.0 TGR III Table 3 pSEOBNR results, 17 events, schema-compatible with the phase1 literature YAML.
- **GWTC-4 pyRing DS (RINGEST ingest)**: empty YAML at the time of inspection.

## Event overlap

Phase 1 literature 220 events (`data/phase1_data/qnm_events_literature.yml`, n = 19, source = GWTC-2 TGR):

```
GW150914, GW170104, GW170814, GW170823,
GW190408_181802, GW190421_213856, GW190503_185404, GW190512_180714,
GW190513_205428, GW190519_153544, GW190521, GW190521_074359,
GW190602_175927, GW190706_222641, GW190708_232457, GW190727_060333,
GW190828_063405, GW190910_112807, GW190915_235702
```

| source pair | common events | common count | comments |
|---|---|---:|---|
| phase1 literature × Capano 2023 | GW190521 | 1 | Capano covers only GW190521; the Phase 4 220 dataset includes GW190521, but Capano's "range A → 220" identification is posterior, not the same labeled IMR mode. |
| phase1 literature × GWTC-4 Table 3 (minimal) | GW190910_112807 | 1 | Single-event minimal YAML; not enough for a sign test. |
| phase1 literature × GWTC-4 pSEOBNR (RINGEST) | GW150914, GW170104, GW190519_153544, GW190521_074359, GW190828_063405, GW190910_112807 | 6 | Independent pipeline (pSEOBNR), independent paper (GWTC-4 vs GWTC-2). Provides per-event paired comparison for the sign test reproduction. |
| GWTC-4 pSEOBNR (RINGEST) only — new events | GW190630_185205, GW200129_065458, GW200224_222234, GW200311_115853, GW230628_231200, GW230914_111401, GW230927_153832, GW231028_153006, GW231102_071736, GW231206_233901, GW231226_101520 | 11 (not common; new) | Eleven additional events not present in the phase1 dataset. Useful as an independent extension cohort for the sign test under a different pipeline. |

Out of the 16 rows in the current Paper 4 220 dataset (the 19-event phase1 file minus three rows that did not survive into the schema-aligned 220 table), six events are directly comparable in GWTC-4 pSEOBNR. The remaining 10 GWTC-4 pSEOBNR events are not in the current Paper 4 dataset and would form a non-overlapping extension cohort.

## Field gaps

Capano 2023:

- Missing critical for a 220 frequency-residual test: `M_final_Msun`, `sigma_M_final_Msun`, `chi_final`, `sigma_chi_final`, `z`. Without these, `f_kerr_hz` cannot be computed inside the existing producer convention.
- Cannot be derived from the YAML alone. Would require pulling remnant parameters from another source (GWOSC PE, IMR posterior). That introduces a derivation step rather than a clean second-pipeline measurement.
- Frame is explicit and matches the producer convention (`frame: detector`).
- Verdict: not a drop-in second source for the sign test; usable for a single-event GW190521 cross-check on `f_hz` only, with remnant parameters borrowed from another source (which loses pipeline independence).

GWTC-4 Table 3 (minimal, local):

- One event only. Not enough for a population-level test.
- Field names differ (`f220_hz` not `f_hz`, `redshifted_Mf_Msun` not `M_final_Msun`, `chi_f` not `chi_final`); a mapping layer would be needed.
- Mass is detector-frame (`redshifted_Mf_Msun`); the producer convention expects source-frame `M_final_Msun`. Would need source-frame conversion via `z`, but `z` is not present in this YAML.
- Verdict: descriptive provenance only; not feasible by itself.

GWTC-4 pSEOBNR (RINGEST ingest):

- All required fields present: `f_hz`, `sigma_f_hz`, `M_final_Msun`, `chi_final`, `sigma_M_final_Msun`, `sigma_chi_final`, `z`, `mode`/`l`/`m`/`n`, `source_paper`.
- Sigma convention identical to phase1 literature: `max_abs_upper_lower_error_from_gwosc_api_v2_preferred_parameter_run`.
- Mass frame matches phase1 convention: YAML stores source-frame `M_final_Msun` from GWOSC PE; the producer's `M_detector = M_final_Msun*(1+z)` is therefore directly applicable. The metadata note "Table 3 mass is detector-frame (1+z)M_f; YAML uses source-frame M_final_Msun from GWOSC PE" makes this explicit.
- Pipeline is independent (pSEOBNR vs GWTC-2 TGR IMR). Source paper is independent (GWTC-4.0 TGR III vs GWTC-2 TGR).
- Verdict: drop-in second source. The producer schema does not need to change; only the input YAML path would change.

No new physical derivation is required to use the GWTC-4 pSEOBNR YAML for a sign-test reproduction. The other candidates do not pass the field-completeness bar by themselves.

## Feasibility verdict

`multisource_ready`.

Justification: a second, schema-compatible, independently produced QNM/remnant YAML exists in the RINGEST sibling workspace (`/home/ignac/RINGEST/runs_sync/active/gwtc4_pseobnr_ingest/qnm_events_gwtc4_pseobnr.yml`). It has 17 events of which 6 overlap with the current Paper 4 220 dataset and 11 are new. All necessary fields (`f_hz`, `sigma_f_hz`, `M_final_Msun`, `chi_final`, `sigma_M_final_Msun`, `sigma_chi_final`, `z`, `mode`) are present, the sigma convention and mass frame match the phase1 convention, and the pipeline (pSEOBNR) and source paper (GWTC-4 TGR III) are independent of GWTC-2 TGR. Capano 2023 and the local minimal GWTC-4 Table 3 YAML are not feasible by themselves due to single-event scope and field gaps.

## Recommended next step

Single next step: prepare a documentation-only mapping plan that specifies how the phase1 producer (`02c_paper4_literature_to_dataset.py`) can ingest the GWTC-4 pSEOBNR YAML *without* recalculating phase1 outputs and without modifying the existing producer in-place. The deliverable should be `docs/paper4_multisource_mapping_plan.md` enumerating: input YAML path, expected per-event field mapping, sigma convention check, mass-frame convention check, output dataset path under a new `runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/` directory, and the residual sign-test command sequence to be run against that output. No producer modification, no run, no recalculation, and no candidate language is required at this step.
