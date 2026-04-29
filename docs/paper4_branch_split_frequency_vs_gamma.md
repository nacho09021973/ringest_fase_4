# Paper 4 — Frequency/Gamma Branch Split

## Scope

This document formalizes the separation of the Paper 4 220 Kerr audit into two clearly-labeled descriptive branches: a frequency-only Kerr audit and a gamma-dominated/systematics-limited audit. It does not modify scripts, data, YAML, configs, or residuals. It does not produce any new numerical result, recalculate Kerr predictions, change thresholds, or declare candidates. It is a documentation-only governance step that fixes which language is allowed in each branch and which next analyses are permitted.

## Reason for split

- The detector/source-frame question for `tau_ms` was resolved as detector-frame in `docs/paper4_tau_source_frame_source_check.md`, against direct evidence from Table IX and Eq. (7) of the source paper.
- The producer `02c_paper4_literature_to_dataset.py` is therefore frame-consistent: `damping_hz = 1000.0/tau_ms` and `gamma_kerr_hz = -omega_im/(M_detector·G/c³)` are both detector-frame, so `residual_gamma` is no longer blocked by the frame channel.
- Despite frame-consistency, `docs/paper4_gamma_systematics_remaining_audit.md` showed that `residual_gamma` remains systematics-limited. The combined budget of asymmetric-error symmetrization in Table IX, posterior median-mapping non-commutativity in the damping channel, and the LVK-acknowledged weaker constraint on damping time absorbs residuals at the 1.0–1.7σ scale observed in the top rows, leaving no defensible physical Kerr-deviation interpretation on the gamma side.
- The frequency channel is materially less affected by this systematic stack. In the top 8 descriptive residual rows, 6/8 are gamma-dominated and the remaining 2 have frequency and gamma comparable; the frequency residuals are consistently smaller and better-behaved.
- A formal split makes the difference operational: frequency residuals can be examined as a descriptive Kerr audit on their own merits, while gamma residuals are kept as a systematics-limited side-record that must not be used as a candidate criterion.

## Branch A — Frequency-only Kerr audit

- Input: `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv` (schema-aligned), and the existing descriptive table `runs/paper4_residual_audit_v1/paper4_220_residuals_descriptive.csv`.
- Principal observable: `f_hz` vs `f_kerr_hz`.
- Metric: existing `residual_f = (f_hz − f_kerr_hz) / sqrt(sigma_f_hz² + sigma_f_kerr_hz²)`. No recalculation of `f_kerr_hz` or of any sigma is performed in this branch.
- Objective: descriptive ranking of events by `|residual_f|`, used to identify which events show the largest frequency-side deviations from the Kerr point estimate, independent of damping.
- Allowed language: "frequency-only outlier", "frequency residual", "descriptive frequency tension", "frequency channel", "f-channel ranking".
- Forbidden language: "candidate", "detection", "new physics", "Kerr violation", "evidence" — none of these are permissible in Branch A under the current Paper 4 candidate criteria.

## Branch B — Gamma-dominated / systematics-limited audit

- Input: `tau_ms`, `sigma_tau_ms`, `gamma_kerr_hz`, `sigma_gamma_kerr_hz`, `residual_gamma` from the same descriptive table.
- Status: frame-consistent but systematics-limited. The dominant systematic channels are asymmetric-error symmetrization of Table IX intervals, posterior median-mapping non-commutativity in the damping channel, and the source-paper damping-time caveats summarized in `docs/paper4_gamma_systematics_remaining_audit.md`.
- Objective: keep a descriptive record of `residual_gamma` and document failure modes per row. The gamma channel is explicitly excluded from candidate criteria; it is reported as a methodological/systematics result, not as physical evidence.
- Allowed language: "gamma-systematics-limited", "damping-dominated", "needs source-level check", "gamma channel descriptive".
- Forbidden language: "Kerr violation", "physical tension", "candidate", "detection", "new physics" — none of these are permissible in Branch B.

## Decision rules

- No event may be declared a candidate using `residual_gamma` until the damping-side systematics (asymmetric-error symmetrization, posterior median-mapping, low-SNR damping caveats) are individually resolved at the source level.
- Events with high `|residual_f|` may proceed to a frequency-only descriptive review under Branch A. They do not become candidates by virtue of that review; they only become eligible for further per-event input/systematic audits.
- Events whose largest residual is on the gamma channel are classified `not_candidate_yet` and remain in Branch B.
- Any final descriptive statement, in either branch, must report `N` and the `source_paper`. The single-source provenance constraint inherited from the candidate criteria is unchanged.
- A row may appear in both branches simultaneously (e.g., a row with both high `residual_f` and high `residual_gamma`); the branch label governs only which channel is being interpreted, not which rows are visible.

## Allowed next analyses

Only the following descriptive next analyses are permitted under this split:

1. Build a frequency-only descriptive table from the existing dataset, ordered by `|residual_f|` descending, without recalculating `f_kerr_hz` or any sigma.
2. Document the top frequency-side residuals descriptively, with the same conservative language used in `docs/paper4_220_residuals_descriptive_audit.md`.
3. Compare whether the top frequency rows coincide with the top gamma rows, and report the agreement or disagreement as a descriptive observation only.

No new producer run, no recalculation, no candidate language, and no Stage 02/03/04 execution is permitted under this split.

## Immediate next step

Single next step: create `docs/paper4_frequency_only_residual_audit.md` using the existing descriptive table, ordering rows by `|residual_f|` and documenting the top frequency-side residuals without recalculating Kerr predictions and without declaring candidates.
