# Paper 4 — Remaining Gamma Systematics Audit

## Scope

This audit catalogs the remaining systematic channels that prevent interpreting the largest descriptive `residual_gamma` rows as a physical Kerr tension, now that the detector/source-frame question has been resolved as detector-frame in `docs/paper4_tau_source_frame_source_check.md`. It does not modify scripts, data, YAML, configs, or residuals. It does not recalculate Kerr predictions, change thresholds, or declare candidates. It is a documentation-only audit that maps the residual_gamma pattern onto explicitly-named systematic channels.

## Status entering this audit

- `tau_ms` is detector-frame, confirmed against Table IX of arXiv:2010.14529v3 (Abbott et al., PRD 103, 122002).
- The producer `02c_paper4_literature_to_dataset.py` is frame-consistent: `damping_hz = 1000.0/tau_ms` and `gamma_kerr_hz = -omega_im/(M_detector·G/c³)` with `M_detector = M_final_Msun·(1+z)`, both detector-frame.
- `residual_gamma` is no longer blocked by the frame channel.
- No Paper 4 candidate has been declared, and the candidate criteria in `docs/paper4_candidate_criteria.md` still require ruling out remaining systematics before any tension language is permissible.

## Top residual pattern

Top 8 rows of `runs/paper4_residual_audit_v1/paper4_220_residuals_descriptive.csv` (descriptive ranking, not a candidate ranking):

| event_id | z | residual_f | residual_gamma | max_abs_residual | dominant channel | source_paper |
|---|---:|---:|---:|---:|---|---|
| GW150914 | 0.090 | 0.863 | 1.683 | 1.683 | gamma | GWTC-2 TGR |
| GW190708_232457 | 0.197 | 1.010 | 1.569 | 1.569 | both (gamma slightly larger) | GWTC-2 TGR |
| GW170814 | 0.124 | 0.776 | 1.515 | 1.515 | gamma | GWTC-2 TGR |
| GW190521_074359 | 0.210 | 0.645 | 1.324 | 1.324 | gamma | GWTC-2 TGR |
| GW170104 | 0.200 | 0.521 | 1.015 | 1.015 | gamma | GWTC-2 TGR |
| GW190602_175927 | 0.644 | 0.734 | 1.008 | 1.008 | both (comparable) | GWTC-2 TGR |
| GW190910_112807 | 0.290 | 0.418 | 0.855 | 0.855 | gamma | GWTC-2 TGR |
| GW190408_181802 | 0.243 | 0.291 | 0.834 | 0.834 | gamma | GWTC-2 TGR |

In 6 of the top 8 rows the residual is gamma-dominated; in the remaining 2, frequency and gamma residuals are comparable. No row has a frequency-only dominant residual within the top 8.

## Remaining systematic channels

### Kerr interpolation

The producer uses the Kerr l=m=2 n=0 dimensionless eigenfrequencies from Berti 2009 (arXiv:0905.2975, Table VIII), tabulated at chi ∈ {0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.69, 0.80, 0.90, 0.99} — 11 anchor points. Interpolation between anchors is linear in chi (`_interpolate` in the producer).

Limitations:

- The chi grid spacing is 0.10 except for the 0.69 anchor; truncation/interpolation error scales like the second derivative of `omega_re(chi)` and `omega_im(chi)` over a 0.10 window. The first derivative of `omega_im(chi)` is small at moderate chi (e.g. 0.60–0.69 region) but grows rapidly above chi ≈ 0.80, where `omega_im` flattens (longer Kerr damping). Linear interpolation in this regime is mildly biased.
- The numerical chi derivative used to propagate `sigma_chi` into `sigma_gamma_kerr_hz` is computed with `dchi = 1e-3`, which is much smaller than the table spacing. The local slope reduces to the slope between adjacent anchors, so `sigma_gamma_kerr_hz` is effectively a piecewise-linear sensitivity. This is internally consistent with the table representation but does not capture interpolation curvature.

Expected impact on top rows:

- The top-five rows have chi_final ∈ [0.66, 0.72], which falls inside the [0.60, 0.80] interval where `omega_im(chi)` is varying smoothly. The interpolation error is a minor systematic for these rows; it is plausibly a few percent of `gamma_kerr_hz`, not a 1.5σ effect.
- This channel alone does not appear sufficient to explain residual_gamma values around 1.5σ, but it is non-zero and contributes to the denominator/numerator together with other channels.

### Asymmetric-error symmetrization

Table IX in the source paper reports asymmetric 90% credible intervals (e.g., GW190521 IMR damping time `15.8 +3.9/−2.5`). The YAML stores a single `sigma_tau_ms` per mode, and `docs/paper4_tau_source_frame_source_check.md` confirmed this scalar matches the arithmetic mean of upper and lower 90% bounds (e.g., `(3.9+2.5)/2 = 3.2` for GW190521).

Limitations:

- Treating `sigma_tau_ms` as a Gaussian symmetric standard error ignores the underlying asymmetry of the posterior. For events where the upper error is materially larger than the lower (the typical pattern at low SNR), this symmetrization compresses the upper tail and inflates the lower tail.
- The propagation `sigma_damping_hz = 1000·sigma_tau_ms / tau_ms²` is a first-order Gaussian propagation. Asymmetric posteriors in tau translate into still more asymmetric posteriors in `1/tau`, and the symmetric `sigma_damping_hz` does not capture that.
- For top rows the asymmetry ratio `(upper)/(lower)` of the Table IX IMR damping time is approximately 1.5 (GW150914), 1.33 (GW170104), 1.5 (GW170814), 1.56 (GW190521), 2.0 (GW190708_232457). GW190708_232457 is the most asymmetric of the top rows, and is also the second-largest residual_gamma; this is consistent with symmetrization being a contributor.

