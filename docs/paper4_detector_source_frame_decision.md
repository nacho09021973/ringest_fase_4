# Paper 4 — Detector/Source Frame Decision

## Scope

This document narrows the detector/source-frame convention for the Paper 4 220 damping residuals. It does not modify the pipeline, does not change residuals, does not change the producer, and does not classify any event.

## Motivation

`docs/paper4_gamma_tau_convention_audit.md` found that the large damping residuals are not explained by a simple `2*pi` factor. It also found that comparing `gamma_current/(1+z)` with `gamma_kerr_hz` moves several of the largest-residual rows much closer to the Kerr damping rate. The remaining question is whether the YAML `tau_ms` values are source-frame or detector-frame quantities, and whether `gamma_kerr_hz` is being compared in the same frame.

## Code frame convention

`02c_paper4_literature_to_dataset.py` applies redshift to Kerr predictions through detector-frame mass:

- `M_detector = M_final_Msun * (1 + z)`.
- `scale_detector = M_detector * G/c^3`.
- `f_kerr_hz = omega_re_kerr / (2*pi*scale_detector)`.
- `gamma_kerr_hz = -omega_im_kerr / scale_detector`.

The code comments state that this places `f_kerr_hz` in the detector frame to match `f_hz` from the literature. The same `scale_detector` is used for `gamma_kerr_hz`, so Kerr damping is also emitted in detector-frame units.

For observed damping, the code currently does:

- `damping_hz = 1000.0 / tau_ms`.
- `sigma_damping_hz = 1000.0 * sigma_tau_ms / tau_ms**2`.

No `(1+z)` transformation is applied to observed `tau_ms` or `damping_hz`. Therefore the frame consistency depends entirely on whether the YAML `tau_ms` is already detector-frame. If `tau_ms` is source-frame, the current comparison mixes source-frame observed gamma with detector-frame Kerr gamma. If `tau_ms` is detector-frame, the current comparison is frame-consistent.

## Source frame evidence

`data/phase1_data/qnm_events_literature.yml` provides, per mode:

- `f_hz`;
- `sigma_f_hz`;
- `tau_ms`;
- `sigma_tau_ms`;
- `source_paper`.

It also provides event-level `z`. It does not provide explicit fields such as `tau_frame`, `frequency_frame`, `gamma_frame`, `detector_frame`, or `source_frame`. The YAML source provenance for the top rows is the GWTC-2 tests-of-GR source paper, but the local YAML itself does not state whether `tau_ms` is reported in the detector frame or source frame.

Thus the local evidence is insufficient to decide the source convention from the repository alone.

## Diagnostic comparison

These values are diagnostic only and do not replace the existing residuals.

| event_id | z | gamma_current | gamma_current/(1+z) | gamma_kerr_hz | residual_gamma | brief comment |
|---|---:|---:|---:|---:|---:|---|
| GW150914 | 0.090 | 238.095 | 218.436 | 203.471 | 1.683 | Source-frame adjustment moves toward Kerr but does not fully align. |
| GW190708_232457 | 0.197 | 476.190 | 397.820 | 391.898 | 1.569 | Source-frame adjustment nearly matches detector-frame Kerr. |
| GW170814 | 0.124 | 270.270 | 240.454 | 226.359 | 1.515 | Source-frame adjustment moves toward Kerr but remains offset. |
| GW190521_074359 | 0.210 | 185.185 | 153.046 | 155.824 | 1.324 | Source-frame adjustment nearly matches detector-frame Kerr. |
| GW170104 | 0.200 | 285.714 | 238.095 | 244.901 | 1.015 | Source-frame adjustment moves close to detector-frame Kerr. |

## Decision

Decision: `unresolved_needs_source_check`.

The code clearly emits Kerr frequency and damping in detector-frame units. The YAML clearly stores redshift and `tau_ms`, but it does not declare the frame of `tau_ms`. The diagnostic pattern is compatible with a possible source/detector-frame mismatch: if `tau_ms` is source-frame, then the observed damping rate should be divided by `(1+z)` before comparison with detector-frame `gamma_kerr_hz`. However, this cannot be treated as confirmed without checking the original source table/protocol.

## Consequence for Paper 4

Paper 4 should not classify the large damping residual rows until the frame convention is resolved. The current repository evidence supports a focused source-protocol audit, not a code change or event classification. If the original source confirms source-frame `tau_ms`, then the producer should be patched and the residual audit regenerated. If the source confirms detector-frame `tau_ms`, then the current comparison is frame-consistent and the workflow can move to preliminary input-dominated / not-explained-by-obvious-systematics classification.

## Immediate next step

Check the original GWTC-2 tests-of-GR table/protocol for whether the reported `tau_ms` values are source-frame or detector-frame.
