# Paper 3 — Source A_double_prime: GWTC-4.0 Remnants

## Rol

Fuente LVK posterior al baseline A para auditar heterogeneidad de reporting en resultados de remanentes.

No se clasifica como fuente B externa independiente.

## Fuente primaria

LVK, "GWTC-4.0: Tests of General Relativity. III. Tests of the Remnants", arXiv:2603.19021.

## Clasificación

`A_double_prime_LVK_O4a_remnants`

También puede describirse como:

`B_param_with_reconstructed_abs`

## Tablas relevantes

### Table 1

Lista los eventos analizados y qué pipelines aplican: PYRING, pSEOBNR, QNMRF y búsquedas de ecos.

### Table 3

Contiene resultados pSEOBNRV5PHM para eventos seleccionados:

- `delta_f220`
- `delta_tau220`
- `f220 [Hz]`
- `tau220 [ms]`
- `(1+z)Mf`
- `chi_f`
- valores IMR-GR entre paréntesis.

## Table 1 como matriz de cobertura

Table 1 se usará como matriz de cobertura metodológica: indica qué eventos entran en PYRING, pSEOBNR, QNMRF y búsquedas de ecos.

No se usará como tabla de valores QNM finales. Para valores `delta_f220`, `delta_tau220`, `f220` y `tau220`, la referencia tabular relevante es Table 3.

## Decisión

Esta fuente no debe entrar como B externa, porque es LVK.

Sí puede entrar como `A_double_prime` para comparar:

- baseline A;
- A_prime LVK/TGR 2021;
- A_double_prime GWTC-4.0 Remnants.

## Evento sugerido por informe externo

El informe bibliográfico proponía `GW190519_153544`.

La lectura primaria muestra que este evento aparece en Table 3, pero sus valores pSEOBNRV5PHM e IMR-GR parecen solapar razonablemente.

Valores:

| observable | pSEOBNRV5PHM | IMR-GR |
|---|---:|---:|
| f220 [Hz] | 121.7 +11.8/-14.3 | 127.9 +9.3/-8.6 |
| tau220 [ms] | 8.55 +4.75/-2.90 | 9.49 +1.84/-1.54 |

## Evento prioritario real

El evento más prometedor para un segundo caso de heterogeneidad es `GW190910_112807`.

Motivo:

- está en baseline A;
- aparece en Table 3;
- el texto primario señala que su damping time `tau220` está desplazado hacia valores mayores;
- los intervalos 90% de `tau220` entre pSEOBNRV5PHM e IMR-GR son marginalmente incompatibles;
- la frecuencia `f220` parece estable.

Valores:

| observable | pSEOBNRV5PHM | IMR-GR |
|---|---:|---:|
| delta_f220 | 0.01 +0.13/-0.10 | n/a |
| delta_tau220 | 0.61 +0.63/-0.50 | n/a |
| f220 [Hz] | 174.5 +12.2/-8.4 | 177.1 +8.3/-8.2 |
| tau220 [ms] | 9.49 +3.46/-2.82 | 5.83 +0.75/-0.55 |
| (1+z)Mf [Msun] | 123.2 +16.4/-19.6 | 96.1 +8.5/-7.1 |
| chi_f | 0.90 +0.05/-0.12 | 0.69 +0.07/-0.08 |

## Interpretación provisional

`GW190910_112807` parece un candidato fuerte para repetir el patrón observado en GW190521:

- frecuencia compatible o cercana;
- damping time desplazado;
- heterogeneidad de reporting, no tensión física.

## Decisión operativa

Siguiente caso a diseñar:

`GW190910_112807 baseline A vs GWTC-4.0 Remnants Table 3`

Antes de crear YAML o comparador, diseñar esquema para `A_double_prime` que preserve:

- fuente LVK;
- pipeline pSEOBNRV5PHM;
- delta_f220/delta_tau220;
- f220/tau220 reconstruidos;
- valores IMR-GR entre paréntesis;
- intervalos asimétricos;
- procedencia Table 3.

## YAML mínimo creado

- Ruta: `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`.
- Contiene solo `GW190910_112807`.
- Preserva `delta_f220`/`delta_tau220`, `f220`/`tau220` reconstruidos, valores IMR-GR entre paréntesis e intervalos asimétricos.
- No incluye todos los eventos de Table 3.
- No calcula residual contra baseline A.

## Estado

`ready_for_A_double_prime_schema_design`