Expected impact on top rows:

- For asymmetry ratios of 1.3–2.0, replacing the symmetric sigma with the upper-error-only sigma typically reduces `residual_gamma` by a noticeable factor (the denominator grows), but does not by itself drive residuals to zero. It is a real but partial explanation.

### Damping-time estimation caveat

The source paper explicitly documents (p. 20–21) that damping-time estimates are weakly constrained at low ringdown SNR, and that low-SNR ringdown analyses tend to overestimate the damping time relative to a full IMR analysis. The paper notes that the DS (`pyRing` damped sinusoid) and pSEOB columns of Table IX show this overestimation for several events, while the IMR column is the better-controlled estimator.

Implications for this audit:

- The YAML uses the IMR column of Table IX (verified in `docs/paper4_tau_source_frame_source_check.md`). The general LVK overestimation caveat targets the DS/pSEOB columns, not the IMR column directly, so it does not apply at full strength.
- However, the IMR `tau` is derived from a parameter-estimation analysis that assumes GR throughout the inspiral-merger-ringdown waveform. The Kerr `gamma_kerr_hz` in the producer is built from the same (M_f, chi_f) point estimates. The residual_gamma is therefore comparing two quantities that are not independent: any non-zero residual reflects the gap between (i) the median of the IMR-derived posterior on `tau` and (ii) `1/(omega_im(chi_f_median)/M_detector_median)`. For asymmetric (M_f, chi_f) posteriors, these two are not equal in general, and the gap can produce a non-zero apparent residual_gamma even for a perfectly Kerr signal.
- The damping channel is therefore disproportionately affected by posterior shape and median-mapping non-commutativity, more than the frequency channel. The LVK paper's comment that the damping time is the worse-constrained quantity is consistent with our pattern of gamma-dominated top residuals.

For the specific top rows: GW150914, GW170104, GW170814, GW190521_074359, GW170104 are all high-SNR events for which the LVK paper does not flag the IMR damping time as problematic. The "low-SNR overestimation" caveat does not directly explain their residuals; it stands as a general caveat on the damping channel rather than a per-event explanation.

### Frequency vs gamma contrast

In the top 8 rows, `residual_f` is below `residual_gamma` for 6/8 and comparable for 2/8. Across the full 16-row 220 dataset, the frequency channel is consistently better-behaved than the damping channel. The combined evidence — (i) the source paper's own statement that the damping time is the worse-constrained ringdown observable, (ii) the symmetrization of asymmetric Table IX errors, (iii) the median-mapping non-commutativity in the damping channel — implies that the descriptive residual ranking is dominated by damping-side systematics rather than by a physical Kerr deviation.

The frequency channel is therefore a candidate analysis route that is materially less affected by the residual_gamma systematic stack and may, on its own merits, support a more conservative descriptive analysis.

## Preliminary status by event

Conservative labels for the top five rows:

| event_id | preliminary status | comment |
|---|---|---|
| GW150914 | gamma_systematics_dominated_possible; not_explained_by_frame; not_candidate_yet | High-SNR event; LVK does not flag its IMR damping time. Residual is consistent with the joint contribution of asymmetric symmetrization and median-mapping in the damping channel. |
| GW190708_232457 | gamma_systematics_dominated_possible; needs_source_level_check; not_candidate_yet | Most asymmetric Table IX damping interval among the top rows (factor ≈ 2). Symmetrization is a strong candidate explanation; source-level check on the IMR posterior shape would tighten this. |
| GW170814 | gamma_systematics_dominated_possible; not_explained_by_frame; not_candidate_yet | Profile similar to GW150914; same channels apply. |
| GW190521_074359 | gamma_systematics_dominated_possible; not_explained_by_frame; not_candidate_yet | Mid-redshift, gamma-dominated; no specific LVK damping-overestimation flag for this event in the source paper. |
| GW170104 | gamma_systematics_dominated_possible; needs_source_level_check; not_candidate_yet | Lowest top-row residual; broader `sigma_chi_final = 0.08` enlarges Kerr-side propagation; symmetrization plausibly explains the rest. |

None of the top-five rows is promoted to candidate status by this audit.

## Immediate conclusion

What is now allowed:

- `residual_gamma` is interpretable with respect to the detector/source-frame channel; the frame question is closed.
- The descriptive ranking of `residual_gamma` is preserved as a descriptive observation; it is not a physical Kerr-tension claim.
- The frequency channel is materially less affected by the gamma systematic stack and remains a viable basis for a more conservative descriptive analysis.

What remains blocked:

- No top-residual_gamma row may be presented as evidence of a physical deviation from Kerr. The combination of asymmetric-error symmetrization, posterior median-mapping non-commutativity, and the LVK-acknowledged weaker constraint on damping time provides sufficient systematic budget to absorb residuals at the 1.0–1.7σ scale seen in the top rows.
- No candidate language is permissible on the gamma channel under the current criteria.

## Next step

Single next step: split the Paper 4 residual analysis into two clearly-labeled descriptive branches — (i) frequency-only residuals (`residual_f`) and (ii) gamma-dominated / systematics-limited residuals (`residual_gamma`) — and document the split as the operating mode for any subsequent descriptive ranking, without producing candidate language on the gamma branch. No bridge run, Stage 02/03/04 execution, or residual recalculation is required for this step.
