# Paper 4 — Multi-Source Mapping Plan

## Scope

This document fixes, before any execution, how the active Paper 4 producer will ingest the independent GWTC-4 pSEOBNR YAML to test whether the population-level `residual_f` sign asymmetry from `docs/paper4_frequency_sign_test.md` reproduces under an independent pipeline. It does not run the producer, does not run the sign test, does not copy the YAML, does not modify scripts, data, or any existing outputs. It is a pre-execution mapping plan.

## Source selected

- Exact YAML path: `/home/ignac/RINGEST/runs_sync/active/gwtc4_pseobnr_ingest/qnm_events_gwtc4_pseobnr.yml` (30 KB, 17 events, schema-compatible with phase1 literature).
- Source label: GWTC-4 pSEOBNR.
- Source paper: "GWTC-4.0 Tests of General Relativity III: Tests of the Remnants", arXiv:2603.19021, Table 3, pSEOBNR pipeline.
- Motivation for selection: the only repository-accessible YAML with (a) full per-mode `f_hz`/`sigma_f_hz`/`tau_ms`/`sigma_tau_ms`, (b) per-event `M_final_Msun`/`chi_final` with sigmas, (c) per-event `z`, (d) an explicit independent pipeline (pSEOBNR ≠ GWTC-2 TGR IMR), and (e) an independent source paper (GWTC-4.0 ≠ GWTC-2 TGR). Six events overlap with the current Paper 4 220 dataset; eleven additional events form an extension cohort. See `docs/paper4_multisource_feasibility.md`.

## Producer

- Active producer: `02c_paper4_literature_to_dataset.py`.
- Confirmed signature (`--help`):
  - `--sources SOURCES`: YAML path; `Path` type, accepts absolute paths.
  - `--out OUT`: output directory; `Path` type.
- The producer's existence check (`if not args.sources.exists():`) accepts any absolute path. No copy of the YAML into the repository tree is required and none should be made.
- The producer will not be modified for this run. The only inputs that change relative to the phase1 baseline are `--sources` and `--out`.

## Field mapping

Required fields used by the producer's existing logic (already verified against the GWTC-2 TGR phase1 YAML), and how they appear in the GWTC-4 pSEOBNR YAML:

| required field | GWTC-4 pSEOBNR field | status | comment |
|---|---|---|---|
| event identifier | `event` (per-event) | present | Same key name as in phase1 YAML; producer reads `event` (the descriptive output column `event_id` is downstream). |
| `ifo` | `ifo` | present | String; informational only. |
| `f_hz` (per mode) | `modes[*].f_hz` | present | Median frequency from Table 3 pSEOBNR; pipeline-independent from phase1's IMR `f_hz`. |
| `sigma_f_hz` (per mode) | `modes[*].sigma_f_hz` | present | YAML metadata declares `sigma_*` is `max(abs(+CI), abs(-CI))`; differs from phase1's average-of-asymmetric convention (see Convention check). |
| `tau_ms` (per mode) | `modes[*].tau_ms` | present | Median damping time from Table 3 pSEOBNR. |
| `sigma_tau_ms` (per mode) | `modes[*].sigma_tau_ms` | present | Same `max-abs` convention as `sigma_f_hz`. |
| `M_final_Msun` (per event) | `M_final_Msun` | present | Source-frame remnant mass from GWOSC PE (per `mass_frame_note`). Table 3 pSEOBNR detector-frame mass is preserved separately as `table3_detector_frame_M_final_Msun`. |
| `sigma_M_final_Msun` | `sigma_M_final_Msun` | present | GWOSC PE convention `max_abs_upper_lower_error_from_gwosc_api_v2_preferred_parameter_run`. |
| `chi_final` (per event) | `chi_final` | present | Same GWOSC PE source. Table 3 pSEOBNR `chi_f` is preserved separately as `table3_pseobnr_chi_f`. |
| `sigma_chi_final` | `sigma_chi_final` | present | GWOSC PE max-abs convention. |
| `z` / redshift (per event) | `z` | present | Used by the producer to form `M_detector = M_final_Msun*(1+z)`. |
| `l`, `m`, `n` / `mode` (per mode) | `modes[*].l`, `modes[*].m`, `modes[*].n`, `modes[*].mode` | present | Producer's 220 filter expects `l=2, m=2, n=0`. |
| `source_paper` (per mode) | `modes[*].source_paper` | present | "GWTC-4.0 Tests of General Relativity III: Tests of the Remnants". |
| `pole_source` (per row) | derived in producer | n/a | Producer assigns `pole_source = source_paper` from the mode entry. |

No mapping layer is required. The producer's existing reader handles the GWTC-4 pSEOBNR YAML without modification.

Caveats on independence:

