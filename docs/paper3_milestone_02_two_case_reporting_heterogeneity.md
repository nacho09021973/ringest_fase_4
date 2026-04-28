# Paper 3 — Milestone 02: two-case reporting heterogeneity

## Estado

Paper 3 ya cuenta con dos casos trazables de reporting heterogeneity.

## Casos

| Evento | Comparación | f_hz | tau_ms | Fuente secundaria |
|---|---|---|---|---|
| GW190521 | baseline A vs Capano 2023 | solapa | no solapa | B_abs_agnostic_labels |
| GW190910_112807 | baseline A vs GWTC-4.0 Table 3 | solapa | no solapa | A_double_prime / B_param_with_reconstructed_abs |

## Interpretación común

En ambos casos auditados:

- la frecuencia del modo 220 o candidato 220 permanece compatible bajo el criterio conservador de solapamiento de intervalos;
- el damping time muestra no-solapamiento de intervalos;
- la heterogeneidad aparece en `tau_ms`, no en `f_hz`.

## Qué afirma

Esto afirma una regularidad documental en los casos auditados:

> `tau_ms` es más sensible que `f_hz` a las decisiones de reporting, pipeline, parametrización o extracción.

## Qué no afirma

No afirma:

- tensión física con Kerr;
- violación de GR;
- detección nueva;
- conclusión poblacional;
- p-value;
- residual sigma combinado;
- independencia externa en el caso GWTC-4.0.

## Provenance

### GW190521

- input A: `outputs/paper3/baseline_a_coverage.csv`
- input B: `data/phase1_data/qnm_events_capano2023.yml`
- script: `scripts/paper3/compare_gw190521_a_vs_capano2023.py`
- outputs:
  - `outputs/paper3/gw190521_a_vs_capano2023_comparison.csv`
  - `outputs/paper3/gw190521_a_vs_capano2023_comparison.md`

### GW190910_112807

- input A: `outputs/paper3/baseline_a_coverage.csv`
- input A_double_prime: `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`
- script: `scripts/paper3/compare_gw190910_a_vs_gwtc4_table3.py`
- outputs:
  - `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.csv`
  - `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.md`

## Próximo paso

No ampliar conclusiones todavía.

Opciones siguientes:

1. ampliar Table 3 a más eventos del baseline A;
2. construir matriz de cobertura con Table 1;
3. redactar estructura mínima del Paper 3.
