# Paper 3 — Source note: Siegel et al. 2023 / GW190521

## Rol

Fuente metodológica para interpretar GW190521 y contextualizar Capano et al. 2023.

No se clasifica como fuente tabular de datos QNM.

## Fuente primaria

Siegel, Isi & Farr, "The Ringdown of GW190521: Hints of Multiple Quasinormal Modes with a Precessional Interpretation", Phys. Rev. D 108, 064008 (2023), arXiv:2307.11975.

## Clasificación

`No_tabular / methodological_GW190521`

Rol secundario:

`interpretation_check_for_Capano2023`

## Hechos relevantes

- Evento principal: GW190521.
- Modelos discutidos: `{220}`, `{220,330}`, `{220,210}`, `{220,210,320}`.
- El paper encuentra que modelos con `{220,210}` pueden ser más consistentes con NRSur7dq4 que interpretaciones previas.
- El paper encuentra cierto soporte para incluir `{320}`.
- La interpretación propuesta vincula modos con `l != m` con posible precesión.
- La identificación del modo subdominante de Capano como `330` no queda cerrada; Siegel et al. argumentan que puede ser más consistente con `320`.

## Decisión para Paper 3

No crear YAML a partir de este paper.

Motivo:

- no hay tabla limpia `f_hz/tau_ms`;
- las cantidades relevantes están principalmente en figuras/posteriors;
- transcribir valores aproximados desde figuras introduciría provenance débil;
- para usarlo cuantitativamente habría que auditar el data release.

## Impacto sobre Capano 2023

Este paper no invalida el YAML Capano 2023.

Sí refuerza que `range B / 330_candidate` debe mantenerse como identificación posterior y no como modo Kerr medido de forma inequívoca.

## Estado

`no_yaml`
`methodological_context_only`
