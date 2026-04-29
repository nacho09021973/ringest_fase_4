# Paper 4 — Release manifest

## Propósito del release

Empaquetar Fase 4 como release técnico reproducible para depósito tipo Zenodo. El release contiene:

- las tablas finales pequeñas, congeladas bajo `results/paper4_summary_tables/`;
- los scripts que las regeneran a partir de los CSV de input ya versionados en `runs/`;
- la documentación metodológica que las acompaña.

El release no introduce datos nuevos, no modifica los CSV de input y no reabre Fase 4 como discovery.

## Commit base

Commit base de Fase 4 antes del release:

```
6725c097f98643645594380a47b725be5f38c48a
```

(`git rev-parse HEAD` ejecutado el 2026-04-29 en `/home/ignac/ringest_fase_4`, antes del commit de release.)

## Scripts relevantes

- `tools/paper4_build_summary_tables.py` — generador único de las cinco tablas finales del release.
- `tools/paper4_frequency_sign_test.py` — test de signo del residual de frecuencia por dataset.
- `tools/paper4_frequency_sign_systematics.py` — auditoría de systematics aplicada al sign test.
- `tools/paper4_multisource_paired_comparison.py` — comparación pareada entre fuentes para eventos comunes.

## Documentos relevantes

- `docs/paper4_literature_context_systematic_biases.md`
- `docs/paper4_remnant_median_mapping_audit_plan.md`
- `docs/paper4_remnant_mapping_level1_status.md`
- `docs/paper4_posterior_samples_availability.md`
- `docs/paper4_outline.md`
- `docs/paper4_final_tables_manifest.md`
- `docs/paper4_deposit_decision.md`

## Inputs requeridos

- `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv` — GWTC-2 TGR IMR consolidado.
- `runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset_220.csv` — GWTC-4 pSEOBNR.

Ambos llevan `sigma_f_kerr_hz` y `kerr_sigma_source = propagated`, equivalente a level 1a remnant uncertainty propagada desde la mediana del remanente. El directorio `runs/` está gitignorado por convención del repo; estos CSV son los inputs canónicos del release y deben acompañar al depósito como tarball separado o como artefactos versionados aparte.

## Outputs congelados

Tablas finales versionadas bajo `results/paper4_summary_tables/`:

- `frequency_sign_summary.csv`
- `multisource_comparison.csv`
- `paired_common_events.csv`
- `methodological_verdict.json`
- `manifest.json`

`manifest.json` contiene los sha256 de los CSV de input usados en la regeneración y la lista exacta de outputs producidos por el script.

## Comando de regeneración

Desde la raíz del repo:

```
python3 tools/paper4_build_summary_tables.py
```

El script consume únicamente los dos CSV listados en "Inputs requeridos", reusa los JSON de sign-test ya presentes en `runs/` cuando existen, y reescribe los cinco outputs en `runs/paper4_summary_tables/`. Tras regenerar, los cinco archivos deben copiarse manualmente a `results/paper4_summary_tables/` para actualizar el snapshot versionado.

## Interpretación permitida

`methodological_systematics_limited`.

- No hay outliers individuales robustos frequency-only ≥ 2σ.
- Existe una asimetría positiva reproducible en `residual_f` multi-source: 14/16 positivos en GWTC-2 TGR IMR (p ≈ 0.00209) y 9/9 en GWTC-4 pSEOBNR (p ≈ 0.00195), con 5/5 eventos comunes manteniendo signo.
- La magnitud de la asimetría es compatible con los systematics conocidos del mapeo Kerr a nivel 1a.
- Gamma/damping queda systematic-limited y no se incluye como observable de auditoría en este release.

## Interpretaciones prohibidas

- Beyond-Kerr claim.
- Kerr violation / GR violation.
- New physics / discovery.
- Catálogo de candidatos beyond-Kerr.
- Population Kerr-violation claim.
- Reapertura de Fase 5 / O4 / GW250114 sobre la base de este release.

## Limitaciones explícitas

- Level 2 posterior samples pendiente. La auditoría actual usa summaries escalares y propagación level 1a; el cierre completo requiere posterior samples reales y queda explícitamente fuera de este release.
- Auditoría basada en escalar `residual_f`. No reemplaza un análisis de posterior conjunta sobre `(f, tau)`.
- Sin claim beyond-Kerr.
- Gamma/damping systematic-limited.

## Notas operativas

- `runs/` no se versiona; el release técnico se apoya exclusivamente en `results/paper4_summary_tables/` y en los scripts versionados bajo `tools/`.
- Cualquier regeneración futura debe registrar el commit del repo y el sha256 de los CSV de input. El propio `manifest.json` recoge ambos en cada ejecución.
- El presente manifest no autoriza tag ni push. Esos pasos requieren decisión separada.
