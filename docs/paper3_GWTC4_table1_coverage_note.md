# Paper 3 — GWTC-4.0 Remnants Table 1 coverage note

## Rol

Table 1 de GWTC-4.0 Remnants se trata como una matriz de cobertura metodológica.

No es una tabla de resultados QNM finales.

## Fuente primaria

LVK, "GWTC-4.0: Tests of General Relativity. III. Tests of the Remnants", arXiv:2603.19021.

## Qué contiene

Table 1 lista eventos de O1-O3 y O4a con:

- SNR;
- masa final redshifted `(1+z)Mf`;
- spin final `chi_f`;
- razón de masas `q`;
- cobertura de análisis ringdown:
  - pyRing;
  - pSEOBNR;
  - QNMRF;
- cobertura de análisis de ecos:
  - ADA;
  - BHP;
  - BW;
  - CWB.

## Uso para Paper 3

Table 1 permite estudiar heterogeneidad de cobertura:

- qué eventos del baseline A reaparecen en GWTC-4.0 Remnants;
- qué pipelines se aplican a cada evento;
- qué eventos tienen resultados previos LVK;
- qué eventos son excluidos de ciertos análisis;
- cómo la selección de eventos condiciona qué resultados pueden existir después en Table 2 o Table 3.

## Distinción con Table 3

| Tabla | Uso en Paper 3 |
|---|---|
| Table 1 | cobertura / selección / elegibilidad |
| Table 2 | resultados pyRing para O4a |
| Table 3 | resultados pSEOBNRV5PHM: `delta_f220`, `delta_tau220`, `f220`, `tau220`, `(1+z)Mf`, `chi_f` |

## Eventos baseline A visibles en Table 1

Registrar explícitamente que Table 1 incluye varios eventos del baseline A, entre ellos:

- GW150914
- GW170104
- GW170814
- GW170823
- GW190408_181802
- GW190512_180714
- GW190519_153544
- GW190521
- GW190521_074359
- GW190828_063405
- GW190910_112807

No transcribir todavía toda la tabla.

## Decisión

Table 1 se acepta como fuente de cobertura metodológica para Paper 3.

No se crea YAML todavía.

Antes de producir una matriz completa de cobertura baseline A vs GWTC-4.0, habría que diseñar un esquema o un CSV derivado mediante script permanente.

## Estado

`coverage_source_accepted`
`no_yaml`
`no_script_yet`
