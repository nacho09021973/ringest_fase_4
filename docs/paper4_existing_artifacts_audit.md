# Paper 4 — Existing Artifacts Audit

## Scope

Esta auditoría inventaría artefactos ligeros/versionables ya presentes en el workspace de Fase 4.

No ejecuta análisis, no recalcula métricas, no genera tablas numéricas nuevas y no interpreta resultados nuevos. La lectura se limita a `docs/`, `runs_sync/`, `data/phase1_data/`, `data/phase1_outputs/` y markdown/README ya versionados.

La ruta solicitada `data/qnm_events_literature.yml` no existe en este workspace; la ruta canónica versionada es `data/phase1_data/qnm_events_literature.yml`.

## Candidate-relevant artifacts

| path | artifact type | physical use | limitation | reuse status |
|---|---|---|---|---|
| `data/phase1_data/qnm_events_literature.yml` | YAML canónico de eventos QNM publicados | Auditoría de input y generación documental de candidatos baseline 220; contiene `event`, modo, `f_hz`, `sigma_f_hz`, `tau_ms`, `sigma_tau_ms`, `M_final_Msun`, `chi_final`, `z` y sigmas Kerr/PE | Una sola familia de fuente QNM para la cohorte base; no resuelve heterogeneidad entre extractores por sí solo | Puede responder sin rerun qué eventos tienen input mínimo trazable; insuficiente para conclusión física |
| `data/phase1_data/qnm_events_capano2023.yml` | YAML de fuente alternativa Capano 2023 para GW190521 | Candidato documental para ambigüedad modal/reporting: rangos agnósticos, identificación posterior 220/330 y errores asimétricos | Un único evento; etiquetas agnósticas; no es una cohorte ni una prueba Kerr directa | Puede alimentar matriz de candidatos sin rerun; no basta para discovery |
| `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml` | YAML de GWTC-4.0 Remnants Table 3 para GW190910_112807 | Caso de evolución de pipeline/catálogo y parametrización reconstruida absoluta vs fraccional | Fuente LVK posterior, no fuente externa independiente; intervalos asimétricos y convención específica | Puede responder sin rerun una pregunta de reporting/pipeline; insuficiente como tensión física |
| `data/phase1_outputs/qnm_dataset.csv` | CSV canónico derivado ya versionado | Tabla ligera con observables QNM, metadata Kerr, valores Kerr esperados y residuales existentes | Es un output heredado; no debe ampliarse ni reinterpretarse sin auditoría de provenance | Útil para auditoría de input/comparación Kerr existente; no crea candidato por sí solo |
| `data/phase1_outputs/qnm_dataset_220.csv` | CSV filtrado 220 ya versionado | Subtabla ligera para preguntas centradas en modo 220 | Comparte las limitaciones del dataset canónico; no contiene heterogeneidad multi-fuente completa | Puede responder sin rerun qué filas 220 existen y qué metadata traen; insuficiente para conclusión física |
| `docs/paper3_case_study_GW190521_A_vs_Capano2023.md` | Estudio de caso documental | Define comparación baseline A vs Capano 2023 y marca `f_hz`/`tau_ms` como reporting heterogeneity | Indica outputs en `outputs/paper3/` que no están en el workspace ligero; no es test estadístico nuevo | Contexto candidato directo para matriz Paper 4; no es candidato físico cerrado |
| `docs/paper3_case_study_GW190910_A_vs_GWTC4_table3.md` | Estudio de caso documental | Registra solape en `f_hz` y no-solape en `tau_ms` entre baseline A y GWTC-4 Table 3 | Explícitamente no es test físico de Kerr; una fuente LVK posterior no independiza el caso | Puede responder sin rerun qué anomalía documental existe; insuficiente para claim físico |
| `docs/paper3_milestone_01_GW190521_reporting_heterogeneity.md` | Nota de milestone | Contexto trazable del caso GW190521 | Depende del alcance Paper 3 y de comparaciones ya cerradas | Contexto metodológico y candidato documental |
| `docs/paper3_milestone_02_two_case_reporting_heterogeneity.md` | Nota de milestone | Resume los dos casos trazables heredados por Fase 4 | No extiende N ni resuelve física | Puede guiar matriz inicial sin rerun |

