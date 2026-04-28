# Paper 2 analysis producers

This directory contains the versioned analysis producers used for the Paper 2 reproducibility package.

The scripts operate on frozen input tables and write the corresponding analysis outputs. External catalog metadata should be treated as frozen inputs before downstream statistical analyses.

## Scripts

1. `01_build_population_metadata.py`
   - builds the population metadata table and metadata coverage artefacts.

2. `02_build_population_tail_statistics.py`
   - computes population-tail statistics, including Mahalanobis distance, Spearman rank tests, permutation tests, Theil-Sen slopes, and leave-one-out diagnostics.

3. `03_audit_snr_residuals.py`
   - audits the relation between network SNR and Kerr residuals.

4. `04_patch_snr_residual_interpretation.py`
   - updates the interpretation fields/notes for the SNR residual audit outputs.

5. `05_decompose_snr_overlap.py`
   - decomposes residual changes into overlap-analysis groups.

6. `06_patch_overlap_interpretation.py`
   - updates the interpretation fields/notes for the overlap-decomposition outputs.

## Notes

These scripts are included to make the tabulated analyses reproducible. They do not, by themselves, establish evidence for new physics.
