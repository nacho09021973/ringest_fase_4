# Paper 4 Initial Architecture

## Estado operativo

RINGEST Fase 1, Fase 2 y Fase 3 estan depositadas en Zenodo como fases cerradas del proyecto publico.

RINGEST Fase 4 es, por ahora, solo el workspace activo en GitHub. No tiene deposito Zenodo asociado.

Este paso no ejecuta ningun analisis nuevo, no recalcula resultados y no crea outputs cientificos.

## Criterio de deposito

Fase 4 solo ira a Zenodo si produce resultados defendibles.

Un resultado defendible debe tener provenance completa, trazabilidad documental, comparacion conservadora y una interpretacion compatible con las restricciones heredadas de Fase 3.

Si Fase 4 no produce resultados defendibles, no debe convertirse en un deposito por inercia.

## Objetivo de Fase 4

Fase 4 explora candidatos QNM/ringdown defendibles.

La exploracion esta subordinada a dos filtros:

1. consistencia Kerr;
2. auditoria de sistematicos.

La fase no parte de una afirmacion de nueva fisica y no debe convertir discrepancias aisladas en discovery claims.

## Pregunta fisica concreta

Despues de separar reporting heterogeneity, evolucion de pipeline, parametrizacion, incertidumbre Kerr, seleccion de fuente y evolucion de catalogo:

> Queda algun evento, modo u observable ringdown que sea anomalamente robusto de forma fisicamente interpretable?

## Taxonomia minima

Cada evento, modo u observable candidato debe clasificarse al menos en una de estas clases:

| Clase | Significado operativo |
|---|---|
| `reporting_artifact` | La anomalia desaparece o queda explicada por convencion de reporting. |
| `pipeline_evolution` | La anomalia es compatible con cambios de pipeline o catalogo LVK. |
| `parameterization_effect` | La anomalia depende de parametrizacion absoluta, fraccional o reconstruida. |
| `modal_label_ambiguity` | La anomalia depende de etiquetas agnosticas o identificacion modal posterior. |
| `uncertainty_incomplete` | La tension aparente usa errores incompletos o no comparables. |
| `low_N_candidate` | El caso es interesante, pero el tamano muestral no soporta conclusion fuerte. |
| `physics_candidate` | El caso sobrevive a los filtros anteriores y mantiene plausibilidad fisica. |

## Candidato defendible

Un candidato defendible debe cumplir, como minimo:

- no depender de una sola fuente o una sola convencion de reporting;
- conservar provenance completa hasta tabla, catalogo o documento primario;
- sobrevivir a intervalos asimetricos y comparaciones conservadoras;
- no reducirse a una discrepancia fragil de `tau_ms` sin soporte adicional;
- distinguir frecuencia, damping time, parametrizacion y etiqueta modal;
- declarar explicitamente la incertidumbre Kerr usada;
- mantener plausibilidad Kerr o explicar por que la tension seria fisicamente significativa;
- seguir siendo interesante despues de separar sistematicos conocidos.

## No cuenta como candidato

No cuenta como candidato defendible:

- un score alto sin interpretacion fisica;
- una mejora de R2 o ajuste estadistico sin plausibilidad Kerr;
- un embedding, cluster o distancia latente sin trazabilidad fisica;
- una familia geometrica construida sobre variables no auditadas;
- una tension calculada con errores incompletos o no comparables;
- un no-solapamiento aislado de `tau_ms`;
- una diferencia entre pipelines LVK sin fuente externa;
- una etiqueta agnostica tratada como modo Kerr definitivo;
- una figura sin tabla o sin provenance reproducible.

## Condiciones de avance

Fase 4 puede avanzar si se cumplen estas condiciones:

1. la taxonomia queda cerrada antes de introducir nuevas metricas;
2. los casos iniciales se documentan como matriz de candidatos, no como claims;
3. cada candidato tiene fuente, comparacion, incertidumbre y clase asignada;
4. los sistematicos heredados de Fase 3 se aplican antes de interpretar fisica;
5. cualquier analisis nuevo queda justificado por una pregunta fisica concreta;
6. las conclusiones se formulan de forma conservadora y falsable.

## Condiciones de cierre

Si no hay candidatos robustos ni conclusion metodologica clara, el proyecto publico queda cerrado en Fase 3 / Paper 3.

En ese caso, Fase 4 no debe forzar un Paper 4, no debe crear deposito Zenodo y no debe inflar resultados de N pequeno.
