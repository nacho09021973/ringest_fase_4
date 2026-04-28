# Paper 3 — Capano 2023 YAML schema draft

## Propósito

Definir el esquema de datos para incorporar Capano et al. 2023 / GW190521 como fuente `B_abs_agnostic_labels`.

Este documento diseña el esquema. No contiene todavía el YAML de datos.

## Principio

Capano 2023 no debe forzarse al esquema plano de baseline A porque:

- la extracción primaria es agnóstica por rangos de frecuencia;
- la identificación como `(220)` y `(330)` es posterior;
- los intervalos son asimétricos;
- el análisis depende del tiempo `tref + 6 ms`;
- existe una capa paramétrica adicional para desviaciones Kerr.

## Ruta propuesta

El futuro YAML, si se crea, será:

`data/phase1_data/qnm_events_capano2023.yml`

## Esquema propuesto

Una entrada por resonancia agnóstica:

```yaml
source_family: capano2023
source_classification: B_abs_agnostic_labels
source_paper: "Capano et al., Phys. Rev. Lett. 131, 221402 (2023)"
doi: "10.1103/PhysRevLett.131.221402"
arxiv: "2105.05238"
event_id: GW190521
analysis_reference_time_gps: 1242442967.445
analysis_time_offset_ms: 6
agnostic_range: A
agnostic_frequency_range_hz: [50, 80]
mode_label_original: range_A_primary
kerr_identification: "220_candidate"
identification_status: posterior_consistent_with_kerr_mode
f_hz: 63
f_hz_minus: 2
f_hz_plus: 2
tau_ms: 26
tau_ms_minus: 6
tau_ms_plus: 8
uncertainty_type: asymmetric_credible_interval
frame: detector
notes: "Agnostic range A; interpreted posteriorly as compatible with the Kerr (2,2,0) mode."
```

Para range B, el mismo esquema con:

- `agnostic_range: B`
- `agnostic_frequency_range_hz: [80, 256]`
- `mode_label_original: range_B_secondary`
- `kerr_identification: "330_candidate"`

## Bloque paramétrico opcional

Si se decide registrar los resultados de no-hair test, deben ir en un bloque separado, por ejemplo:

```yaml
parametric_tests:
  - test_name: delta_330
    model: "Kerr (220)+(330)"
    analysis_time_offset_ms: 6
    delta_f330: -0.008
    delta_f330_minus: 0.090
    delta_f330_plus: 0.081
    delta_tau330: 0.6
    delta_tau330_minus: 1.2
    delta_tau330_plus: 1.9
    modified_f330_hz: 96.5
    modified_f330_hz_minus: 8.7
    modified_f330_hz_plus: 8.5
    uncertainty_type: asymmetric_credible_interval
```

## Reglas

- No convertir intervalos asimétricos a sigmas simétricas en este YAML.
- No mezclar resonancias agnósticas y tests paramétricos en la misma fila.
- No llamar `mode = 330` sin preservar `agnostic_range = B`.
- No comparar directamente con baseline A sin una función explícita de comparación que entienda intervalos asimétricos.
- No usar este YAML para afirmar cohorte; es un estudio de caso GW190521.

## Decisión pendiente

Antes de crear el YAML real, decidir si se incluye solo el bloque absoluto agnóstico o también el bloque paramétrico `delta_330`.
