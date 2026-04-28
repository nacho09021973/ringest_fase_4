# Paper 3 — QNM reporting heterogeneity matrix

## Estado

Paper 3 — reporting heterogeneity.

Idea defendible, sin depender de GPU.

Este documento define la matriz mínima A/B/C/D/E de fuentes o extractores QNM publicados para auditar heterogeneidad de reporting y su impacto sobre residuales Kerr.

---

## Objetivo

Auditar la heterogeneidad entre fuentes publicadas de QNM para eventos GWTC y medir su impacto sobre conclusiones de consistencia Kerr.

La pregunta física no es si hay nueva física, sino:

> ¿Hasta qué punto el veredicto de consistencia Kerr depende de la fuente/extractor QNM usado y de sus convenciones de reporting?

---

## Unidad de comparación

Una fila corresponde a:

```text
evento + modo + fuente/extractor
```

Columnas mínimas:

| Columna                    | Significado                             |
| -------------------------- | --------------------------------------- |
| `event_id`                 | Identificador del evento GW             |
| `source_family`            | Familia A/B/C/D/E                       |
| `source_paper`             | Paper o catálogo de origen              |
| `mode`                     | Modo reportado, p. ej. 220              |
| `f_hz`                     | Frecuencia observada en Hz              |
| `sigma_f_hz`               | Incertidumbre en frecuencia             |
| `tau_ms`                   | Tiempo de damping, si se reporta así    |
| `sigma_tau_ms`             | Incertidumbre en tau                    |
| `gamma_hz`                 | Damping rate convertido a Hz            |
| `sigma_gamma_hz`           | Incertidumbre propagada de gamma        |
| `M_final_Msun`             | Masa final usada para Kerr              |
| `chi_final`                | Spin final usado para Kerr              |
| `redshift`                 | Redshift usado para marco detector      |
| `convention_notes`         | Notas de unidades/marco/convención      |
| `quality_flag`             | usable / partial / ambiguous / excluded |
| `usable_for_kerr_residual` | sí/no                                   |

---

## Matriz A/B/C/D/E

| ID | Fuente/extractor | Tipo                         | Eventos cubiertos | Modos    | Incertidumbres completas | Estado    |
| -- | ---------------- | ---------------------------- | ----------------: | -------- | ------------------------ | --------- |
| A  | LVK / TGR        | baseline institucional       |               TBD | 220      | TBD                      | baseline  |
| B  | pyRing           | ringdown Bayesian dedicado   |               TBD | 220/221? | TBD                      | candidate |
| C  | Isi et al.       | ringdown parametrizado       |               TBD | 220      | TBD                      | candidate |
| D  | Giesler et al.   | overtone-aware               |               TBD | 220/221  | TBD                      | candidate |
| E  | Capano / otros   | fuente alternativa publicada |               TBD | TBD      | TBD                      | candidate |

---

## Nota A_double_prime LVK/O4a Remnants

GWTC-4.0 Remnants (`arXiv:2603.19021`) queda confirmado como fuente tabular LVK posterior al baseline A.

Clasificación: `A_double_prime_LVK_O4a_remnants / B_param_with_reconstructed_abs`.

Siguiente evento recomendado: `GW190910_112807`, no `GW190519_153544`, porque la lectura primaria apunta a mayor heterogeneidad en `tau220` con frecuencia `f220` relativamente estable.

---

## Criterio de inclusión

Una fuente entra en la comparación principal solo si reporta:

* evento identificable;
* modo identificable;
* frecuencia o frecuencia angular convertible;
* damping time o damping rate convertible;
* incertidumbre trazable;
* referencia bibliográfica exacta;
* convención de marco suficientemente clara: source frame / detector frame / redshift aplicable.

---

## Exclusiones

No entra como fuente principal ningún extractor propio no validado sobre strain crudo.

La antigua rama ESPRIT queda fuera del Paper 3 salvo como ejemplo metodológico de failure mode ya cerrado.

No se reintroducen scripts eliminados de Ruta C.

---

## Métrica mínima de desacuerdo entre fuentes

Para dos fuentes `i, j` que reportan el mismo evento y modo:

```text
delta_f_ij = (f_i - f_j) / sqrt(sigma_f_i^2 + sigma_f_j^2)

delta_gamma_ij = (gamma_i - gamma_j) / sqrt(sigma_gamma_i^2 + sigma_gamma_j^2)
```

Clasificación preliminar:

| Rango       | Interpretación                                      |
| ----------- | --------------------------------------------------- |
| `< 1 sigma` | compatible entre fuentes                            |
| `1–2 sigma` | diferencia moderada                                 |
| `2–3 sigma` | tensión de reporting                                |
| `> 3 sigma` | desacuerdo fuerte o convención/sistemático probable |

---

## Impacto sobre Kerr

Para cada fuente usable se calculará, o se reutilizará si ya existe:

```text
r_f = (f_obs - f_Kerr) / sqrt(sigma_f_obs^2 + sigma_f_Kerr^2)

r_gamma = (gamma_obs - gamma_Kerr) / sqrt(sigma_gamma_obs^2 + sigma_gamma_Kerr^2)
```

El objetivo del Paper 3 es detectar casos donde:

```text
verdict_kerr(source A) != verdict_kerr(source B)
```

o donde el residual cambia de forma físicamente relevante al cambiar fuente.

---

## Salida esperada

Tabla de solapamiento:

* eventos presentes en al menos 2 fuentes;
* eventos presentes en al menos 3 fuentes;
* eventos con desacuerdo significativo en frecuencia;
* eventos con desacuerdo significativo en damping;
* eventos donde cambia el veredicto Kerr al cambiar fuente;
* eventos dominados por ambigüedad de convención o reporting incompleto.

---

## Qué podrá afirmar el paper

El paper podrá afirmar, si los datos lo sostienen:

* qué eventos tienen reporting QNM robusto entre fuentes;
* qué eventos dependen fuertemente del extractor o fuente;
* qué discrepancias afectan al residual Kerr;
* qué parte de una aparente tensión Kerr puede ser reporting heterogeneity;
* qué subcohorte mínima es estable frente a elección razonable de fuente.

---

## Qué no afirmará

* No afirmará nueva física.
* No afirmará violación de Kerr.
* No afirmará evidencia holográfica.
* No usará embeddings A/B como conclusión física principal.
* No interpretará tensiones con N pequeño sin marcarlas como preliminares.

---

## Próximo paso

Auditar `data/phase1_data/qnm_events_literature.yml` y extraer:

1. lista de eventos;
2. fuente bibliográfica actual;
3. modos disponibles;
4. campos de incertidumbre presentes;
5. campos faltantes que impiden comparación A/B/C/D/E.

---

## Diagnóstico inicial del input canónico actual

Input inspeccionado en esta copia de fase 2:

```text
data/phase1_data/qnm_events_literature.yml
```

Nota de ruta: el fichero canónico actual está bajo `data/phase1_data/qnm_events_literature.yml`.

Hecho verificado: el YAML contiene 19 eventos, todos con una única fuente bibliográfica QNM y un único modo `(l,m,n) = (2,2,0)`.

El `source_paper` exacto en las 19 filas es:

```text
Tests of General Relativity with Binary Black Holes from the second LIGO-Virgo Gravitational-Wave Transient Catalog
```

| event_id | source_paper | modos | QNM observables presentes | metadata Kerr presente | uso actual |
| --- | --- | --- | --- | --- | --- |
| GW150914 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW170104 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW170814 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW170823 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190408_181802 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190421_213856 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190503_185404 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190512_180714 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190513_205428 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190519_153544 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190521 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190521_074359 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190602_175927 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190706_222641 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190708_232457 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190727_060333 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190828_063405 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190910_112807 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |
| GW190915_235702 | LVK TGR GWTC-2 | 220 | f_hz, sigma_f_hz, tau_ms, sigma_tau_ms | M_final_Msun, chi_final, z, sigma_M_final_Msun, sigma_chi_final | baseline A |

Resumen de campos:

