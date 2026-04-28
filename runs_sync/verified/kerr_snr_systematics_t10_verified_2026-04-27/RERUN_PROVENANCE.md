# Verified run provenance

Date: 2026-04-27

Status:
- verified downstream analysis run from frozen input tables
- external catalog metadata treated as frozen input upstream of this run
- no numerical differences greater than 1e-12 were observed in downstream verification comparisons
- checksums are recorded below

Scope:
- snr_residual_* files are downstream SNR residual audit outputs
- snr_overlap_decomposition_* files are downstream overlap-decomposition outputs
- metadata acquisition from external catalog/API services is not part of this verified run

Notes:
- These artefacts support reproducibility of the tabulated analyses.
- They are not, by themselves, evidence for new physics.

## SHA256 files in this verified run

404a51f37fbe0c2d66287a96d6e46564894866d829fd468a4c8457dd39c8a771  snr_overlap_decomposition.csv
4d09a4c8c97b2f6002e5e6882387f2bc7b8a96d8324cb73ce563f930154df364  snr_overlap_decomposition_notes.md
ce1de9f6a03ee25d6e5d022a3ee9fc2fce343271f6e47d83f21aeb6331585d8b  snr_overlap_decomposition_summary.json
6438b93ec1e1d3cae5fc172595f7bb36b35e693a6a99727af314002364662317  snr_residual_audit_table.csv
94c3688d10dbfc2ed627d1b2e3ca984955589e5fabb1c9596e7e31e7edb5dc9a  snr_residual_notes.md
b4c0063cbd980bba4e59751a55d73a520378ac453eb6b9b3ec2ee1138902b287  snr_residual_summary.json