- `f_hz` and `tau_ms` (the observed ringdown values) are fully pipeline-independent: pSEOBNR (GWTC-4 Table 3) versus IMR (GWTC-2 TGR Table IX).
- `M_final_Msun` and `chi_final` come from GWOSC PE in both YAMLs. The phase1 file uses `pe_parameter_run: GWTC-2.1-confident preferred C01:Mixed`; the GWTC-4 pSEOBNR YAML uses `pe_parameter_run: GWTC-1-confident_GW150914_R2_pe_combined` (and equivalent versioned runs per event). The two PE runs differ in catalog version and possibly in waveform family, so the remnant point estimates are not identical, but they share the GWOSC PE provenance. The Kerr prediction `f_kerr_hz` therefore retains some residual correlation with phase1; the observed-side asymmetry channel remains independent.
- The Table 3 pSEOBNR remnant parameters (`table3_pseobnr_chi_f`, `table3_detector_frame_M_final_Msun`) are stored in the YAML but are *not* used by the producer; the producer reads `M_final_Msun` and `chi_final` (GWOSC PE source-frame). This preserves the existing producer convention without ad-hoc changes.

## Convention check

- Sigma convention. Phase 1 literature YAML's metadata: `pe_sigma_convention: max_abs_upper_lower_error_from_gwosc_api_v2_preferred_parameter_run` (effective symmetric PE uncertainty for Kerr propagation). GWTC-4 pSEOBNR YAML metadata: `pe_sigma_convention: max_abs_upper_lower_error_from_gwosc_api_v2_preferred_parameter_run` (identical). For the per-mode `sigma_f_hz` and `sigma_tau_ms`, the GWTC-4 pSEOBNR YAML uses `qnm_ci_convention: Table 3 reports median with 90% credible intervals; sigma_* here is max(abs(+CI), abs(-CI)) for RINGEST ingestion`. Phase 1 used the arithmetic mean of upper/lower asymmetric Table IX errors. This is a *real* convention difference for the observed-side sigmas: phase1 uses `mean(+,−)`, GWTC-4 pSEOBNR uses `max(+,−)`. The mapping plan does not attempt to reconcile this; it is recorded as a known difference in the comparison and re-examined under "Decision gates".
- Mass frame. Both YAMLs store `M_final_Msun` as source-frame from GWOSC PE; the producer multiplies by `(1+z)` to obtain detector-frame `M_detector`. The convention is identical.
- Redshift semantics. Both YAMLs store `z` per event, used identically by the producer.
- Mode convention. Both YAMLs use `l`, `m`, `n` integer keys with `mode` as a string/int label. The producer's 220 filter (`is_220_candidate`) does not change.
- Comparability. Observed `f_hz` and `tau_ms` channels are fully pipeline-independent. The Kerr-side prediction shares the GWOSC PE provenance via `M_final_Msun` and `chi_final`. The sigma convention on `sigma_f_hz`/`sigma_tau_ms` differs (`max` vs `mean`), which mechanically inflates the GWTC-4 pSEOBNR sigmas relative to phase1 and therefore deflates the magnitude of `residual_f` toward zero — a conservative direction for the sign test (it does not artificially inflate sign coherence).

## Planned commands

To be executed only after this plan is approved:

```bash
python3 02c_paper4_literature_to_dataset.py \
  --sources /home/ignac/RINGEST/runs_sync/active/gwtc4_pseobnr_ingest/qnm_events_gwtc4_pseobnr.yml \
  --out runs/paper4_qnm_dataset_gwtc4_pseobnr_v1

python3 tools/paper4_frequency_sign_test.py \
  --input runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset_220.csv \
  --out-dir runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1
```

These are the only commands the plan authorizes. Do not introduce additional flags, do not redirect outputs to alternative paths, and do not chain post-processing.

## Expected outputs

After the producer command:

- `runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset.csv` — full unfiltered dataset.
- `runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset_220.csv` — 220-mode filtered dataset; expected size ≈ 17 rows (one per event, all 220 fundamentals from Table 3).

After the sign-test command:

- `runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/frequency_sign_test_summary.json` — `n_total`, `n_positive`, `n_negative`, `n_zero`, `p_one_sided_positive`, `p_two_sided`.
- `runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/frequency_sign_test_table.csv` — per-event `residual_f` and sign, sorted descending.

## Decision gates

- If the producer fails on the GWTC-4 pSEOBNR YAML for any schema reason, do not adapt the producer in-place. Document the failure in a follow-up note; do not modify `02c_paper4_literature_to_dataset.py` to handle ad-hoc cases.
- If the sign asymmetry is reproduced (e.g., `n_positive ≥ 13/17` and `p_one_sided ≲ 0.05`), proceed to a documented multi-source comparison note (paired comparison on the 6 overlap events, full-population comparison on all 17). The descriptive language remains "population-level sign coherence reproduced under independent pipeline"; no candidate or detection language.
- If the sign asymmetry is not reproduced (e.g., approximately balanced split), interpret as source/pipeline-limited: the phase1 sign asymmetry is consistent with a GWTC-2 TGR IMR pipeline systematic and does not generalize. Document accordingly.
- Under no decision branch is candidate/detection/new-physics language admissible.

## Immediate next step

Single next step: execute exactly the two planned commands listed under "Planned commands", in that order, only if this plan is approved. No producer modification, no additional flag, no output redirection, and no candidate language is to be introduced at execution time.