| Campo | Cobertura observada | Comentario |
| --- | ---: | --- |
| `event_id` | 19/19 | En el YAML aparece como clave `event`. |
| `source_paper` | 19/19 | Una sola fuente: LVK/TGR GWTC-2. |
| `mode` | 19/19 | Disponible como `l`, `m`, `n`; todos son 220. |
| `f_hz` | 19/19 | Presente. |
| `sigma_f_hz` | 19/19 | Presente. |
| `tau_ms` | 19/19 | Presente. |
| `sigma_tau_ms` | 19/19 | Presente. |
| `M_final_Msun` | 19/19 | Presente. |
| `chi_final` | 19/19 | Presente. |
| `redshift` | 19/19 | Presente semánticamente como `z`, no con clave literal `redshift`. |
| `sigma_M_final_Msun` | 19/19 | Presente. |
| `sigma_chi_final` | 19/19 | Presente. |
| `gamma_hz` | 0/19 | No está escrito; debe derivarse desde `tau_ms` si se usa damping rate. |
| `sigma_gamma_hz` | 0/19 | No está escrito; debe propagarse desde `sigma_tau_ms`. |
| `source_family` | 0/19 | No está escrito; inferible por ahora como baseline A. |
| `quality_flag` | 0/19 | No está escrito. |
| `usable_for_kerr_residual` | 0/19 | No está escrito. |

Veredicto:

* Usable para baseline A: si. El YAML actual sirve como cohorte LVK/TGR para residuales Kerr 220, con frecuencia, damping time y sigmas QNM presentes en todos los eventos.
* Insuficiente todavía para matriz A/B/C/D/E: si. No hay varias fuentes por evento, no hay pyRing/Isi/Giesler/Capano codificados, y por tanto no existe solapamiento real entre fuentes dentro del YAML actual.
* Insuficiente para propagación completa de incertidumbre Kerr por falta de sigmas de `M_final` o `chi_final`: no en este YAML. `sigma_M_final_Msun` y `sigma_chi_final` están presentes en los 19 eventos. La limitación pendiente no es ausencia de esas sigmas, sino validar que su convención PE es compatible con el cálculo Kerr usado.

Lectura física sobria: el input actual permite una línea base institucional A y una auditoría interna de consistencia Kerr para 19 eventos 220. No permite todavía estudiar reporting heterogeneity A/B/C/D/E, porque solo contiene una fuente QNM por evento y no contiene comparadores publicados independientes.

### Estado actual de la matriz A/B/C/D/E

- El YAML actual contiene 19 eventos.
- Todos los eventos proceden de una sola familia de fuente: LVK/TGR GWTC-2.
- Esto permite construir el baseline A.
- No permite todavía medir reporting heterogeneity entre fuentes.
- Para Paper 3 hace falta añadir o tabular fuentes adicionales B/C/D/E con provenance trazable.
- Por tanto, el resultado actual es diagnóstico de cobertura, no aún análisis de heterogeneidad.

## Artefacto baseline A

- Script usado: `scripts/paper3/build_baseline_a_coverage.py`.
- CSV producido: `outputs/paper3/baseline_a_coverage.csv`.
- Fuente YAML: `data/phase1_data/qnm_events_literature.yml`.
- Número de filas: 19 (una por evento, modo `(2,2,0)`).
- Alcance: este artefacto cubre baseline A (LVK/TGR GWTC-2). No es la matriz de heterogeneidad A/B/C/D/E; las fuentes B/C/D/E aún no están codificadas en el YAML canónico.

### Auditoría de incertidumbres Kerr (baseline A)

En la auditoría posterior del CSV, las 19 filas tienen `sigma_M_final_Msun` y `sigma_chi_final` presentes; por tanto el baseline A actual es usable para propagación completa de incertidumbre Kerr dentro de esta fuente.

Esto no implica heterogeneidad A/B/C/D/E: sigue habiendo una sola familia de fuente QNM en el YAML actual.

## Decisión de almacenamiento por fuente

