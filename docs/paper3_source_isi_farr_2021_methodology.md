# Paper 3 — Source note: Isi & Farr 2021

## Rol

Fuente metodológica para análisis ringdown.

No se clasifica como fuente tabular de datos QNM para Paper 3.

## Fuente primaria

Isi & Farr, "Analyzing black-hole ringdowns", arXiv:2107.05609.

## Clasificación

`No_tabular / methodological_framework`

Rol secundario:

`supports_ringdown_methodology`

## Hechos relevantes

- Presenta un marco formal para análisis ringdown en dominio temporal.
- Discute la necesidad de una likelihood temporal no circulante para aislar datos post-truncation.
- Discute detectabilidad y resolubilidad de modos QNM.
- Presenta el paquete Python `ringdown`.
- Incluye simulaciones e inyecciones tipo GW150914.
- La Table I contiene parámetros inyectados de un ejemplo sintético, no valores observacionales medidos de GW150914.
- No proporciona una tabla primaria `f_hz/tau_ms` observacional lista para poblar YAML.

## Decisión para Paper 3

No crear YAML a partir de este paper.

Motivo:

- no es una fuente tabular observacional;
- la tabla relevante es de inyección/simulación;
- los valores de GW150914 que aparecen son comparaciones con resultados publicados en otros trabajos;
- usarlo como B_abs inflaría indebidamente la independencia de la fuente.

## Uso permitido

Puede citarse en Paper 3 para justificar:

- tratamiento cuidadoso de la truncación temporal;
- cautela con criterios de resolubilidad tipo Rayleigh;
- interpretación metodológica de overtones;
- necesidad de no convertir figuras o simulaciones en datos observacionales canónicos.

## Estado

`no_yaml`
`methodological_context_only`
