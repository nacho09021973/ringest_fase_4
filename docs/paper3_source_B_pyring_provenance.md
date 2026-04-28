# Paper 3 — Source B pyRing provenance

## Rol

Fuente B candidata para auditar reporting heterogeneity frente al baseline A LVK/TGR GWTC-2.

## Fuente candidata principal

Fuente B candidata: pyRing-related Carullo literature. La fuente tabular exacta queda pendiente de identificación.

Referencias relevantes, separadas para evitar confusión bibliográfica:

- Carullo et al., *Phys. Rev. D* **98**, 104020 (2018) — *Empirical tests of the black hole no-hair conjecture using gravitational-wave observations*; referencia del test de no-hair / parametrized ringdown.
- G. Carullo, *Phys. Rev. D* **103**, 124043 (2021) — *parametrized ringdown spin expansion coefficients formalism*; trabajo distinto al anterior.

Aún no está confirmado que ninguna de las dos referencias contenga una tabla directamente convertible a `f_hz` / `tau_ms` por evento y modo. Eso es exactamente lo que debe resolverse antes de crear el YAML de fuente B.

## Estado

No se ha creado todavía `data/phase1_data/qnm_events_pyring.yml`.

No se ha transcrito ningún valor QNM.

El solape real A/B permanece desconocido hasta extraer una lista explícita de `event_id` desde la fuente B.

## Justificación metodológica

pyRing es metodológicamente distinto del baseline A: análisis bayesiano de ringdown post-merger, con likelihood temporal, modelos de ringdown y tests parametrizados de GR sobre frecuencias y damping times.

## Preguntas que deben resolverse antes de crear el YAML

1. ¿La fuente reporta valores absolutos de `f` y `tau`, o solo desviaciones fraccionales respecto a Kerr?
2. ¿Las incertidumbres son simétricas o intervalos creíbles asimétricos?
3. ¿Las cantidades están en marco detector, marco fuente o unidades geométricas?
4. ¿El damping se reporta como `tau`, `gamma`, `omega_I` o `Q`?
5. ¿Qué eventos del baseline A aparecen realmente?
6. ¿Qué modo se reporta: 220, overtone 221, modos superiores u otro parametrizado?
7. ¿La tabla permite una fila comparable `event_id + mode + f_hz + tau_ms`?
8. ¿Hace falta transformar desviaciones fraccionales usando Kerr(M_final, chi_final)?

## Criterio para aceptar pyRing como fuente B

pyRing entra como fuente B principal solo si puede producirse una tabla trazable con:

- `event_id`
- `source_paper`
- `mode`
- `f_hz` o una transformación explícita hacia `f_hz`
- `sigma_f_hz` o intervalo convertible
- `tau_ms` o una transformación explícita hacia `tau_ms`
- `sigma_tau_ms` o intervalo convertible
- notas claras de convención

## Decisión pendiente

Leer la fuente exacta y decidir si pyRing proporciona observables absolutos directamente comparables con baseline A o si solo permite una comparación en espacio de desviaciones parametrizadas.

## Hipótesis actual sobre comparabilidad

- pyRing es válido como fuente metodológica candidata para Paper 3.
- La vía más probable de entrada no es una tabla directa `f_hz/tau_ms`, sino reporting parametrizado en desviaciones de frecuencia y damping time (`delta_f`, `delta_tau`).
- Antes de crear `data/phase1_data/qnm_events_pyring.yml`, hay que decidir si Paper 3 comparará:
  1. observables absolutos `f_hz/tau_ms`; o
  2. desviaciones fraccionales respecto a Kerr; o
  3. ambas, si la fuente permite transformar unas en otras con provenance.
- PRD 103, 124043 (2021) debe tratarse como candidato de eventos/desviaciones, no como fuente tabular absoluta hasta leer la tabla exacta (presumiblemente Table II, pendiente de verificar).
- Si pyRing solo reporta desviaciones parametrizadas, el YAML B no debe forzarse al esquema de baseline A sin una transformación explícita y documentada.

## Decisión pendiente antes de YAML B

La siguiente decisión científica es si la matriz A/B/C/D/E comparará fuentes en espacio de observables físicos absolutos (`f_hz`, `tau_ms`) o en espacio de desviaciones parametrizadas (`delta_f`, `delta_tau`). No se debe crear el YAML B hasta cerrar esta decisión para pyRing.

## Próxima lectura obligatoria

Antes de crear `data/phase1_data/qnm_events_pyring.yml`, hay que leer la tabla exacta de la fuente pyRing-related candidata.

Prioridad de lectura:

1. G. Carullo, *Phys. Rev. D* **103**, 124043 (2021), especialmente Table II si contiene los eventos incluidos en el análisis de desviaciones de frecuencia y damping time.
2. Carullo et al., *Phys. Rev. D* **98**, 104020 (2018), si contiene observables o parametrizaciones comparables.
3. Documentación/publicaciones pyRing solo como soporte metodológico, no como fuente tabular de valores QNM.

La lectura debe responder:

- ¿La tabla contiene valores absolutos de frecuencia y damping time?
- ¿O contiene desviaciones fraccionales respecto a Kerr?
- ¿Qué eventos aparecen?
- ¿Qué modos aparecen?
- ¿Qué incertidumbres aparecen?
- ¿Las incertidumbres son simétricas o intervalos creíbles?
- ¿La tabla permite construir `qnm_events_pyring.yml` con el mismo esquema que baseline A?
- Si no permite el mismo esquema, ¿hace falta un esquema B_param separado?

Hasta completar esta lectura, fuente B queda en estado `candidate_methodological`, no `candidate_tabular`.
