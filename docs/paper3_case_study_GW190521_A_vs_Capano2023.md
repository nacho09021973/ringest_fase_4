# Paper 3 — Case study: GW190521 baseline A vs Capano 2023

## Objetivo

Comparar, de forma documental y preliminar, el evento GW190521 entre:

- baseline A: LVK/TGR GWTC-2;
- fuente B: Capano et al. 2023, `B_abs_agnostic_labels`.

## Inputs

| Fuente | Artefacto | Clasificación |
|---|---|---|
| A | `outputs/paper3/baseline_a_coverage.csv` | baseline_A |
| B | `data/phase1_data/qnm_events_capano2023.yml` | B_abs_agnostic_labels |

## Hechos de fuente B

Capano 2023 proporciona dos resonancias agnósticas a `tref + 6 ms`:

| range | identificación posterior | f_hz | tau_ms | notas |
|---|---|---:|---:|---|
| A | 220_candidate | 63 +2/-2 | 26 +8/-6 | rango agnóstico [50, 80] Hz |
| B | 330_candidate | 98 +89/-7 | 40 +50/-30 | rango agnóstico [80, 256] Hz |

## Comparabilidad

La comparación directa limpia con baseline A solo puede hacerse, en principio, entre:

- baseline A modo 220;
- Capano range A / 220_candidate.

La resonancia Capano range B / 330_candidate no tiene equivalente en baseline A si baseline A solo contiene 220.

## Cautelas

- Capano usa etiquetas agnósticas y posterior identificación modal.
- Los intervalos de Capano son asimétricos.
- Baseline A usa un esquema distinto de incertidumbre.
- No se debe calcular residual A-B hasta definir una función de comparación que trate intervalos asimétricos.
- Este caso no constituye una cohorte; es un estudio de caso de reporting heterogeneity para GW190521.

## Pregunta siguiente

¿Queremos construir un comparador permanente para A vs B que soporte intervalos asimétricos, o basta por ahora con una comparación manual documentada?

## Fila baseline A para GW190521

Cabecera y fila exactas, copiadas literalmente desde `outputs/paper3/baseline_a_coverage.csv`:

```csv
event_id,source_family,source_paper,mode,f_hz,sigma_f_hz,tau_ms,sigma_tau_ms,M_final_Msun,chi_final,redshift,sigma_M_final_Msun,sigma_chi_final,has_qnm_uncertainty,has_kerr_metadata,has_kerr_uncertainty,usable_for_baseline_A,usable_for_full_kerr_uncertainty
GW190521,A,Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog,220,68.0,4.0,15.8,3.2,147.4,0.62,0.825,40.0,0.23,True,True,True,True,True
```

Lectura inmediata, solo a título indicativo y sin calcular residual:

| Magnitud | Baseline A (modo 220) | Capano 2023 (range A / 220_candidate) |
|---|---|---|
| f_hz | 68.0 ± 4.0 (simétrica) | 63 +2/-2 (asimétrica) |
| tau_ms | 15.8 ± 3.2 (simétrica) | 26 +8/-6 (asimétrica) |
| frame | (convención baseline A) | detector |
| tiempo de análisis | (no explícito en baseline A) | tref + 6 ms |

Esta yuxtaposición es indicativa, no un test estadístico. La diferencia aparente en `tau_ms` es justamente el tipo de reporting heterogeneity que Paper 3 quiere caracterizar de forma trazable y con un comparador formal todavía por definir.

## Comparador permanente

- Script: `scripts/paper3/compare_gw190521_a_vs_capano2023.py`.
- Outputs:
  - `outputs/paper3/gw190521_a_vs_capano2023_comparison.csv`
  - `outputs/paper3/gw190521_a_vs_capano2023_comparison.md`
- Métricas calculadas: diferencias brutas (`delta_f_hz`, `delta_tau_ms`), intervalos A simétricos (`mean ± sigma`) e intervalos B asimétricos preservados (`mean - minus`, `mean + plus`), y banderas booleanas `overlap_f_interval` / `overlap_tau_interval` por intersección de intervalos.
- **No** se calculan p-values, ni residual sigma combinado, ni se simetrizan los intervalos de B. La Capano range B / 330_candidate queda explícitamente fuera porque baseline A no contiene 330 para GW190521.
