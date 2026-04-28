# Verified run provenance

Date: 2026-04-27

Status:
- verified downstream analysis run from frozen input tables
- external catalog metadata treated as frozen input
- no numerical differences greater than 1e-12 were observed in downstream verification comparisons
- checksums are recorded below

Scope:
- population_metadata_* files are frozen external metadata inputs
- population_tail_* files are downstream analysis outputs
- metadata acquisition from external catalog/API services is not part of this verified run

Notes:
- These artefacts support reproducibility of the tabulated analyses.
- They are not, by themselves, evidence for new physics.

## SHA256 files in this verified run

b52ce4d0043844f07e541bc08e967dbd109e3dce4bd5fccbbb0121ee11e9f0a1  population_metadata_coverage.json
6da843896635f2c996049a3f20d1a615cd6ad14e7f7c5d2989851cb2f450f191  population_metadata_notes.md
eb7436e1db7f825e65706df6ccb818e86b64c443b04199fd689754b93804167a  population_metadata_table.csv
184a329fd127acf2492f6275fa0a61a02e6df9952f5e7d97ebec4802f61b1156  population_tail_notes.md
586686302ef7065957c73c1a00b89d90ed403f1ce609625e9064550bc1ccb484  population_tail_stats_table.csv
d25c73656f92f2ce73df6bbb5c889eafa5be661d468811c835d8f88105c95b63  population_tail_summary.json
