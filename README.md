# RINGEST Fase 4 — Discovery-filter candidate generation

![RINGEST Phase 4 social preview](docs/social_preview.png)

## Estado

Workspace inicial de Fase 4.

Fase 3 queda congelada como Paper 3 / reporting heterogeneity.

Fase 4 comienza como filtro de discovery condicionado por Fase 3.

No parte de una afirmación de nueva física.

## Pregunta central

Después de controlar heterogeneidad de reporting, evolución de pipeline, parametrización, incertidumbre Kerr y selección de fuente:

> ¿queda algún evento, modo u observable que siga siendo anómalo de forma físicamente robusta?

## Dependencia de Fase 3

Fase 3 documentó dos casos trazables donde `f_hz` solapa entre fuentes, pero `tau_ms` no solapa:

| Evento | Comparación | f_hz | tau_ms |
|---|---|---|---|
| GW190521 | baseline A vs Capano 2023 | solapa | no solapa |
| GW190910_112807 | baseline A vs GWTC-4.0 Table 3 | solapa | no solapa |

Interpretación permitida heredada de Fase 3:

- `tau_ms` parece más frágil que `f_hz` en los casos auditados.
- Una discrepancia aislada en `tau_ms` puede ser reporting heterogeneity.
- No debe confundirse automáticamente con tensión Kerr.
- No hay conclusión poblacional.

## Objetivo de Fase 4

Explorar si queda algún patrón candidato a discovery una vez separadas:

1. heterogeneidad de reporting;
2. evolución de pipeline;
3. parametrización absoluta vs fraccional;
4. etiquetas agnósticas vs identificación modal posterior;
5. incertidumbre Kerr;
6. selección de eventos;
7. evolución de catálogo LVK.

## Qué podría contar como candidato

Un candidato solo puede considerarse interesante si cumple, como mínimo:

- no depende de una sola fuente;
- no desaparece al cambiar convención de reporting;
- no se explica solo por intervalos asimétricos;
- no se reduce a `tau_ms` frágil sin soporte adicional;
- tiene provenance completa;
- conserva plausibilidad Kerr o explica claramente por qué la tensión sería significativa;
- sobrevive a una comparación conservadora.

## Qué no cuenta como discovery

No cuenta como discovery:

- un no-solapamiento aislado de `tau_ms`;
- una diferencia entre pipelines LVK sin fuente externa;
- un resultado tomado de figura sin tabla;
- una desviación parametrizada forzada a `f_hz`/`tau_ms`;
- una etiqueta agnóstica tratada como modo Kerr definitivo;
- una mejora de R² sin plausibilidad física;
- un patrón de N pequeño sobrevendido.

## Estrategia inicial

Fase 4 no empieza buscando una métrica compleja.

Empieza clasificando cada anomalía potencial como:

| Clase | Significado |
|---|---|
| `reporting_artifact` | explicable por reporting heterogeneity |
| `pipeline_evolution` | explicable por cambio LVK/pipeline |
| `parameterization_effect` | explicable por delta_f/delta_tau o reconstrucción |
| `modal_label_ambiguity` | etiqueta agnóstica o identificación posterior |
| `low_N_candidate` | interesante pero N insuficiente |
| `physics_candidate` | sobrevive a los filtros anteriores |

## Restricciones iniciales

- No afirmar discovery física.
- No recalcular nada al crear el workspace.
- No reintroducir ESPRIT.
- No crear scripts efímeros.
- No inflar N pequeño.
- No modificar Fase 1, Fase 2 ni Fase 3.
- No añadir PDFs primarios todavía.
- No proponer métricas nuevas antes de cerrar la taxonomía.

## Próximo paso

Crear una nota de arquitectura de Paper 4 y, después, una matriz documental inicial de candidatos con solo los casos ya trazados en Fase 3.

## Paper 4 / Phase 4 — Frequency-residual sign asymmetry audit

Fase 4 se cierra como auditoría metodológica. No produce un catálogo de candidatos beyond-Kerr ni una afirmación de nueva física.

### Objetivo

Auditar, sobre el residual escalar `residual_f = f_pipeline_hz − f_kerr_hz`, si después de controlar reporting heterogeneity y propagación de incertidumbre Kerr a nivel 1a queda algún patrón robusto al cambiar de fuente o pipeline.

### Datasets

- `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv` — GWTC-2 TGR IMR consolidado.
- `runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset_220.csv` — GWTC-4 pSEOBNR.

Ambos llevan `sigma_f_kerr_hz` y `kerr_sigma_source = propagated`, es decir, level 1a remnant uncertainty propagada desde la mediana del remanente.

### Resultado principal

- Ningún evento individual presenta outlier robusto frequency-only ≥ 2σ.
- `residual_f` exhibe una asimetría positiva reproducible entre fuentes:
  - GWTC-2 TGR IMR: 14/16 positivos, p ≈ 0.00209 (binomial exacto, una cola).
  - GWTC-4 pSEOBNR: 9/9 positivos, p ≈ 0.00195 (binomial exacto, una cola).
  - Eventos comunes a ambos datasets: 5/5 mantienen signo positivo.
- Gamma/damping queda systematic-limited y no se incluye como observable de auditoría en esta fase.

### Interpretación permitida

`methodological_systematics_limited`. La asimetría positiva es reproducible pero su magnitud es del orden de los systematics conocidos del mapeo Kerr a nivel 1a y no constituye evidencia de desviación física.

### Limitaciones

- Auditoría basada en summaries escalares; no usa posterior samples directos.
- Level 2 remnant uncertainty (con posterior samples reales) queda pendiente.
- No se reclama beyond-Kerr, ni Kerr violation, ni catálogo de candidatos.
- O4 / GW250114 fuera de alcance.

### Reproducibilidad

Para regenerar las tablas finales:

```
python3 tools/paper4_build_summary_tables.py
```

Las tablas congeladas para depósito viven en:

```
results/paper4_summary_tables/
```

Detalle del release técnico en `docs/paper4_release_manifest.md`.
