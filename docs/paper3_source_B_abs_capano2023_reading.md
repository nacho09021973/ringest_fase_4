# Paper 3 — Source B_abs candidate: Capano et al. 2023

## Rol

Candidato principal actual para fuente `B_abs` focal en Paper 3.

Evento esperado:

- GW190521

## Fuente primaria pendiente

Capano et al., "Multimode Quasinormal Spectrum from a Perturbed Black Hole", Phys. Rev. Lett. 131, 221402 (2023), arXiv:2105.05238.

## Estado

No se ha creado YAML B.

No se ha transcrito ningún valor QNM.

Este documento existe para registrar la lectura primaria antes de decidir si la fuente entra como `B_abs`.

## Preguntas de lectura

La fuente primaria debe responder:

1. ¿Reporta valores absolutos de frecuencia en Hz?
2. ¿Reporta tiempos de damping en ms?
3. ¿Qué evento(s) analiza explícitamente?
4. ¿Qué modo(s) identifica o asocia: 220, 221, 330 u otros?
5. ¿Las incertidumbres son simétricas, intervalos creíbles asimétricos o solo posterior plots?
6. ¿Las cantidades están en detector frame, source frame o no queda claro?
7. ¿El método es agnóstico/frequency-domain o impone relaciones Kerr?
8. ¿La tabla/texto permite construir una fila comparable con baseline A para GW190521?
9. ¿Hay material suplementario o data release que deba usarse antes que el texto principal?
10. ¿Los dos picos reportados, si existen, corresponden a modos físicos identificables o a resonancias agnósticas etiquetadas a posteriori?

## Criterio de aceptación como B_abs

Capano et al. 2023 entra como `B_abs` inicial solo si se puede documentar con fuente primaria:

- `event_id = GW190521`
- `source_paper`
- `mode` o etiqueta de resonancia agnóstica claramente mapeable
- `f_hz`
- incertidumbre de frecuencia o intervalo creíble
- `tau_ms`
- incertidumbre de tau o intervalo creíble
- convención de marco
- notas sobre identificación modal

## Decisión pendiente

Tras leer la fuente primaria, decidir:

- `accept_B_abs`: crear YAML mínimo para Capano/GW190521.
- `accept_B_abs_agnostic_labels`: crear YAML con etiquetas agnósticas si no hay modo Kerr inequívoco.
- `needs_more_provenance`: falta tabla/data release o convención.
- `reject_tabular`: no sirve como fuente tabular comparable.

## Lectura primaria — decisión

- Resultado: `accept_B_abs_agnostic_labels`.
- Evento: GW190521.
- Motivo: la fuente primaria proporciona valores absolutos de frecuencia y damping time para dos resonancias agnósticas, con identificación modal posterior compatible con `(2,2,0)` y `(3,3,0)`.
- Valores agnósticos verificados a `tref + 6 ms`:
  - Range A (modo primario): `f = 63 +2/-2 Hz`, `tau = 26 +8/-6 ms`.
  - Range B (modo secundario): `f = 98 +89/-7 Hz`, `tau = 40 +50/-30 ms`.
- Modelo Kerr `(220)+(330)`: Bayes factor `56 ± 1` a `tref + 6 ms` frente al modelo de un solo modo fundamental.
- Identificación modal: el modo secundario se interpreta como `(3,3,0)`, pero la entrada en YAML debe preservar la etiqueta agnóstica original (`range A` / `range B`) además de la identificación posterior.
- Cautela interpretativa externa: Siegel et al. 2023 discute una interpretación alternativa del subdominant feature como `320` y posiblemente relacionada con precesión. Esto no cambia el YAML Capano 2023, pero refuerza que `agnostic_range` y `kerr_identification = 330_candidate` deben conservarse como identificación posterior, no como verdad modal cerrada.
- Los intervalos son asimétricos (`+plus/-minus`); no se deben convertir a sigma simétrica sin una regla explícita documentada.
- Resultados paramétricos adicionales en el material suplementario:
  - `delta_f330 = -0.008 +0.081/-0.090`.
  - `delta_tau330 = 0.6 +1.9/-1.2`.
  - `f330 (1 + delta_f330) = 96.5 +8.5/-8.7 Hz`.
- Otros parámetros físicos reportados (no transcribir aún a YAML, dejar como referencia bibliográfica):
  - `(1+z) Mf = 330 +30/-40 Msun` (masa final redshifted).
  - `chi_f = 0.86 +0.06/-0.11`.
  - `A330/A220 = 0.2 +0.2/-0.1`.
- Estado final: `ready_for_yaml_design`. No se crea YAML todavía: antes hay que diseñar el esquema que preserve `agnostic_range`, etiqueta `mode_label` agnóstica, identificación modal posterior, tiempo de análisis (`analysis_time_offset_ms`) e intervalos asimétricos.

## YAML creado

- Ruta: `data/phase1_data/qnm_events_capano2023.yml`.
- Contiene únicamente el bloque absoluto agnóstico (range A y range B para GW190521) bajo el esquema documentado en `docs/paper3_capano2023_yaml_schema.md`.
- **No** contiene `parametric_tests`; `delta_f330` / `delta_tau330` quedan deliberadamente fuera por ahora.
- Los intervalos se preservan asimétricos (`f_hz_minus`/`f_hz_plus`, `tau_ms_minus`/`tau_ms_plus`); no se han convertido a sigma simétrica.
- No es una cohorte: es un estudio de caso de un único evento (GW190521) con dos resonancias agnósticas.
