# RINGEST Fase 4 — Discovery-filter candidate generation

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
