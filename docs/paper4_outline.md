# Paper 4 Outline

## Recommended title

A Reproducible Audit of Frequency-Residual Sign Asymmetry in Published Ringdown QNM Observables

## Thesis

We find no robust individual frequency outliers and no candidate-level Kerr deviations. However, published 220 ringdown observables show a positive population-level frequency-residual sign asymmetry that persists across two source/pipeline choices. The interpretation is methodological and systematic-limited, not beyond-Kerr.

## Abstract skeleton

We audit published 220 ringdown QNM observables using a conservative Kerr residual construction with explicit provenance. No individual event reaches a robust frequency-only outlier threshold, and the damping/gamma channel is not suitable for physical claims because it remains systematic-limited. The frequency channel nevertheless shows a positive residual sign asymmetry in the GWTC-2 TGR IMR source and reproduces under the GWTC-4 pSEOBNR source, with common events preserving the positive sign across pipelines. We interpret this as a reproducible methodological observation and a prompt for systematic-bias audits, not as evidence for a Kerr violation or beyond-Kerr physics. The main remaining limitations are remnant median mapping, availability of posterior samples, waveform/ringdown modeling systematics, source selection, and heterogeneous reporting conventions.

## Introduction / motivation

- State the Paper 4 question conservatively: whether published ringdown QNM observables contain robust, traceable Kerr residual behavior after provenance and systematic checks.
- Motivate separating individual candidate searches from population-level methodological audits.
- Emphasize that the goal is not to claim new physics, but to test whether a reproducible residual pattern survives basic cross-source checks.
- Introduce the key finding: no candidate-level event, but a sign-coherent frequency residual pattern.

## Data sources and provenance

- Phase1 / GWTC-2 TGR IMR 220 dataset: published tabular QNM observables and remnant summaries ingested into the Paper 4 schema.
- GWTC-4 pSEOBNR 220 dataset: independent source/pipeline comparison with partial event overlap.
- Clarify that the analysis uses published scalar summaries, not strain reanalysis and not full posterior propagation.
- Document source-level caveats: shared GWOSC remnant provenance, event selection, sigma conventions, and partial pipeline independence.

## Observable definition

- Define `residual_f` as the standardized difference between observed frequency and Kerr-predicted frequency.
- State that `freq_hz` is the observed frequency field and `f_kerr_hz` is computed from `M_final_Msun`, `chi_final`, and detector-frame scaling.
- State that current residuals include `sigma_freq_hz` and the propagated Kerr-side `sigma_f_kerr_hz` where available.
- Keep frequency and damping/gamma channels separate.

## Frequency-only residual audit

- Report that no frequency-only event reaches `|residual_f| >= 2`.
- Report the maximum phase1 frequency residual scale as approximately `1.01 sigma`.
- State that no individual frequency-only candidate is declared.
- Explain why small individual residuals do not preclude a population-level sign audit.

## Multi-source sign asymmetry

- GWTC-2 TGR IMR: 14/16 `residual_f` values are positive, with `p_one_sided_positive ~= 0.00209`.
- GWTC-4 pSEOBNR: 9/9 `residual_f` values are positive, with `p_one_sided_positive ~= 0.00195`.
- Common events: 5/5 preserve positive sign across source/pipeline comparison.
- State explicitly that these p-values are descriptive within the documented source-dependence caveats and should not be combined into an overstrong population claim.

## Damping/gamma limitations

- State that `tau_ms` frame consistency was checked and the code is frame-consistent.
- Explain that gamma/damping residuals remain systematic-limited by damping-time constraints, asymmetric uncertainty handling, and median-mapping issues.
- Do not use gamma for candidate claims.
- Treat gamma as a systematic cautionary channel, not as a physical result.

## Remnant mapping audit

### Level 1a implemented

- Local propagation of `sigma_M_final_Msun` and `sigma_chi_final` into `sigma_f_kerr_hz` is already implemented in the current datasets.
- `residual_f` already uses the combined denominator with `sigma_freq_hz` and `sigma_f_kerr_hz`.
- Therefore the sign asymmetry is not an artifact of completely ignoring remnant mass/spin uncertainty in the denominator.

### Level 1b weak/exploratory

- A possible approximation could estimate central-value bias from curvature or non-commutativity using only published summaries.
- This would be a weak exploratory check, not a resolution of the median-mapping problem.
- It must be labeled as approximate and insufficient for physical claims.

### Level 2 pending posterior samples

- The strong audit requires joint posterior samples for `M_final` and `chi_final`.
- The target comparison is `median(f_Kerr(M_final, chi_final))` versus `f_Kerr(median(M_final), median(chi_final))`.
- Level 2 is pending availability of concrete posterior files, parameter names, event coverage, and frame conventions.

## Literature/systematics context

- Use recent ringdown/modeling-systematics literature as interpretation context.
- Foo & Hamilton 2024 supports treating precession/ringdown mismodeling as a possible bias source in parameter estimation and IMR tests.
- Völkel & Dhani 2025 supports treating unmodeled ringdown components, including overtones, quadratic modes, and tails, as possible sources of systematic bias in black-hole spectroscopy.
- Greybody/QNM work in modified spacetimes is secondary theoretical context, not an explanation of the Paper 4 data.
- Main interpretation: waveform/ringdown modeling and remnant-mapping systematics are more plausible gates than beyond-Kerr language.

## Limitations

- Small sample sizes and partial source dependence.
- Published scalar summaries rather than posterior samples.
- Shared or partially shared remnant provenance.
- Event selection and publication/reporting effects.
- Sigma conventions differ between sources.
- Damping/gamma channel is systematic-limited.
- No Level 2 remnant posterior propagation yet.
- No claim that residuals are independent draws without caveats.

## Reproducibility / artefacts

- List the exact documents and scripts that define the audit chain.
- Identify final tables that would be needed before deposit.
- Keep `runs/` out of git unless a later explicit artifact policy says otherwise.
- Ensure the final repository state has no ambiguous untracked interpretive documents.
- README should be updated only at the end, after the Paper 4 scope and deposit decision are fixed.

## Tables and figures needed later

- Source summary table.
- Frequency sign table.
- Paired common-events table.
- Remnant mapping status table.
- Limitations/provenance table.

Figures, if added later, should remain descriptive: sign distribution, paired residual comparison, or provenance map. No figure should imply a beyond-Kerr detection.

## Claims allowed

- No robust individual Kerr-violation candidates are identified.
- A positive sign asymmetry appears in `residual_f` across the current source/pipeline choices.
- The result is reproducible from published scalar summaries.
- The interpretation is systematic/modeling-limited.

## Claims forbidden

- No evidence for new physics.
- No candidate catalogue.
- No population-level Kerr violation claim.
- No claim that median mapping is solved without posterior samples.
- No gamma-based physical claim.

## Decision gates before deposit

- Final summary tables are reproducible.
- Limitations are explicit and placed near the main result.
- Level 2 posterior-sample availability is stated honestly.
- README is updated only at the end.
- No untracked interpretive documents are left ambiguous.

## Conclusion skeleton

Paper 4 should close as a technical audit unless posterior-level evidence changes the interpretation. The defensible result is that no individual frequency candidate emerges, while a small positive frequency-residual sign asymmetry persists across two published source/pipeline choices. The appropriate conclusion is a reproducible systematic-bias observation that motivates remnant-posterior and waveform-modeling audits, not a beyond-Kerr claim.
