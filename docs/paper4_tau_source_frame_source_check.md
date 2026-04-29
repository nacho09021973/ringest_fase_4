# Paper 4 — Tau Source Frame Source Check

## Scope

This note verifies the reporting frame of `tau_ms` in the original source paper used by `data/phase1_data/qnm_events_literature.yml`. It does not modify scripts, data, YAML, configs, README, or residuals. It does not recalculate Kerr predictions, change thresholds, or declare any candidate. It is a documentation-only check that resolves the open question left by `docs/paper4_detector_source_frame_decision.md` (`unresolved_needs_source_check`).

## YAML provenance

All 19 events in `data/phase1_data/qnm_events_literature.yml` cite the same `source_paper`. The relevant fields and their observed values are:

| field | observed value(s) | comment |
|---|---|---|
| `source_paper` | "Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog" (single, identical string for all 19 events) | Single-source provenance. Resolves to Abbott et al., Phys. Rev. D 103, 122002 (2021), arXiv:2010.14529. |
| `pole_source` | not present as an explicit YAML field at the event/mode level | The Phase 4 audits use this term informally; the YAML's effective per-row source is `source_paper`. |
| `tau_ms` | numeric per mode, e.g. GW150914 `tau_ms = 4.2`, GW190521 `tau_ms = 15.8` | Matches Table IX IMR median values in the source paper. |
| `sigma_tau_ms` | numeric per mode, e.g. GW150914 `0.25`, GW190521 `3.2` | Consistent with symmetrization of the asymmetric Table IX intervals (average of upper and lower 90% credible bounds). |
| `z` (event-level redshift) | numeric per event, e.g. GW150914 `0.090`, GW190521 `0.825` | Used by the producer to form `M_detector = M_final_Msun*(1+z)`. |
| `f_hz` | numeric per mode, e.g. GW150914 `248.0`, GW190521 `68.0` | Matches Table IX IMR median values. |
| `sigma_f_hz` | numeric per mode | Consistent with symmetrization of the asymmetric Table IX intervals. |

## Source availability

The original source paper is available locally:

- `/home/ignac/ringest_fase_3/docs/2010.14529v3.pdf` (39 pages).

There is also an internal Phase 3 reading note for the same paper:

- `/home/ignac/ringest_fase_3/docs/paper3_source_A_prime_LVK_TGR_2021_reading.md`,
- mirrored in this repository at `docs/paper3_source_A_prime_LVK_TGR_2021_reading.md`.

Both were consulted for this audit. The PDF is the primary evidence; the reading note is a corroborating internal record.

## Evidence found

Direct evidence from `2010.14529v3.pdf`:

- Section VII.A "Ringdown", Eq. (7), p. 17, defines the observed waveform during ringdown explicitly with redshift factors:
  `h+(t) − i h×(t) = Σ Aℓmn · exp[−(t − t0) / ((1 + z) τℓmn)] · exp[−2π i fℓmn (t − t0) / (1 + z)] · −2Sℓmn(θ, ϕ, χf)`.
  In this expression, `τℓmn` and `fℓmn` are the source-frame (Kerr) damping time and frequency, and the `(1 + z)` factors transform them into the observed (detector-frame) decay time `(1 + z)·τℓmn` and observed frequency `fℓmn / (1 + z)`.
- Table VIII, p. 19, has the column header "Redshifted final mass `(1+z) Mf` [M⊙]". This fixes the LVK convention: "redshifted" = `(1+z)`-multiplied mass = detector-frame mass.
- Table IX, p. 20, caption: "The median value and symmetric 90% credible interval of the **redshifted frequency** and **damping time** estimated using the full IMR analysis (IMR), the pyRing analysis with a single damped sinusoid (DS), and the pSEOBNRv4HM analysis (pSEOB)."
- Section VII.A.2, p. 21, additionally states: "Table IX shows the redshifted effective frequency `f220` and the redshifted effective damping time `τ220` of the 220 mode inferred from this analysis."

Combining these, "redshifted damping time" in Table IX denotes `(1 + z)·τ_source`, i.e., the detector-frame observed damping time.

