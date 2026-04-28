# Paper 3 — Source A_prime: LVK/TGR PRD 103, 122002

## Rol

Fuente interna LVK/TGR para auditar heterogeneidad de reporting dentro del propio ecosistema que alimenta baseline A.

No se clasifica como fuente B externa independiente.

## Fuente primaria

Abbott et al., "Tests of general relativity with binary black holes from the second LIGO-Virgo gravitational-wave transient catalog", Phys. Rev. D 103, 122002 (2021), arXiv:2010.14529.

## Clasificación

`A_prime_internal_LVK_TGR`

También puede describirse como:

`A_prime_abs_and_param`

## Tablas relevantes

### Tabla VIII

Contiene estimaciones de masa final redshifted y spin final para IMR, Kerr220, Kerr221 y KerrHM, además de Bayes factors para higher modes / overtones y odds modified-GR.

Uso potencial: rama paramétrica o diagnóstico interno de modelos ringdown.

### Tabla IX

Contiene frecuencia redshifted [Hz] y damping time redshifted [ms] para IMR, DS y pSEOB.

Uso potencial: auditoría directa de heterogeneidad interna en `f_hz` y `tau_ms`.

## Decisión

Este paper no debe entrar como fuente B externa porque pertenece al mismo marco LVK/TGR del baseline A.

Sí debe entrar como `A_prime`, para separar:

- baseline A canónico;
- reporting interno alternativo LVK/TGR;
- fuentes B/C/D/E externas como Capano 2023.

## Ejemplo GW190521

Tabla IX reporta para GW190521:

| pipeline | f_hz | tau_ms |
|---|---:|---:|
| IMR | 68 +4/-4 | 15.8 +3.9/-2.5 |
| DS | 65 +3/-3 | 22.3 +12.6/-7.5 |
| pSEOB | 67 +2/-2 | 30.7 +7.7/-7.4 |

Este ejemplo sugiere que la frecuencia es relativamente estable entre pipelines, mientras que el damping time muestra heterogeneidad fuerte.

## Cautela

Esto no es una tensión física con Kerr.

Esto no es fuente externa independiente.

Esto no debe mezclarse con Capano 2023 sin preservar la etiqueta de procedencia.

## Próxima decisión

Diseñar si Paper 3 incorporará un YAML separado para A_prime, por ejemplo:

`data/phase1_data/qnm_events_lvk_tgr_2021_table_ix.yml`

antes de generar comparadores adicionales.