## Kerr / consistency artifacts

| path | artifact type | physical use | limitation | reuse status |
|---|---|---|---|---|
| `runs_sync/verified/README.md` | README de runs verificados | Define que los artefactos Paper 2 son reproducibilidad tabulada y no evidencia de nueva física | Alcance Paper 2; no introduce candidatos Paper 4 | Contexto obligatorio antes de reutilizar resultados |
| `runs_sync/verified/kerr_population_tail_t9_verified_2026-04-27/RERUN_PROVENANCE.md` | Manifest/provenance con checksums | Verifica que los artefactos T9 vienen de inputs congelados y tienen checksums | Metadata externa no se adquiere en este run; no prueba física | Puede responder sin rerun si un archivo es verificable |
| `runs_sync/verified/kerr_population_tail_t9_verified_2026-04-27/population_metadata_table.csv` | CSV ligero de metadata y residuales Kerr previos | Base tabular existente para revisar cobertura, metadata física, residuales y verdicts heredados | Resultado downstream heredado; no debe reinterpretarse como discovery | Puede responder preguntas de auditoría de input/comparación Kerr existente sin rerun |
| `runs_sync/verified/kerr_population_tail_t9_verified_2026-04-27/population_metadata_coverage.json` | JSON de cobertura/provenance de metadata | Auditoría de procedencia de PE/search metadata | No es observable QNM primario | Puede responder sin rerun preguntas de cobertura y fuente |
| `runs_sync/verified/kerr_population_tail_t9_verified_2026-04-27/population_metadata_notes.md` | Notas de metadata | Contexto de adquisición/cobertura de metadata | No clasifica candidatos físicos | Solo contexto metodológico |
| `runs_sync/verified/kerr_population_tail_t9_verified_2026-04-27/population_tail_stats_table.csv` | CSV ligero de score poblacional y residuales | Permite revisar si existen relaciones heredadas entre rareza poblacional y residual Kerr | El propio run recomienda `KILL`; score poblacional no es evidencia física | Puede responder sin rerun una pregunta negativa/metodológica; insuficiente para candidato físico |
| `runs_sync/verified/kerr_population_tail_t9_verified_2026-04-27/population_tail_notes.md` | Resumen T9.2 | Documenta interpretación heredada NULL/KILL de population-tail | No sustituye auditoría Paper 4 por fuente QNM | Contexto metodológico; no candidato |
| `runs_sync/verified/kerr_population_tail_t9_verified_2026-04-27/population_tail_summary.json` | Resumen JSON T9.2 | Manifest ligero de resultados heredados | Formato de resumen, no tabla primaria de candidatos | Contexto y comprobación sin rerun |
| `runs_sync/verified/kerr_snr_systematics_t10_verified_2026-04-27/RERUN_PROVENANCE.md` | Manifest/provenance con checksums | Verifica integridad de artefactos SNR/sistemáticos | No añade física por sí mismo | Puede responder sin rerun si la auditoría es reproducible |
| `runs_sync/verified/kerr_snr_systematics_t10_verified_2026-04-27/snr_residual_audit_table.csv` | CSV ligero de auditoría SNR-residual | Diagnóstico técnico de relación SNR/residual heredada | El propio resumen limita el uso a sistemáticos/cobertura, no narrativa física | Puede responder sin rerun una pregunta de sistemáticos |
| `runs_sync/verified/kerr_snr_systematics_t10_verified_2026-04-27/snr_residual_notes.md` | Resumen T10.0 | Documenta `ROBUST_DIAGNOSTIC` para T6.6 y limitaciones para T8.2a/combined | Diagnóstico estadístico/técnico, no claim físico global | Contexto fuerte para auditoría de sistemáticos; no candidato físico |
| `runs_sync/verified/kerr_snr_systematics_t10_verified_2026-04-27/snr_residual_summary.json` | Resumen JSON T10.0 | Estado compacto del diagnóstico | No sustituye revisión de tabla/notas | Contexto |
| `runs_sync/verified/kerr_snr_systematics_t10_verified_2026-04-27/snr_overlap_decomposition.csv` | CSV ligero de descomposición overlap | Compara eventos solapados T6.6/T8.2a y separa cambios por observable/sigma/Kerr | Descriptivo; no afirma causalidad fuerte | Puede responder sin rerun si cambios vienen de input/sigmas vs predicción Kerr |
| `runs_sync/verified/kerr_snr_systematics_t10_verified_2026-04-27/snr_overlap_decomposition_notes.md` | Resumen T10.1 | Explica drivers como `OBS_SIGMA_CHANGE`, `OBS_SHIFT` o `MIXED` | Debe leerse como diagnóstico de waveform/posterior-systematics | Contexto clave para separar sistemáticos de candidatos físicos |
| `runs_sync/verified/kerr_snr_systematics_t10_verified_2026-04-27/snr_overlap_decomposition_summary.json` | Resumen JSON T10.1 | Manifest compacto de descomposición | No reemplaza tabla ni notas | Contexto |