- Paper 3 usará un YAML por familia/fuente QNM.
- Baseline A queda en `data/phase1_data/qnm_events_literature.yml`.
- La fuente B candidata será pyRing, en un futuro `data/phase1_data/qnm_events_pyring.yml`.
- No se debe mezclar pyRing dentro del YAML de baseline A.
- Esta separación preserva provenance, permite comparar fuente contra fuente y evita convertir la matriz A/B/C/D/E en una tabla ambigua.
- El fichero pyRing todavía no debe crearse con datos hasta tener identificada la tabla/paper exacto y sus convenciones.
- La afirmación de solape real A/B se considera pendiente hasta tabular event_id concretos desde la fuente B.

## Fuente B candidata: pyRing

- Fuente B candidata: pyRing-related Carullo literature. La fuente tabular exacta queda pendiente de identificación.
- Referencias relevantes, separadas para evitar confusión bibliográfica:
  - Carullo et al., *Phys. Rev. D* **98**, 104020 (2018) — *Empirical tests of the black hole no-hair conjecture using gravitational-wave observations*; referencia del test de no-hair / parametrized ringdown.
  - G. Carullo, *Phys. Rev. D* **103**, 124043 (2021) — *parametrized ringdown spin expansion coefficients formalism*; trabajo distinto al anterior.
- Aún no está confirmado que ninguna de las dos referencias contenga una tabla directamente convertible a `f_hz` / `tau_ms` por evento y modo; eso es lo que hay que determinar al leerlas.
- Rol: primera fuente independiente frente al baseline A LVK/TGR GWTC-2.
- Motivo: pyRing es metodológicamente distinto al baseline A y está orientado a análisis bayesiano de ringdown post-merger; maximiza la señal esperable de reporting heterogeneity respecto a un test IMR-consistency institucional.
- Antes de crear `data/phase1_data/qnm_events_pyring.yml`, hay que localizar:
  - paper exacto;
  - tabla exacta;
  - eventos;
  - columnas;
  - convenciones (marco source/detector, simetría de incertidumbres, parametrización del damping `tau` / `gamma` / `omega_I` / `Q`, valores absolutos vs desviaciones fraccionales).
- No se transcribirá ningún valor hasta resolver esos puntos.
- El solape A/B se considera desconocido hasta construir una tabla de `event_id` desde la fuente pyRing.

## Primer caso trazable de heterogeneidad

- Evento: GW190521.
- Comparación:
  - baseline A / LVK-TGR GWTC-2, modo 220.
  - Capano et al. 2023, range A / 220_candidate.
- Artefactos:
  - `scripts/paper3/compare_gw190521_a_vs_capano2023.py`
  - `outputs/paper3/gw190521_a_vs_capano2023_comparison.csv`
  - `outputs/paper3/gw190521_a_vs_capano2023_comparison.md`
  - `docs/paper3_case_study_GW190521_A_vs_Capano2023.md`
- Resultado:
  - frecuencia: intervalos solapan (`overlap_f_interval = True`).
  - damping time: intervalos no solapan (`overlap_tau_interval = False`).
- Interpretación:
  - evidencia documental de reporting heterogeneity en `tau_ms` para GW190521.
  - no es todavía test físico ni tensión Kerr.
  - no es conclusión de cohorte.
  - no incluye el modo 330 porque baseline A no tiene entrada 330.

## Segundo caso trazable de heterogeneidad

- Evento: GW190910_112807.
- Comparación:
  - baseline A / LVK-TGR GWTC-2, modo 220.
  - GWTC-4.0 Remnants Table 3 / pSEOBNRV5PHM, modo 220.
- Clasificación:
  - `A_double_prime_LVK_O4a_remnants / B_param_with_reconstructed_abs`.
- Artefactos:
  - `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`
  - `scripts/paper3/compare_gw190910_a_vs_gwtc4_table3.py`
  - `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.csv`
  - `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.md`
  - `docs/paper3_case_study_GW190910_A_vs_GWTC4_table3.md`
- Resultado:
  - frecuencia: intervalos solapan.
  - damping time: intervalos no solapan.
- Interpretación:
  - evidencia documental de reporting heterogeneity en `tau_ms` para GW190910_112807.
  - no es test físico.
  - no es tensión Kerr.
  - no es fuente externa independiente.
  - no es conclusión de cohorte.
