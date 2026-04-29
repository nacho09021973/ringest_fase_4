# Paper 4 — Gamma/Tau Convention Audit

## Scope

This audit checks damping-time/gamma conventions for the largest descriptive 220 residuals. It does not identify physical candidates, does not change residuals, does not recalculate Kerr outputs, and does not change thresholds or row selection.

## Motivation

`docs/paper4_top_residuals_systematics_audit.md` found that the highest descriptive 220 residuals are dominated by `residual_gamma`, while obvious schema fields and uncertainty columns are populated. The next systematic to audit is therefore the convention connecting `tau_ms`, observed damping rate, Kerr damping rate, and detector/source-frame quantities.

## Code convention

`02c_paper4_literature_to_dataset.py` uses these conventions:

- Observed damping rate from literature damping time:
  `damping_hz = 1000.0 / tau_ms`.
- Observed imaginary angular frequency:
  `omega_im = -damping_hz`.
- Observed damping uncertainty propagated from `sigma_tau_ms`:
  `sigma_damping_hz = 1000.0 * sigma_tau_ms / tau_ms**2`.
- Kerr frequency uses detector-frame mass:
  `f_kerr_hz = omega_re_kerr / (2*pi*M_detector*G/c^3)`.
- Kerr damping rate uses detector-frame mass and does not divide by `2*pi`:
  `gamma_kerr_hz = -omega_im_kerr / (M_detector*G/c^3)`.
- Damping residual:
  `residual_gamma = (damping_hz - gamma_kerr_hz) / sqrt(sigma_damping_hz**2 + sigma_gamma_kerr_hz**2)`.

The code therefore treats gamma as an exponential decay rate `1/tau_s`, not as a cyclic frequency `1/(2*pi*tau_s)`.

## Source convention

For the top-five rows, `data/phase1_data/qnm_events_literature.yml` contains:

- `tau_ms`;
- `sigma_tau_ms`;
- `f_hz`;
- `sigma_f_hz`;
- `source_paper`.

The YAML does not contain an explicit `gamma_hz`, `damping_hz`, sign convention, or separate detector/source-frame flag for `tau_ms`. The source provenance for all five rows is:

```text
Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog
```

## Diagnostic comparison

These values are diagnostic only. They compare algebraic conventions without rewriting the dataset.

| event_id | tau_ms | sigma_tau_ms | gamma_current | 1000/tau_ms | 1/(2*pi*tau_s) | gamma_kerr_hz | residual_gamma |
|---|---:|---:|---:|---:|---:|---:|---:|
| GW150914 | 4.200 | 0.250 | 238.095 | 238.095 | 37.894 | 203.471 | 1.683 |
| GW190708_232457 | 2.100 | 0.150 | 476.190 | 476.190 | 75.788 | 391.898 | 1.569 |
| GW170814 | 3.700 | 0.250 | 270.270 | 270.270 | 43.015 | 226.359 | 1.515 |
| GW190521_074359 | 5.400 | 0.400 | 185.185 | 185.185 | 29.473 | 155.824 | 1.324 |
| GW170104 | 3.500 | 0.350 | 285.714 | 285.714 | 45.473 | 244.901 | 1.015 |

Additional detector/source-frame diagnostic:

| event_id | z | gamma_current | gamma_current/(1+z) | gamma_kerr_hz |
|---|---:|---:|---:|---:|
| GW150914 | 0.090 | 238.095 | 218.436 | 203.471 |
| GW190708_232457 | 0.197 | 476.190 | 397.820 | 391.898 |
| GW170814 | 0.124 | 270.270 | 240.454 | 226.359 |
| GW190521_074359 | 0.210 | 185.185 | 153.046 | 155.824 |
| GW170104 | 0.200 | 285.714 | 238.095 | 244.901 |

## Interpretation

- Simple tau/gamma convention issue: `gamma_current` is exactly `1000/tau_ms`, so the current observed-gamma convention is internally consistent with `1/tau_s`.
- Factor `2*pi`: not supported as a simple explanation. `1/(2*pi*tau_s)` is far below both `gamma_current` and `gamma_kerr_hz` for all five rows.
- Detector/source frame issue: plausible and unresolved. Dividing `gamma_current` by `(1+z)` brings several top rows much closer to `gamma_kerr_hz`, especially the moderate-redshift rows. This does not prove the frame convention is wrong; it flags the source-paper convention for `tau_ms` as a priority check.
- Uncertainty propagation issue: not obviously caused by missing fields. `sigma_tau_ms`, `sigma_M_final_Msun`, and `sigma_chi_final` are populated for these rows, but the propagation assumptions still need source-convention validation.
- Not resolved by convention audit: the audit narrows the main open question to detector/source-frame and damping-definition provenance in the original source.

## Limitations

- No definitive outputs are recalculated.
- Existing residuals are not changed.
- No physical candidates are declared.
- The conclusion depends on the correct interpretation of the original source table convention for `tau_ms`.

## Immediate next step

Review the original source table/protocol for `tau_ms` frame and damping definition before touching code or classifying residuals.
