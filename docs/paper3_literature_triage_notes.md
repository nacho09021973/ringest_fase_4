# Paper 3 — Literature triage notes

## Fuente de esta nota

Esta nota resume el informe local:

`docs/Auditar Heterogeneidad QNM Ringdown Gravitacional.pdf`

El PDF se usa como triage bibliográfico interno, no como fuente primaria de valores QNM.

## Estado

Este documento registra el triage bibliográfico recibido para seleccionar fuentes B/C/D/E.

No autoriza todavía la creación de YAML B ni la transcripción de valores numéricos.

## Clasificación operativa

| Clase | Significado |
|---|---|
| B_abs | Fuente con valores absolutos comparables: `f_hz`, `tau_ms` o equivalentes convertibles con provenance directa |
| B_param | Fuente con desviaciones fraccionales respecto a Kerr: `delta_f`, `delta_tau`, `delta_omega_R`, `delta_omega_I`, etc. |
| No_tabular | Fuente metodológica o contextual sin tabla observacional directamente comparable |

## Candidatos identificados por el triage

| Candidato | Evento(s) | Clasificación provisional | Uso inicial |
|---|---|---|---|
| LVK/TGR GWTC-2/3 | 19 eventos baseline A | B_param | No empezar aquí; requiere decisión de transformación |
| Abbott et al. PRD 103, 122002 (2021) / Table IX | muchos eventos solapados con baseline A | A_prime_internal_LVK_TGR | Alta utilidad para auditar heterogeneidad interna; no fuente B externa |
| Isi et al. 2019 | GW150914 | B_param_focal_GW150914 / needs_more_provenance | Reclasificada tras lectura primaria; ver `paper3_source_B_abs_isi2019_reading.md` |
| Capano et al. 2023 | GW190521 | B_abs_agnostic_labels / ready_for_yaml_design | Reclasificada tras lectura primaria; ver `paper3_source_B_abs_capano2023_reading.md` |
| Siegel et al. 2023 / GW190521 | GW190521 | No_tabular / methodological_GW190521 | Útil como `interpretation_check_for_Capano2023`; no YAML sin data release |
| Isi & Farr 2021 / arXiv:2107.05609 | metodología / simulaciones | No_tabular / methodological_framework | No YAML; útil para metodología de ringdown |
| Cotesta et al. 2022 / GW150914 | GW150914 | No_tabular / methodological_GW150914 | No YAML; útil como `overtone_robustness_check` |
| Giesler et al. 2019 | NR / GW150914-like | No_tabular | Discusión sobre sobretonos y tiempo de inicio |
| Finch & Moore 2022 | GW150914 | No_tabular provisional | Discusión de estabilidad/sensibilidad |

Nota tras lectura primaria de Isi et al. 2019 ("Testing the no-hair theorem with GW150914", *Phys. Rev. Lett.* **123**, 111102, 2019): la fuente primaria **no** confirma una tabla absoluta `f_hz/tau_ms` para el modo `220`. Sólo aporta cantidades parametrizadas (`delta_f1`, `delta_tau1` referidas al sobretono `n=1`) más masa/spin remanente bajo hipótesis Kerr. Por eso baja a `B_param_focal_GW150914 / needs_more_provenance`. Detalles en `docs/paper3_source_B_abs_isi2019_reading.md`.

Nota tras lectura primaria de Capano et al. 2023 ("Multimode Quasinormal Spectrum from a Perturbed Black Hole", *Phys. Rev. Lett.* **131**, 221402, 2023; arXiv:2105.05238): la fuente primaria **sí** proporciona valores absolutos de `f` y `tau` para GW190521, pero a través de un análisis agnóstico en dos rangos de frecuencia (`range A` y `range B`) con identificación modal posterior como `(2,2,0)` y `(3,3,0)`. Los intervalos son asimétricos. Por eso pasa a `B_abs_agnostic_labels / ready_for_yaml_design`. Detalles en `docs/paper3_source_B_abs_capano2023_reading.md`.

## Decisión práctica

Para probar Fase 3, empezar por fuentes absolutas focales:

1. Isi et al. 2019 para GW150914.
2. Capano et al. 2023 para GW190521.

No empezar por `B_param` LVK/TGR hasta decidir formalmente si la matriz A/B/C/D/E comparará desviaciones parametrizadas además de observables absolutos.

## Reglas de cautela

- No usar el PDF de triage como fuente primaria de valores.
- No transcribir números desde fuentes secundarias.
- Verificar cada valor contra paper oficial, arXiv o data release.
- Si una fuente reporta intervalos creíbles asimétricos, no convertirlos a sigma simétrica sin documentar la regla.
- Si una fuente reporta desviaciones parametrizadas, no forzarla al esquema `f_hz/tau_ms`.
- El PDF sirve para priorizar lectura, no para poblar YAML.

## Próxima acción

Leer la fuente primaria de Isi et al. 2019 para GW150914 y decidir si permite crear un YAML `B_abs` mínimo.