Cross-check with the YAML (IMR column of Table IX, source paper):

| event_id | YAML `f_hz` (sigma) | Table IX IMR `f` | YAML `tau_ms` (sigma) | Table IX IMR `τ` |
|---|---:|---:|---:|---:|
| GW150914 | 248.0 (7.5) | 248 +8/−7 | 4.2 (0.25) | 4.2 +0.3/−0.2 |
| GW170104 | 287.0 (20.0) | 287 +15/−25 | 3.5 (0.35) | 3.5 +0.4/−0.3 |
| GW170814 | 293.0 (12.5) | 293 +11/−14 | 3.7 (0.25) | 3.7 +0.3/−0.2 |
| GW190521 | 68.0 (4.0) | 68 +4/−4 | 15.8 (3.2) | 15.8 +3.9/−2.5 |
| GW190708_232457 | 497.0 (28.0) | 497 +10/−46 | 2.1 (0.15) | 2.1 +0.2/−0.1 |

The YAML reproduces the Table IX IMR median values exactly, and the YAML `sigma_*` is consistent with the symmetrized average of the asymmetric upper and lower 90% bounds in Table IX.

This is direct evidence (not inference): `tau_ms` in the YAML is the redshifted (detector-frame) damping time as reported in Table IX of the source paper.

A consistent corroboration is `M_final_Msun`. For GW150914, the YAML stores `M_final_Msun = 63.1` and `z = 0.090`, so `(1+z)·M_final_Msun = 68.78`, matching the IMR "Redshifted final mass" column of Table VIII (`68.8 +3.6/−3.1`). The YAML's `M_final_Msun` is therefore source-frame, and the producer's `M_detector = M_final_Msun*(1+z)` is the correct detector-frame reconstruction.

## Decision status

`tau_detector_frame_confirmed`

Justification: the source paper's Table IX, which is the direct origin of the YAML `tau_ms` and `f_hz` values, is explicitly described in the paper as containing the redshifted damping time and redshifted frequency, and Eq. (7) of the same paper fixes "redshifted" to mean the `(1+z)`-transformed detector-frame observable.

## Consequence

Direct consequences for Paper 4:

- The current `02c_paper4_literature_to_dataset.py` comparison is frame-consistent. Observed damping is `damping_hz = 1000.0 / tau_ms` with detector-frame `tau_ms`, so `damping_hz` is detector-frame. Kerr damping is `gamma_kerr_hz = −omega_im / (M_detector·G/c³)` with `M_detector = M_final_Msun·(1+z)`, which is the detector-frame Kerr damping rate. The two sides of `residual_gamma` are in the same frame.
- `residual_gamma` may continue to be audited at the residual level (descriptive, ranking, systematics) without a code change, YAML change, or recalculation triggered by frame considerations.
- The earlier diagnostic from `docs/paper4_gamma_tau_convention_audit.md` and `docs/paper4_detector_source_frame_decision.md` — that `gamma_current / (1+z)` lies closer to `gamma_kerr_hz` for several top rows — is no longer interpretable as evidence of a frame mismatch. Both observed and Kerr damping are confirmed detector-frame; the apparent numerical proximity after dividing by `(1+z)` is a coincidence at the small redshifts of the top-residual rows, not a physical correction.
- The previous block on Paper 4 candidate language, however, is not lifted by this finding alone. The top-residual rows are still not declared candidates: their large `residual_gamma` values must now be explained by other systematics (Kerr table interpolation, sigma symmetrization, asymmetric error handling, or the LVK-acknowledged damping-time overestimation effects in low-SNR ringdown analyses, see source paper p. 20–21) before any tension language is defensible. The frame channel is closed; the systematics channel remains open.

## Immediate next step

Frame question is resolved as detector-frame; no patch and no code change are required for the frame convention. The single next step is to audit the remaining systematics on `residual_gamma` (Kerr-side interpolation, sigma symmetrization from asymmetric Table IX errors, low-SNR ringdown overestimation acknowledged in the source paper), without producing any candidate language. No bridge run, Stage 02/03/04 execution, or residual recalculation is required for this step.
