# Paper 4 — Methodological Synthesis

## Scope

This synthesis integrates the Paper 4 results already documented in the frequency/gamma audits and the multi-source sign-coherence notes. It does not generate new results, rerun scripts, modify data, change thresholds, decide publication, or decide whether Fase 4 should be deposited.

The purpose is to state what Fase 4 can defensibly claim after the frequency/gamma split and the multi-source comparison, and what remains blocked by systematic uncertainty.

## Main result

Paper 4 does not identify robust individual beyond-Kerr candidates. It identifies a population-level positive sign asymmetry in frequency residuals that persists across two sources/pipelines, while the damping channel is systematics-limited.

The defensible result is therefore methodological and statistical: the frequency residual signs show coherent positive structure across the GWTC-2 TGR IMR phase1 dataset and the GWTC-4 pSEOBNR comparison dataset, but this structure is not yet interpretable as a physical deviation from Kerr.

## Evidence chain

| result component | document | key number/result | interpretation | limitation |
|---|---|---|---|---|
| Frequency-only no individual outliers | `docs/paper4_frequency_only_residual_audit.md` | 0 rows with `|residual_f| >= 2`; maximum `|residual_f| ~= 1.010` in phase1 | No robust individual frequency-side outlier is present under the current standardized residual protocol. | `N = 16`, single GWTC-2 TGR IMR source; absence of outliers does not explain the population sign pattern. |
| Gamma systematics-limited | `docs/paper4_gamma_systematics_remaining_audit.md` | `tau_ms` is detector-frame and code is frame-consistent; gamma residuals remain limited by damping-time constraints, asymmetric-error symmetrization, and median-mapping | The frame objection is closed, but the damping channel cannot support candidate claims. | The dominant residuals are at a scale that can plausibly be absorbed by damping-side systematic budget. |
| Phase1 frequency sign asymmetry | `docs/paper4_frequency_sign_test.md` | 14/16 `residual_f > 0`; `p_one_sided_positive ~= 0.00209` | The phase1 frequency residuals show a statistically non-trivial positive sign asymmetry. | Single-source and single-pipeline result; not evidence for beyond-Kerr physics. |
| Sign-systematics audit | `docs/paper4_frequency_sign_systematics.md` | No obvious explanation from `z`, `M_final`, `chi_final`, or frequency scale; `chi_final` association is moderate and fragile; `sigma_freq_hz` association is mechanical | No trivial single-variable explanation was found, and the result is source-limited. | Small `N`; only 2 negative signs; all rows share the same source and pole provenance. |
| GWTC-4 pSEOBNR sign asymmetry | `docs/paper4_multisource_sign_test_result.md` | 9/9 `residual_f > 0`; `p_one_sided_positive ~= 0.00195` | The positive sign coherence reproduces in an observationally independent pSEOBNR source with a more conservative sigma convention. | Independence is partial because Kerr-side remnant metadata still shares GWOSC PE provenance. |
| Paired common-event persistence | `docs/paper4_multisource_paired_comparison.md` | 5/5 common events preserve positive sign; `median_delta_residual_f ~= -0.132`; `median_delta_f_hz ~= +5.30 Hz` | The sign does not flip for common events even when the observed-side frequency estimate changes across pipelines. | `n_common = 5`; no paired p-value is computed because of small `N` and partial dependence. |

## What is allowed to claim

- No robust individual frequency-only candidates are present under the current protocol.
- Damping/gamma residuals are not suitable for candidate claims under the current protocol.
- Frequency residuals show positive sign coherence in the GWTC-2 TGR IMR phase1 dataset.
- The sign coherence reproduces in the GWTC-4 pSEOBNR dataset.
- Common events preserve the positive sign across pipelines.
- This is a methodological/statistical observation requiring systematic interpretation.

## What is not allowed to claim

- No detection.
- No evidence for beyond-Kerr physics.
- No Kerr violation.
- No candidate catalog.
- No claim of an independent astrophysical population effect.
- No claim that residuals are independent draws without caveats.

## Interpretation

Several explanations remain possible, and the current documentation does not choose among them:

1. Remnant median / nonlinear mapping systematic: `omega_re(median(M_f, chi_f))` need not equal the posterior median of the Kerr frequency after nonlinear transformation, and a coherent offset could appear even for Kerr-consistent signals.
2. Selection/publication effect: both source papers report ringdown estimates only for selected events, so the analyzed population is not an unbiased catalog draw.
3. Waveform-model or pipeline-dependent offset: IMR and pSEOBNR are distinct observed-side pipelines, but pipeline conventions can still create coherent standardized residual structure.
4. Shared GWOSC remnant provenance: the observed-side `f_hz` differs across sources, but the Kerr-side prediction still relies on GWOSC remnant medians and related PE provenance.
5. Genuine population-level discrepancy: this remains a logical possibility, but it is not claimed by Paper 4 under the current protocol.

## Why the result is still interesting

Individual frequency residuals are small, with no row reaching 2 sigma, but the sign is coherent across events. The same positive sign pattern survives the more conservative sigma convention in the GWTC-4 pSEOBNR source, where all 9 retained 220 rows are positive. In the 5 paired common events, the sign does not flip across pipelines even though residual magnitudes and observed frequencies shift.

This combination motivates targeted systematic audits rather than candidate claims. The result is useful because it identifies a precise failure mode to investigate: small per-event residuals that are not individually anomalous but align in sign across partially independent sources.

## Remaining gates before any publication/deposit

- Remnant median mapping audit.
- Selection effects audit.
- Check additional sources if available.
- Freeze a versioned final table or permanent artifact.
- Decide whether Fase 4 merits Zenodo as a methodological result.

## Preliminary decision

`methodological_result_ready_for_writeup` + `needs_one_more_systematics_gate`.

The result is ready to be written up as a methodological observation, but not as a physical claim. One more systematic gate is needed before any publication/deposit decision: the remnant median mapping channel is the most dangerous remaining interpretation risk because it can create sign-coherent offsets through a shared nonlinear transformation.

## Immediate next step

Audit remnant median mapping before writeup.

This is the conservative next step because it directly targets the most plausible systematic capable of producing a coherent positive frequency-residual sign without requiring individual outliers.