## Route B / geometry-surrogate artifacts

| path | artifact type | physical use | limitation | reuse status |
|---|---|---|---|---|
| `docs/paper3_reporting_heterogeneity_matrix.md` | Protocolo Paper 3 con guardrails | Declara que embeddings A/B no serán conclusión física principal | No contiene un resultado Route B/all18 reutilizable | Contexto metodológico; no evidencia física |
| `docs/paper4_candidate_criteria.md` | Criterios Paper 4 | Excluye por sí solos R² alto, `einstein_score`, symbolic regression, embeddings, geometría effective matter-like y familia AdS-like | Documento normativo, no resultado | Sirve como filtro para descartar artefactos method-dominated |
| `docs/paper4_initial_architecture.md` | Arquitectura inicial Paper 4 | Define que scores/embeddings/familias geométricas sin trazabilidad física no cuentan como candidatos | Documento normativo, no resultado | Contexto de decisión |
| `README.md` | README de Fase 4 | Declara que mejoras de R² sin plausibilidad física y patrones de N pequeño no cuentan como discovery | Documento de alcance, no artefacto de análisis | Contexto de política de lenguaje |
| No encontrado bajo `docs/`, `runs_sync/`, `data/` o markdown raíz | Ausencia de resumen Route B/all18 ligero | No hay artefacto versionado disponible para usar como evidencia o contexto detallado Route B/all18 | Cualquier uso futuro exigiría localizar o versionar un resumen ligero antes de interpretarlo | Insuficiente para conclusión física; no reutilizable ahora |

## Documentation / protocol artifacts

