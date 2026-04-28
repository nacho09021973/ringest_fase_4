# Paper 3 — GWTC-4.0 Remnants Table 3 YAML schema draft

## Propósito

Definir el esquema de datos para incorporar GWTC-4.0 Remnants Table 3 como fuente `A_double_prime_LVK_O4a_remnants`.

Este documento diseña el esquema. No contiene todavía el YAML de datos.

## Fuente

LVK, "GWTC-4.0: Tests of General Relativity. III. Tests of the Remnants", arXiv:2603.19021.

## Clasificación

`A_double_prime_LVK_O4a_remnants`

También puede describirse como:

`B_param_with_reconstructed_abs`

## Principio

Table 3 no debe forzarse al esquema plano de baseline A porque:

- es una fuente LVK posterior al baseline A;
- usa pSEOBNRV5PHM;
- reporta desviaciones fraccionales `delta_f220` y `delta_tau220`;
- reporta valores reconstruidos `f220` y `tau220`;
- incluye valores IMR-GR entre paréntesis;
- usa intervalos asimétricos;
- mezcla información paramétrica y reconstrucción absoluta.

## Ruta propuesta

El futuro YAML, si se crea, será:

`data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`

## Esquema propuesto

Una entrada por evento de Table 3:

```yaml
source_family: gwtc4_remnants
source_classification: A_double_prime_LVK_O4a_remnants
secondary_classification: B_param_with_reconstructed_abs
source_paper: "LVK, GWTC-4.0: Tests of General Relativity. III. Tests of the Remnants"
arxiv: "2603.19021"
table: "Table 3"
pipeline: pSEOBNRV5PHM
mode: "220"
events:
  - event_id: GW190910_112807
    delta_f220: 0.01
    delta_f220_minus: 0.10
    delta_f220_plus: 0.13
    delta_tau220: 0.61
    delta_tau220_minus: 0.50
    delta_tau220_plus: 0.63
    f220_hz: 174.5
    f220_hz_minus: 8.4
    f220_hz_plus: 12.2
    f220_imr_gr_hz: 177.1
    f220_imr_gr_hz_minus: 8.2
    f220_imr_gr_hz_plus: 8.3
    tau220_ms: 9.49
    tau220_ms_minus: 2.82
    tau220_ms_plus: 3.46
    tau220_imr_gr_ms: 5.83
    tau220_imr_gr_ms_minus: 0.55
    tau220_imr_gr_ms_plus: 0.75
    redshifted_Mf_Msun: 123.2
    redshifted_Mf_Msun_minus: 19.6
    redshifted_Mf_Msun_plus: 16.4
    redshifted_Mf_imr_gr_Msun: 96.1
    redshifted_Mf_imr_gr_Msun_minus: 7.1
    redshifted_Mf_imr_gr_Msun_plus: 8.5
    chi_f: 0.90
    chi_f_minus: 0.12
    chi_f_plus: 0.05
    chi_f_imr_gr: 0.69
    chi_f_imr_gr_minus: 0.08
    chi_f_imr_gr_plus: 0.07
    uncertainty_type: asymmetric_90_percent_credible_interval
    notes: "Table 3 pSEOBNRV5PHM result; IMR-GR values are those printed in parentheses in the source table."
```

## Campos obligatorios

- `event_id`
- `delta_f220`, `delta_f220_minus`, `delta_f220_plus`
- `delta_tau220`, `delta_tau220_minus`, `delta_tau220_plus`
- `f220_hz`, `f220_hz_minus`, `f220_hz_plus`
- `f220_imr_gr_hz`, `f220_imr_gr_hz_minus`, `f220_imr_gr_hz_plus`
- `tau220_ms`, `tau220_ms_minus`, `tau220_ms_plus`
- `tau220_imr_gr_ms`, `tau220_imr_gr_ms_minus`, `tau220_imr_gr_ms_plus`
- `redshifted_Mf_Msun`, `redshifted_Mf_Msun_minus`, `redshifted_Mf_Msun_plus`
- `redshifted_Mf_imr_gr_Msun`, `redshifted_Mf_imr_gr_Msun_minus`, `redshifted_Mf_imr_gr_Msun_plus`
- `chi_f`, `chi_f_minus`, `chi_f_plus`
- `chi_f_imr_gr`, `chi_f_imr_gr_minus`, `chi_f_imr_gr_plus`
- `uncertainty_type`
- `notes`

## Reglas de uso

- No convertir intervalos asimétricos a sigma simétrica en el YAML.
- No mezclar estos eventos dentro del YAML baseline A.
- No tratar esta fuente como B externa independiente.
- Preservar siempre los valores `delta_*` y los valores reconstruidos `f/tau`.
- Preservar siempre los valores IMR-GR entre paréntesis como campos separados.
- Preservar el pipeline `pSEOBNRV5PHM`.
- Usar `f220_hz` y `tau220_ms` como valores reconstruidos de Table 3, no como baseline A.
- Usar `delta_f220` y `delta_tau220` como cantidades paramétricas primarias de esta fuente.
- No calcular residual A vs A_double_prime dentro del YAML.
- No afirmar tensión física con Kerr a partir de este esquema.
- No comparar contra baseline A sin comparador permanente que trate intervalos asimétricos.

## Primer caso recomendado

El primer evento para poblar y comparar, si se crea el YAML después, será:

`GW190910_112807`

Motivo:

- pertenece al baseline A;
- aparece en Table 3;
- `f220` parece estable frente a IMR-GR;
- `tau220` aparece desplazado hacia valores mayores;
- el paper primario indica que los intervalos 90% de damping time son marginalmente incompatibles.

## Decisión pendiente

Antes de crear el YAML real, decidir si se incluye:

1. solo `GW190910_112807` como caso mínimo;
2. todos los eventos de Table 3 que pertenecen al baseline A;
3. todos los eventos de Table 3.

Recomendación provisional:

crear primero un YAML mínimo con `GW190910_112807`, validar comparador, y solo después ampliar.

## Estado

`schema_draft_only`
`no_yaml_created`
`ready_for_future_table3_yaml`
