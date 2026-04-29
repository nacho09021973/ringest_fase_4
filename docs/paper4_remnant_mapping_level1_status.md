# Paper 4 — Remnant Mapping Level 1 Status

## Scope

This note closes the narrow Level 1a status for Paper 4 remnant mapping. It does not run analysis, recalculate residuals, modify CSV files, create scripts, generate runs, or make any beyond-Kerr claim.

## Initial meaning of Level 1

The initial Level 1 idea was local uncertainty propagation from the published remnant summaries into the Kerr frequency prediction. In practical terms, this means using `sigma_M_final_Msun` and `sigma_chi_final` to estimate a local `sigma_f_kerr_hz`, then combining that Kerr-side uncertainty with the observed frequency uncertainty in the denominator of `residual_f`.

This is a first-order uncertainty check. It is not posterior propagation and does not address the central-value bias that can arise from evaluating a nonlinear map at point medians.

## Verified current state

Inspection of the current Paper 4 220 CSV datasets showed that the required Level 1a fields are already present:

- `sigma_f_kerr_hz` exists in the phase1 GWTC-2 TGR IMR 220 dataset and in the GWTC-4 pSEOBNR 220 dataset.
- `kerr_sigma_source` is `propagated` for the inspected rows.
- `residual_f` is computed with the combined denominator using `sigma_freq_hz` and `sigma_f_kerr_hz`.

The active producer `02c_paper4_literature_to_dataset.py` implements this local propagation from `sigma_M_final_Msun` and `sigma_chi_final` into `sigma_f_kerr_hz`, and then uses that term in the standardized frequency residual.

## Consequence

The observed positive `residual_f` sign asymmetry is not an artifact of having completely ignored `sigma_M_final_Msun` and `sigma_chi_final` in the residual denominator. That narrow criticism is already reduced by the current datasets.

This does not mean that the full remnant mapping systematic is closed.

## Limit

The stronger remnant median mapping criticism remains unresolved. Paper 4 still evaluates `f_Kerr` at point values of `M_final_Msun` and `chi_final`. For a nonlinear Kerr map,

```text
median(f_Kerr(M_final, chi_final)) != f_Kerr(median(M_final), median(chi_final))
```

in general. A local sigma propagation does not reconstruct the joint posterior, does not encode the covariance between `M_final` and `chi_final`, and does not compute the posterior median of `f_Kerr`.

Therefore Level 1a does not answer whether the positive sign asymmetry could be driven by central-value median mapping or posterior non-commutativity.

## Updated taxonomy

| level | meaning | status |
|---|---|---|
| Level 0 | `f_Kerr` treated as a point value with no Kerr-side sigma. | Not the current Paper 4 residual state. |
| Level 1a | Local propagation of `sigma_M_final_Msun` and `sigma_chi_final` into `sigma_f_kerr_hz`, then use of that term in `residual_f`. | Already implemented in current datasets. |
| Level 1b | Approximate audit of central-value bias from curvature/non-commutativity using only published summaries. | Not implemented; weak approximation if attempted. |
| Level 2 | Real posterior samples for `M_final` and `chi_final`, with direct posterior propagation into `f_Kerr`. | Pending posterior-sample availability. |
| Level 3 | Posterior-level comparison by source/pipeline where compatible posterior products exist. | Future work. |

## Methodological verdict

Level 1a reduces one denominator-level criticism, but it does not authorize a strong physical interpretation. The Paper 4 frequency sign asymmetry remains a methodological/statistical observation and should still be treated as systematic/modeling-limited until posterior-level remnant propagation or an explicitly qualified approximation is available.

No candidate language, Kerr-violation language, or beyond-Kerr evidence language is justified by Level 1a.

## Recommendation

Do not create a new Level 1a script. The current producer and datasets already implement the local sigma propagation needed for Level 1a.

If Paper 4 continues technically, the next step should be one of two explicitly separated options:

1. Locate real posterior samples for `M_final` and `chi_final` and design a Level 2 propagation.
2. Design a Level 1b approximation using only published summaries, clearly labeled as exploratory and insufficient for physical claims.
