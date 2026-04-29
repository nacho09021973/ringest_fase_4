# Paper 4 — Literature Context: Systematic Biases in Black-Hole Spectroscopy

## Scope

This document contextualizes the interpretation of the Paper 4 frequency-residual sign asymmetry using recent literature on waveform, ringdown, and black-hole spectroscopy systematics. It does not add new Paper 4 results, execute analysis, modify data, generate runs, or make candidate claims.

The purpose is to clarify that the current Paper 4 observation is best framed as a methodological/modeling-systematics result unless and until specific systematic gates are passed.

## Paper 4 observation

Paper 4 has documented a positive population-level sign asymmetry in `residual_f`:

- GWTC-2 TGR IMR phase1: 14/16 positive `residual_f`, with `p_one_sided_positive ~= 0.00209`.
- GWTC-4 pSEOBNR: 9/9 positive `residual_f`, with `p_one_sided_positive ~= 0.00195`.
- Paired common events: 5/5 preserve positive sign across the two sources/pipelines.

This is not an individual candidate claim. No frequency-only event reaches the current robust outlier threshold, and the gamma/damping channel is systematics-limited. The result is therefore a methodological/statistical observation requiring systematic interpretation.

The relevant source context is LVK TGR-style reporting: the phase1 table uses GWTC-2 TGR IMR ringdown quantities, while the comparison source uses GWTC-4 pSEOBNR quantities. Paper 4 consumes these published products downstream; it does not rerun the LVK waveform analyses or reconstruct the full posterior products behind the tables.

## Directly relevant literature

### Foo & Hamilton 2024

Cheng Foo and Eleanor Hamilton, "Systematic bias due to mismodeling precessing binary black hole ringdown," Physical Review D 110, 104024 (2024). DOI: `10.1103/PhysRevD.110.104024`. arXiv: `2408.02671`.

Foo & Hamilton study systematic bias from mismodeling the ringdown frequency in the coprecessing-frame treatment of precessing binary black hole waveforms. Their result is directly relevant because it shows that ringdown/precession modeling can bias parameter estimation and inspiral-merger-ringdown consistency tests of general relativity, especially for high-mass systems and systems with high mass ratios, high spin magnitudes, and highly inclined spins.

For Paper 4, this supports a conservative hypothesis: a population-level `residual_f` sign asymmetry could be associated with waveform or ringdown modeling systematics in the source pipelines.

Limit: Foo & Hamilton do not prove that the Paper 4 sign pattern comes from precession. Paper 4 does not measure precession directly, does not reanalyze waveform posteriors, and has not yet audited whether the positive-sign events occupy the high-risk regions emphasized in that work.

### Völkel & Dhani 2025

Sebastian H. Völkel and Arnab Dhani, "Quantifying systematic biases in black hole spectroscopy," Physical Review D 112, 084076 (2025). DOI: `10.1103/g6sz-dw28`. arXiv: `2507.22122`.

Völkel & Dhani study systematic biases in black-hole spectroscopy. They use linear-signal analysis to quantify biases from potentially unmodeled contributions in ringdown models, including overtones, quadratic modes, and tails, and discuss relevance both for high-precision simulations and detector data.

For Paper 4, this is directly relevant because the observed pattern is small per event but coherent at the population level. A recent spectroscopy-bias framework reinforces that such a pattern should first be treated as potentially systematic/modeling-limited rather than as a physical beyond-Kerr discrepancy.

Limit: Völkel & Dhani do not prove that the Paper 4 positive sign has this cause. Their work strengthens the interpretation gate: unmodeled-mode and ringdown-model biases must be considered before any physical interpretation.

## Secondary theoretical context

Recent work on QNM and greybody factors in modified or quantum-corrected spacetimes can provide broad theoretical context for how near-horizon or beyond-Kerr structure may affect quasinormal spectra and transmission properties.

That literature is secondary for Paper 4. It does not directly explain the observed `residual_f` sign asymmetry in LVK-derived published tables, and it should not be used as evidence for a strong-field deviation in this project. It may be useful for general motivation, but not as the primary interpretation of the Paper 4 pattern.

## Connection to remnant median mapping

The literature context should be read together with the remnant median mapping gate. Paper 4 currently evaluates `f_Kerr` at point estimates of `M_final` and `chi_final`, but the physically stronger comparison would propagate the joint remnant posterior through the nonlinear Kerr frequency map. In general, `median(f_Kerr(M_final, chi_final))` need not equal `f_Kerr(median(M_final), median(chi_final))`, especially when the remnant posterior is asymmetric or `M_final` and `chi_final` are correlated.

This non-commutativity is not the same systematic as waveform/ringdown modeling bias, but both can create coherent residual structure without requiring a Kerr deviation. They should therefore be treated as linked interpretation gates before any Paper 4 writeup.

## Consequence for Paper 4 interpretation

- Prioritize waveform/ringdown modeling systematics before physical interpretation.
- Do not use beyond-Kerr language.
- Add precession/ringdown modeling bias as a systematic gate.
- Add unmodeled-mode bias, including overtones, quadratic modes, and tails, as a systematic gate.
- Connect these gates with the remnant median mapping audit and posterior non-commutativity, because all of them can create coherent residual structure without requiring a physical Kerr deviation.
- If traceable event-level metadata are available, later audits should check mass, mass ratio, spin magnitude, inclination/precession indicators, and ringdown model assumptions before any writeup claims more than a methodological result.

## Allowed language

- Population-level sign asymmetry.
- Modeling-systematics candidate.
- Systematic-bias hypothesis.
- Methodological result.

## Forbidden language

- Detection.
- Evidence for new physics.
- Kerr violation.
- Greybody-factor explanation of the data.

## Immediate next step

Integrate this context into the Paper 4 methodological synthesis or into the future Paper 4 outline.

The conservative choice is to integrate it first into the synthesis, because that document governs the allowed interpretation before any result-note or paper-outline drafting begins.
