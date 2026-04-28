# Paper 3 — Case study: GW190910 baseline A vs GWTC-4 Table 3

## Evento

`GW190910_112807`

## Inputs

- Baseline A: `outputs/paper3/baseline_a_coverage.csv`
- A_double_prime: `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`

## Script

`scripts/paper3/compare_gw190910_a_vs_gwtc4_table3.py`

## Outputs

- `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.csv`
- `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.md`

## Resultado de solape

| observable | overlap_interval |
|---|---|
| `f_hz` | `True` |
| `tau_ms` | `False` |

## Interpretación

Este caso registra heterogeneidad de reporting entre baseline A y GWTC-4.0 Remnants Table 3 para `GW190910_112807`.

La frecuencia `f_hz` mantiene solape de intervalos.

El damping time `tau_ms` no mantiene solape de intervalos bajo la comparación mínima implementada.

## Cautela

Esto no es un test físico de Kerr.

Esto no afirma tensión física.

GWTC-4.0 Remnants Table 3 es una fuente LVK posterior al baseline A, clasificada como `A_double_prime_LVK_O4a_remnants / B_param_with_reconstructed_abs`.

No es una fuente B externa independiente.
