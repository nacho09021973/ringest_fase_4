# Paper 4 — Missing Candidate Fields

## Scope

This document records the fields still missing or non-canonical in the initial Paper 4 QNM dataset. It does not patch the producer, does not modify source data, does not identify candidates, and does not change any physical threshold or residual definition.

## Current status

- dataset status: partially Kerr-ready
- run-dir: `runs/paper4_initial_qnm_dataset`
- producer: `02b_literature_to_dataset.py`

The current CSVs already contain observed QNM frequency/damping fields, final-mass/final-spin metadata, redshift, Kerr predictions, and residual columns. The blocker for a traceable candidate audit is not the absence of all Kerr ingredients; it is the absence of canonical candidate-audit identifiers and provenance fields.

## Missing / non-canonical fields

| field required by criteria | current status | found in YAML? | found in CSV under another name? | can be derived without new physics? | required action |
|---|---|---|---|---|---|
| `event_id` | Absent as a canonical column. | No exact `event_id`; YAML has `event` for 19/19 mode rows. | Yes: CSV has `event` for all rows. | Yes. Rename or duplicate `event` as `event_id`. | Materialize `event_id = event` or document the mapping. |
| explicit mode label / `l,m,n` / `220` | Absent as explicit columns or a single canonical mode label. | Yes: YAML has `l`, `m`, and `n` for 19/19 mode rows. | Partially: CSV has `mode_rank` and `is_220_candidate`; `qnm_dataset_220.csv` is a filtered 220-like subset. | Yes, if copied from YAML or emitted from already-read producer variables. A `220` label can be constructed from `l=2,m=2,n=0`; it should not be guessed from rank alone. | Emit `l`, `m`, `n`, and optionally `mode=220` when those source values are present. |
| `sigma_tau_ms` | Absent from CSV. | Yes: YAML has `sigma_tau_ms` for 19/19 mode rows. | Partially: CSV has `tau_ms` and propagated `sigma_damping_hz`. | Yes. Prefer copying from YAML. Algebraic recovery is possible only under the producer's existing propagation convention, not as a new physical assumption. | Emit source `sigma_tau_ms`; do not fabricate it when missing. |
| `source_paper` | Absent as a literal canonical column. | Yes: YAML has `source_paper` for 19/19 mode rows. | Yes: CSV has `pole_source` for all rows, populated from YAML `source_paper`. | Yes. Rename or duplicate `pole_source` as `source_paper`. | Materialize `source_paper = pole_source` or preserve both names. |

## Field-by-field decision

### `event_id`

`event_id` does not require a physical decision. The source YAML and current CSV use `event`, which is complete and already carries the event identifier. For candidate-audit compatibility, this is a canonical naming issue: either rename `event` to `event_id` in a Paper 4-facing output or duplicate it while retaining `event` for backward compatibility.

Decision: enough to rename or duplicate. Do not fabricate a new identifier scheme.

### Explicit mode label / `l,m,n` / `220`

The YAML contains explicit `l`, `m`, and `n` fields for each mode row, and the producer already reads those values internally before writing only `mode_rank` and `is_220_candidate`. The 220 subset and `is_220_candidate` flag are useful filters, but they are not a full modal provenance record. `mode_rank=0` should not be treated as a standalone substitute for an explicit `(l,m,n)` label.

Decision: copy `l`, `m`, and `n` from YAML into the output. A `mode` string such as `220` can be derived mechanically from those copied fields when `l=2`, `m=2`, and `n=0`. This is metadata normalization, not new physics.

### `sigma_tau_ms`

The YAML contains `sigma_tau_ms` for every current mode row. The current CSV omits it and instead exposes `sigma_damping_hz`, which the producer computes from `sigma_tau_ms` and `tau_ms`. Because the source uncertainty exists, the safest remediation is to emit the source value directly.

If a future source lacks `sigma_tau_ms`, it should not be invented. Recovering it from `sigma_damping_hz` and `tau_ms` is only a convention-preserving algebraic inverse of the producer's current propagation, and should be marked as derived if used.

Decision: copy from YAML when present; otherwise leave missing or explicitly mark a derived value and its convention.

### `source_paper`

The YAML contains `source_paper` for every mode row. The producer reads that key and writes it to the CSV under `pole_source`. This is a naming/provenance compatibility issue, not a physical one.

Decision: enough to duplicate or rename `pole_source` as `source_paper`. Preserve the original provenance text exactly.

## Minimal remediation options

A. Document-only mapping.

Record that `event -> event_id`, `pole_source -> source_paper`, `freq_hz -> f_hz`, `sigma_freq_hz -> sigma_f_hz`, `damping_hz -> gamma_hz`, `sigma_damping_hz -> sigma_gamma_hz`, and `z -> redshift` are accepted aliases for the current audit. This avoids code changes but leaves downstream candidate tables dependent on manual mapping.

B. Minimal patch to `02b_literature_to_dataset.py`.

Add canonical metadata columns while preserving existing columns and values: `event_id`, `l`, `m`, `n`, `mode`, `sigma_tau_ms`, and `source_paper`. This would materialize fields the producer already reads from YAML, without changing frequencies, damping rates, Kerr predictions, residuals, thresholds, or row selection.

C. Create a renamed Paper 4 producer if compatibility would break.

If adding columns to the historical producer is considered too broad for existing downstream scripts, create a Paper 4-specific producer or export mode that emits a candidate-audit schema while leaving the legacy output untouched.

## Recommended next step

Patch the producer minimally to materialize canonical candidate-audit fields without changing the physical values.
