# Paper 4 Candidate Criteria

## 1. Propósito

Este documento define qué cuenta y qué no cuenta como candidato defendible en RINGEST Fase 4 / Paper 4.

Fase 4 es una exploración de candidatos, no una confirmación. Ningún caso debe presentarse como detección, evidencia fuerte o nueva física sin una justificación posterior que sobreviva a auditoría de input, sistemáticos y consistencia Kerr.

## 2. Input permitido

El input permitido se limita a observables QNM publicados o tablas ya trazables dentro del repo.

La metadata física mínima necesaria incluye:

- `event_id`;
- `mode`;
- `f_hz`;
- `sigma_f_hz`;
- `tau_ms` o `gamma_hz`;
- `M_final`;
- `chi_final`;
- `redshift`, si aplica.

No se debe usar extracción propia desde strain como fuente principal para definir candidatos en esta fase.

## 3. Candidato defendible

Un evento/modo solo puede tratarse como candidato defendible si cumple:

- modo identificado de forma trazable;
- comparación Kerr definida;
- unidades y convenciones claras;
- errores observacionales presentes o ausencia marcada explícitamente;
- metadata de masa/spin final suficientemente documentada;
- la tensión no depende obviamente de una convención, redshift, unidad o sigma faltante;
- `N` y fuente declarados.

## 4. Categorías de clasificación

Cada caso debe recibir una clasificación explícita:

| Categoría | Uso operativo |
|---|---|
| `consistent` | Compatible con Kerr y con los sistemáticos conocidos. |
| `marginal` | Señal débil o ambigua que requiere más documentación antes de interpretarse. |
| `tension` | Tensión aparente con input suficiente para discusión conservadora. |
| `strong_tension` | Tensión aparente robusta frente a auditoría mínima de input y sistemáticos. |
| `no_data` | Falta información necesaria para clasificar. |
| `input_dominated` | El resultado depende principalmente de la fuente, metadata, errores o convención de entrada. |
| `method_dominated` | El resultado depende principalmente del método de análisis o parametrización. |

## 5. No candidatos

No son candidatos por sí solos:

- R² alto;
- `einstein_score` alto;
- symbolic regression compacta;
- embedding sugerente;
- geometría effective matter-like;
- familia AdS-like;
- tensión Kerr calculada con errores incompletos y presentada como física.

## 6. Criterio de avance

Fase 4 solo debe avanzar si hay candidatos que sobreviven a una auditoría mínima de input y sistemáticos.

Si no hay candidatos robustos, el objetivo pasa a ser buscar una conclusión metodológica clara.

Si tampoco hay conclusión metodológica clara, Fase 4 no se deposita y el proyecto público queda cerrado en Fase 3.

## 7. Política de lenguaje

Usar:

- candidato;
- tensión aparente;
- input-dominated;
- method-dominated.

Evitar:

- detección;
- evidencia fuerte;
- nueva física.

Estas expresiones solo deben usarse si una justificación posterior las hace defendibles.
