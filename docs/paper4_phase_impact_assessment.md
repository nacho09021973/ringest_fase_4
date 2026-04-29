# Paper 4 — Phase Impact Assessment

## Scope

This note evaluates the impact of the possible detector/source-frame mismatch in `gamma`/`tau_ms` on RINGEST as a whole. It does not change scripts, data, YAML, configs, or residuals. It does not classify any event. It is a documentation-only mapping from the unresolved frame question onto each phase of the project.

## Trigger

`docs/paper4_detector_source_frame_decision.md` reaches the verdict `unresolved_needs_source_check`:

- Kerr predictions `f_kerr_hz` and `gamma_kerr_hz` are emitted by `02c_paper4_literature_to_dataset.py` in the detector frame using `M_detector = M_final_Msun * (1 + z)`.
- Observed damping is computed directly as `damping_hz = 1000.0 / tau_ms`, with no `(1+z)` transformation applied to `tau_ms`.
- `data/phase1_data/qnm_events_literature.yml` does not declare whether `tau_ms` is reported in the detector frame or in the source frame.
- For the largest descriptive 220 residual rows, `gamma_current/(1+z)` lies much closer to `gamma_kerr_hz` than `gamma_current` does, which is consistent with — but does not confirm — a source/detector-frame mismatch on the observed-damping side.

Direct consequences for the current Paper 4 audit branch:

- `residual_gamma` is currently blocked: it cannot be interpreted as a physical Kerr tension until the YAML `tau_ms` frame is confirmed against the original source.
- `residual_f` is not automatically affected by this specific issue, because the diagnostic targets the damping side; frequency-side consistency depends on its own audits.
- No Paper 4 candidate is being declared. The candidate criteria in `docs/paper4_candidate_criteria.md` require unambiguous units and conventions, which are not currently met for the damping side.

## Impact by phase

| phase | dependency on tau/gamma residuals | impact | action required |
|---|---|---|---|
| Phase 1 | Phase 1 ingests literature QNM observables (`f_hz`, `tau_ms`, `sigma_*`, `z`, `source_paper`) without computing Kerr residuals or making physical Kerr-tension claims. | `no_known_impact` | None. Phase 1 deposits already published on Zenodo are not invalidated by an unresolved frame convention in a downstream Kerr comparison. |
| Phase 2 | Phase 2 establishes provenance and schema for QNM literature inputs; it does not produce gamma-based physical claims. | `no_known_impact` | None. The frame question lives in the comparison layer, not in Phase 2 ingestion or schema. |
| Phase 3 / reporting heterogeneity | Phase 3 / Paper 3 documents reporting heterogeneity across sources and pipelines, not a Kerr-tension claim built on `residual_gamma`. | `strengthens_reporting_heterogeneity` | None against existing Phase 3 deposits. The unresolved frame convention for `tau_ms` is itself an additional reporting-heterogeneity datapoint and, if anything, reinforces Phase 3's framing rather than weakening it. |
| Phase 4 / current Kerr audit | Phase 4 currently exposes `residual_gamma` and considers descriptive top rows; Kerr-tension language depends on damping-side comparability. | `blocks_gamma_based_claims` + `source_check_required` | `no_action_pending_source_check` on residual recalculation, code change, or candidate classification. The required action is documentary: verify the `tau_ms` frame convention in the original source before any further Kerr-side step. |

## Current interpretation

- There is no indication that this issue invalidates previously deposited Zenodo artifacts for Phase 1, Phase 2 or Phase 3. Those deposits do not rest on `residual_gamma` as a physical Kerr-tension claim.
- It does block any strong claim that is built on `residual_gamma` in its current form. Damping-side residuals cannot be lifted from descriptive ranking to physical tension without the frame convention being resolved.
- Paper 3 is at minimum not weakened by this finding. Because Paper 3 is centered on reporting heterogeneity, an unresolved YAML-vs-source-paper frame convention for `tau_ms` is consistent with — and arguably reinforces — its framing.
- Phase 4 must keep `residual_f` and `residual_gamma` separated until the frame question is resolved. Frequency-side consistency is governed by its own conventions and is not automatically discredited by the damping-side ambiguity, but it also cannot be used to rescue damping-side claims.

## Claims currently allowed

- It is allowed to say that the 220 dataset has descriptively large `residual_gamma` values for several top rows.
- It is allowed to say that there is a possible detector/source-frame ambiguity affecting how `tau_ms` enters the Kerr comparison.
- It is allowed to say that resolving this requires checking the original QNM source for the frame convention of `tau_ms`.
- It is not allowed to say that those descriptive `residual_gamma` values represent a physical Kerr tension. Under the current criteria, that language is blocked.

## Immediate next step

Verify, in the original QNM source paper used as `source_paper` for the top-residual rows (the GWTC-2 tests-of-GR catalog), whether the reported `tau_ms` values are quoted in the detector frame or in the source frame. No code, data, YAML, or residual change is to be made before that verification.
