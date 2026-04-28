# Paper 3 — Source note: Cotesta et al. 2022 / GW150914

## Rol

Fuente metodológica para evaluar la robustez de la supuesta detección del overtone 221 en GW150914.

No se clasifica como fuente tabular de datos QNM para Paper 3.

## Fuente primaria

Cotesta, Carullo, Berti & Cardoso, "Analysis of Ringdown Overtones in GW150914", Phys. Rev. Lett. 129, 111102 (2022), arXiv:2201.00822.

## Clasificación

`No_tabular / methodological_GW150914`

Rol secundario:

`overtone_robustness_check`

## Hechos relevantes

- Evento principal: GW150914.
- Modelos comparados: `Kerr220` y `Kerr221`.
- El análisis usa pyRing.
- El resultado depende fuertemente del tiempo de inicio `t_start`.
- Para `Delta t_start/M >= -1.45`, el paper reporta `log10 B_221_220 < 0`.
- Para el tiempo usado por Isi et al. 2019, `Delta t_start/M = -0.72`, reporta `log10 B_221_220 = -0.60`.
- Cerca del pico, la amplitud del overtone `A1` conserva soporte significativo en cero.
- La Figura 2 muestra la variación de Bayes factors y amplitud `A1` con `t_start`.
- No hay una tabla propia `f_hz/tau_ms` observacional lista para poblar YAML.
- La mención a `Table I` se refiere a Table I de Giesler et al. 2019, no a una tabla propia de Cotesta et al. con observables QNM.

## Decisión para Paper 3

No crear YAML a partir de este paper.

Motivo:

- no proporciona tabla directa de `f_hz/tau_ms`;
- los resultados principales son Bayes factors, amplitud del overtone y sensibilidad al tiempo de inicio;
- transcribir posteriors desde figuras debilitaría la provenance;
- el paper es una fuente de robustez metodológica, no una fuente tabular absoluta.

## Impacto sobre GW150914

Este paper refuerza que GW150914 debe tratarse con cautela como caso de overtone.

No debe usarse para crear una fila `B_abs`.

Sí puede usarse para discutir heterogeneidad metodológica alrededor de:

- elección de `t_start`;
- evidencia del overtone 221;
- sensibilidad a ruido;
- diferencia entre soporte de amplitud y evidencia bayesiana.

## Estado

`no_yaml`
`methodological_context_only`
