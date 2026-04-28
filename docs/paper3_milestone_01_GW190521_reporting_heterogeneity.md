# Paper 3 — Milestone 01: GW190521 reporting heterogeneity

## Estado

Primer hito científico trazable de Fase 3.

Este documento resume el primer caso real de reporting heterogeneity construido con provenance completa.

## Pregunta

¿Cambia el observable reportado para un mismo evento y modo cuando se compara el baseline A LVK/TGR con una fuente independiente publicada?

## Caso

Evento:

- GW190521

Comparación:

- baseline A: LVK/TGR GWTC-2, modo 220.
- fuente B: Capano et al. 2023, range A / 220_candidate.

## Artefactos

| Tipo | Ruta |
|---|---|
| Input A | `outputs/paper3/baseline_a_coverage.csv` |
| Input B | `data/phase1_data/qnm_events_capano2023.yml` |
| Script | `scripts/paper3/compare_gw190521_a_vs_capano2023.py` |
| Output CSV | `outputs/paper3/gw190521_a_vs_capano2023_comparison.csv` |
| Output MD | `outputs/paper3/gw190521_a_vs_capano2023_comparison.md` |
| Caso documental | `docs/paper3_case_study_GW190521_A_vs_Capano2023.md` |
| Matriz general | `docs/paper3_reporting_heterogeneity_matrix.md` |

## Resultado mínimo

| Observable | Resultado |
|---|---|
| frecuencia | intervalos solapan |
| damping time | intervalos no solapan |

Valores producidos por el comparador:

- `delta_f_hz = -5.0`
- `delta_tau_ms = 10.2`
- `overlap_f_interval = True`
- `overlap_tau_interval = False`

## Interpretación

Este caso proporciona evidencia documental de reporting heterogeneity en `tau_ms` para GW190521.

La diferencia aparece en el damping time, no en la frecuencia bajo el criterio conservador de solapamiento de intervalos.

## Qué no afirma

Este hito no afirma:

- tensión física con Kerr;
- violación de GR;
- detección nueva;
- conclusión poblacional;
- conclusión sobre el modo 330;
- significancia estadística mediante p-value;
- residual combinado en sigma.

## Limitaciones

- Un solo evento.
- Una sola fuente B.
- Capano 2023 usa extracción agnóstica por rangos de frecuencia e identificación modal posterior.
- Capano reporta intervalos asimétricos.
- Baseline A y Capano no comparten exactamente el mismo esquema de reporting.
- El modo `330_candidate` de Capano queda fuera de esta comparación porque baseline A solo contiene 220.

## Conclusión provisional

Fase 3 ya tiene un primer caso defendible y reproducible de heterogeneidad de reporting:

> Para GW190521, la frecuencia reportada para el candidato 220 solapa entre baseline A y Capano 2023, pero el damping time no solapa.

Esto justifica continuar Paper 3 como auditoría de heterogeneidad de reporting, manteniendo separadas las afirmaciones metodológicas de cualquier interpretación física fuerte.

## Siguiente paso recomendado

Buscar un segundo caso independiente o ampliar la comparación con otra fuente, sin abandonar las reglas actuales:

- no scripts efímeros;
- no PDFs primarios versionados por defecto;
- no simetrizar intervalos asimétricos sin regla documentada;
- no mezclar `B_abs` y `B_param` sin esquema explícito.
