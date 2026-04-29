# Paper 4 — Remnant Median Mapping Audit Plan

## Scope

This document fixes how Paper 4 should audit the remnant median mapping systematic before any writeup. It does not execute analysis, create scripts, modify data, change YAML, generate runs, or decide publication.

The audit question is methodological: whether the positive sign asymmetry in `residual_f` could arise from comparing the published observed frequency against `f_Kerr` evaluated at point estimates of `M_final` and `chi_final`, rather than propagating the joint remnant posterior through the Kerr frequency map.

## Motivation

The current Paper 4 synthesis establishes that the interesting result is not an individual candidate. Individual frequency residuals are small, with no robust frequency-only outliers, while the positive sign asymmetry in `residual_f` is reproduced in the GWTC-4 pSEOBNR source and persists in common events across pipelines.

That makes remnant median mapping a key systematic before writeup. The Kerr frequency map is nonlinear in final mass and final spin, and point remnant medians need not commute with that map. A coherent offset introduced by this approximation could produce sign structure without requiring any physical discrepancy.

## The possible systematic

The current datasets use point values `M_final_Msun` and `chi_final`. The producer evaluates `f_Kerr` at those values and forms

```text
residual_f = (f_hz - f_kerr_hz) / sqrt(sigma_f_hz^2 + sigma_f_kerr_hz^2)
```

The ideal physical comparison would propagate the joint posterior samples for `M_final` and `chi_final` through the Kerr map event by event. In general,

```text
median(f_Kerr(M_final, chi_final)) != f_Kerr(median(M_final), median(chi_final))
```

The mismatch can be sign-coherent if the remnant posterior shapes are similar across events or if the same reporting convention is used across the cohort. The effect can also depend on the joint covariance between `M_final` and `chi_final`; treating the two medians independently discards that information.

## What would count as sufficient audit

### Level 0 — Current state

Only point remnant values are used. This is sufficient for a descriptive residual table, but not sufficient for a strong physical claim about a population-level discrepancy.

### Level 1 — Error propagation from sigmas

Use available `sigma_M_final_Msun` and `sigma_chi_final` values, if complete, to perform a local approximation to the uncertainty in `f_Kerr`. This can test whether a first-order remnant uncertainty budget plausibly absorbs the sign asymmetry.

Level 1 is a sanity check, not closure. It cannot represent non-Gaussian posterior shape, asymmetric credible intervals, or `M_final`/`chi_final` covariance.

### Level 2 — Posterior-sample propagation

Use real posterior samples of `M_final` and `chi_final` for each event and propagate each sample through the Kerr frequency map. Compare the resulting posterior distribution of `f_Kerr` to the published observed `f_hz` and its uncertainty convention.

This is the desirable standard for assessing whether median mapping is responsible for the sign asymmetry.

### Level 3 — Source-pipeline posterior consistency

Where both IMR and pSEOBNR sources provide compatible posterior information, compare the posterior-propagated Kerr frequency distributions across pipelines. This level tests whether the cross-pipeline sign persistence survives posterior-level remnant propagation rather than only point-median remnant propagation.

## Required inputs

| input | available now? | source | required for level |
|---|---|---|---|
| `M_final_Msun` | Yes, in produced datasets | YAML-derived remnant metadata materialized by the Paper 4 producer | Level 0 |
| `sigma_M_final_Msun` | Needs availability audit in phase1 and GWTC-4 pSEOBNR datasets | YAML/source remnant metadata if present and emitted | Level 1 |
| `chi_final` | Yes, in produced datasets | YAML-derived remnant metadata materialized by the Paper 4 producer | Level 0 |
| `sigma_chi_final` | Needs availability audit in phase1 and GWTC-4 pSEOBNR datasets | YAML/source remnant metadata if present and emitted | Level 1 |
| Joint posterior samples for `M_final`, `chi_final` | Not established by current documentation | GWOSC PE posterior samples or source-pipeline posterior products | Level 2 |
| Redshift or posterior redshift, if needed | Point `z` is present; posterior availability not established | YAML/source metadata and possible GWOSC posterior products | Level 2 |
| `f_hz` posterior or published `f_hz` uncertainties | Published point value and uncertainty are present; posterior availability not established | Source ringdown tables or posterior products | Level 2/3 |

## Minimal next implementation

Do not execute the audit yet. The minimal next implementation should be staged as follows:

1. Review whether `sigma_M_final_Msun` and `sigma_chi_final` are complete in the phase1 and GWTC-4 pSEOBNR datasets used by the sign tests.
2. Decide whether a permanent Level 1 script is worthwhile based on that coverage.
3. Do not attempt Level 2 until real posterior samples for `M_final` and `chi_final` are located and their provenance is documented.

## Failure modes

- If Level 1 already absorbs the sign asymmetry, the Paper 4 result becomes systematic-dominated rather than a writeup-ready physical discrepancy.
- If Level 1 does not absorb the sign asymmetry, that does not imply physics. It only justifies seeking Level 2 posterior-sample propagation.
- If posterior samples are unavailable or not comparable across the relevant events, Paper 4 must state that explicitly and keep the result framed as a methodological/statistical observation.
- If `M_final` and `chi_final` uncertainties are incomplete or convention-mismatched across sources, the audit must not silently mix them into a single population claim.
- If source pipelines share remnant posterior provenance, cross-pipeline reproduction remains only partially independent.

## Decision rule

- No strong physical Paper 4 writeup should proceed without at least a documented Level 1 audit plan and availability check.
- No candidate language is allowed under this gate, regardless of Level 1 or Level 2 outcome.
- If Level 2 is not available, the result remains a methodological/statistical observation.
- If Level 2 is available and does not absorb the sign coherence, the next step is still systematic interpretation, not a candidate catalog.

## Immediate next step

Audit availability of `sigma_M_final_Msun` and `sigma_chi_final` in the phase1 and GWTC-4 pSEOBNR datasets, without calculating residual changes yet.
