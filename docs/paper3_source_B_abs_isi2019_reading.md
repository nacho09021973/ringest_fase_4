# Paper 3 — Source B_abs candidate: Isi et al. 2019

## Rol

Primer candidato para fuente `B_abs` focal en Paper 3.

Evento esperado:

- GW150914

## Fuente primaria pendiente

Isi et al., "Testing the no-hair theorem with GW150914", Phys. Rev. Lett. 123, 111102 (2019).

## Estado

No se ha creado YAML B.

No se ha transcrito ningún valor QNM.

Este documento existe para registrar la lectura primaria antes de decidir si la fuente entra como `B_abs`.

## Preguntas de lectura

La fuente primaria debe responder:

1. ¿Reporta valores absolutos de frecuencia en Hz?
2. ¿Reporta tiempos de damping en ms?
3. ¿Qué modo(s) identifica explícitamente: 220, 221 u otros?
4. ¿Las incertidumbres son simétricas o intervalos creíbles asimétricos?
5. ¿Las cantidades están en detector frame, source frame o no queda claro?
6. ¿El análisis usa sobretonos y desde qué tiempo de inicio?
7. ¿La tabla/texto permite construir una fila comparable con baseline A para GW150914?
8. ¿La fuente reporta también masa y spin remanente, o solo QNM?
9. ¿Hay data release suplementario que deba usarse en vez de copiar del texto?

## Criterio de aceptación como B_abs

Isi et al. 2019 entra como `B_abs` inicial solo si se puede documentar con fuente primaria:

- `event_id = GW150914`
- `source_paper`
- `mode`
- `f_hz`
- incertidumbre de frecuencia o intervalo creíble
- `tau_ms`
- incertidumbre de tau o intervalo creíble
- convención de marco
- notas sobre sobretonos / tiempo de inicio

## Decisión pendiente

Tras leer la fuente primaria, decidir:

- `accept_B_abs`: crear YAML mínimo para Isi/GW150914.
- `needs_more_provenance`: falta tabla/data release o convención.
- `reject_tabular`: no sirve como fuente tabular comparable.

## Lectura primaria — decisión

- Resultado: `reject_B_abs_for_now`.
- Clasificación provisional: `B_param_focal_GW150914`.
- Motivo: la fuente primaria no proporciona una tabla directa `f_hz/tau_ms` para el modo 220 comparable con baseline A.
- La información numérica útil identificada es parametrizada: `delta_f1`, `delta_tau1`, masa detector-frame y spin bajo hipótesis Kerr.
- `delta_f1`/`delta_tau1` corresponde al primer sobretono `n=1`, no al modo fundamental `n=0`.
- Por tanto, no se debe crear `data/phase1_data/qnm_events_isi2019.yml` con esquema absoluto.
- Si se usa Isi 2019 más adelante, debe ir a un esquema paramétrico separado, por ejemplo `qnm_events_isi2019_parametric.yml`, y solo tras definir formalmente la comparación en espacio de desviaciones.
- Estado final: `needs_more_provenance`.