| path | artifact type | physical use | limitation | reuse status |
|---|---|---|---|---|
| `README.md` | Scope operativo de Fase 4 | Define la pregunta central y los filtros contra discovery prematuro | No es una tabla de datos | Contexto obligatorio |
| `docs/paper4_initial_architecture.md` | Arquitectura inicial | Define depósito, objetivo, taxonomía mínima, condiciones de avance/cierre | No ejecuta ni valida análisis | Protocolo de decisión |
| `docs/paper4_candidate_criteria.md` | Criterios de candidato | Define input permitido, categorías y política de lenguaje | No clasifica casos concretos | Protocolo de clasificación |
| `docs/paper3_reporting_heterogeneity_matrix.md` | Matriz A/B/C/D/E Paper 3 | Protocolo para heterogeneidad de reporting y campos mínimos | Algunos estados quedan como TBD; no completa Fase 4 | Base metodológica para auditoría de input |
| `docs/paper3_GWTC4_table1_coverage_note.md` | Nota de cobertura GWTC-4 | Contexto de catálogo y cobertura | No reemplaza tabla primaria QNM | Contexto |
| `docs/paper3_GWTC4_table3_yaml_schema.md` | Schema documental | Define cómo interpretar el YAML Table 3 | No clasifica candidatos por sí mismo | Auditoría de input |
| `docs/paper3_capano2023_yaml_schema.md` | Schema documental | Define cómo interpretar el YAML Capano 2023 | No resuelve comparación estadística | Auditoría de input |
| `docs/paper3_source_A_prime_LVK_TGR_2021_reading.md` | Nota de fuente LVK/TGR | Contexto de baseline A/A' | No añade nuevos eventos por sí misma | Contexto metodológico |
| `docs/paper3_source_A_double_prime_GWTC4_remnants_reading.md` | Nota de fuente GWTC-4 Remnants | Contexto de fuente A'' y evolución de pipeline | Fuente posterior LVK, no independencia externa | Contexto para pipeline evolution |
| `docs/paper3_source_B_abs_capano2023_reading.md` | Nota de fuente Capano 2023 | Contexto de fuente externa/agnóstica para GW190521 | Un caso y etiquetas agnósticas | Auditoría de input/candidato documental |
| `docs/paper3_source_B_abs_isi2019_reading.md` | Nota de fuente Isi 2019 | Contexto de fuente publicada alternativa | No se observó aquí una tabla canónica lista para candidatos | Contexto |
| `docs/paper3_source_B_pyring_provenance.md` | Nota de provenance pyRing | Contexto de posible fuente B | No basta sin tabla QNM comparable | Contexto |
| `docs/paper3_source_cotesta2022_GW150914_reading.md` | Nota de fuente Cotesta 2022 | Contexto de GW150914/método publicado | No aparece como tabla canónica comparable en datos | Contexto |
| `docs/paper3_source_isi_farr_2021_methodology.md` | Nota metodológica | Contexto de metodología publicada | No produce candidato concreto | Contexto |
| `docs/paper3_source_siegel2023_GW190521_reading.md` | Nota de fuente Siegel 2023 | Contexto adicional para GW190521 | No basta sin tabla comparable en data | Contexto |
| `docs/paper3_literature_triage_notes.md` | Triage bibliográfico | Mapa de fuentes y prioridades | No es dataset de candidatos | Contexto |
| `docs/paper3_outline.md` | Outline Paper 3 | Contexto narrativo heredado | No es input físico | Contexto |

## Immediate conclusion

Con los artefactos existentes se puede responder sin rerun:

- qué inputs QNM publicados y trazables están ya versionados;
- qué dos casos de reporting heterogeneity heredados de Fase 3 pueden entrar en una matriz inicial de candidatos documentales;
- qué resultados Kerr/SNR previos existen como diagnósticos de sistemáticos y cobertura;
- qué artefactos tienen provenance/checksums suficientes para revisión documental;
- qué familias de scores, embeddings o geometrías deben descartarse como evidencia física por sí solas.

Con los artefactos existentes no se puede responder de forma defendible:

- si hay una tensión física Kerr robusta nueva;
- si un no-solapamiento aislado de `tau_ms` es discovery;
- si Route B/all18 o geometrías surrogate contienen evidencia física, porque no hay resumen ligero versionado bajo el alcance auditado;
- si una comparación multi-fuente completa sobrevive a errores asimétricos, redshift, sigma faltante y evolución de pipeline.

Una pregunta que exigiría rerun futuro es: dada una matriz cerrada de fuentes y convenciones, ¿sobrevive algún evento/modo a una comparación Kerr conservadora con incertidumbres observacionales y Kerr completas?

La pregunta que sí puede abrirse ahora, sin rerun, es: ¿qué casos existentes son solo `reporting_artifact`, `pipeline_evolution`, `input_dominated` o `method_dominated`, y cuáles merecen pasar a una matriz documental inicial de candidatos?
