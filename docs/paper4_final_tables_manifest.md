# Paper 4 — Final Tables Manifest

## Scope

This document describes the final reproducible summary tables for Paper 4. The tables consolidate existing scalar-summary results and existing `residual_f` values. They do not add new physics, recalculate Kerr predictions, reopen candidate selection, or reinterpret the damping/gamma channel.

Regeneration command:

```bash
python3 tools/paper4_build_summary_tables.py
```

## Script

Permanent script:

```text
tools/paper4_build_summary_tables.py
```

Default output directory:

```text
runs/paper4_summary_tables/
```

The script uses only the Python standard library.

## Inputs

Primary inputs:

```text
runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv
runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset_220.csv
```

Previous Paper 4 outputs are detected and reused where they fix conventions:

```text
runs/paper4_frequency_sign_test_v1/frequency_sign_test_summary.json
runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/frequency_sign_test_summary.json
runs/paper4_multisource_paired_comparison_v1/paired_common_events.csv
runs/paper4_multisource_paired_comparison_v1/paired_comparison_summary.json
runs/paper4_frequency_sign_systematics_v1/frequency_sign_systematics_summary.json
```

If sign-test summary JSON files are available, the script uses their `p_one_sided_positive` values and records their convention. If they are unavailable, it computes only the same exact one-sided binomial sign summary from the existing `residual_f` signs and records that fallback convention in `manifest.json`.

## Outputs

The script writes:

```text
runs/paper4_summary_tables/frequency_sign_summary.csv
runs/paper4_summary_tables/multisource_comparison.csv
runs/paper4_summary_tables/paired_common_events.csv
runs/paper4_summary_tables/methodological_verdict.json
runs/paper4_summary_tables/manifest.json
```

## Table descriptions

### `frequency_sign_summary.csv`

One row per source dataset. Columns include:

- `dataset_id`;
- `input_csv`;
- `n_events`;
- `n_positive`;
- `fraction_positive`;
- `n_abs_residual_ge_2`;
- `sign_p_value`;
- `p_value_convention`;
- `residual_column`.

Inherited columns used from the input CSVs:

- `residual_f`;
- `freq_hz`;
- `sigma_freq_hz`;
- `M_final_Msun`;
- `sigma_M_final_Msun`;
- `chi_final`;
- `sigma_chi_final`;
- `f_kerr_hz`;
- `sigma_f_kerr_hz`;
- `source_paper`;
- `event` / `event_id`.

Interpretation: this table summarizes the already-documented frequency sign pattern and verifies whether any frequency-only residual reaches `|residual_f| >= 2`.

### `multisource_comparison.csv`

One row per source family. Columns include:

- `dataset_id`;
- `source_family`;
- `n_events`;
- `n_positive`;
- `sign_pattern`;
- `interpretation`.

Interpretation: this table records that the positive `residual_f` sign pattern is seen in both current source/pipeline choices. It is not a combined population p-value and should not be read as an independent-draw population claim.

### `paired_common_events.csv`

One row per common event between the two input CSVs. Columns include:

- `event`;
- `residual_f_phase1`;
- `residual_f_gwtc4`;
- `sign_phase1`;
- `sign_gwtc4`;
- `sign_agrees`;
- `both_positive`.

Interpretation: this table records cross-source sign persistence for common events using existing `residual_f` values. It does not compute a paired p-value.

### `methodological_verdict.json`

Machine-readable conservative verdict for the Paper 4 technical note. It records:

- no frequency-outlier claim status;
- positive sign-asymmetry status;
- damping/gamma status as `systematics_limited`;
- remnant mapping Level 1a status as implemented in current CSVs;
- Level 2 status as pending posterior samples;
- forbidden interpretations.

Interpretation: this JSON is a guardrail artifact for final writeup language.

### `manifest.json`

Regeneration manifest. It records:

- script path;
- UTC timestamp;
- input paths and SHA256 hashes;
- output paths;
- current `git status --short`;
- notes that Kerr predictions, Kerr sigmas, gamma residuals, and candidates are not recalculated.

## What is not recalculated

The summary-table script does not recalculate:

- `f_kerr_hz`;
- `sigma_f_kerr_hz`;
- `gamma_kerr_hz`;
- `residual_gamma`;
- candidate labels;
- source YAML;
- posterior samples;
- damping/gamma physical claims.

It consumes `residual_f` as already present in the input CSVs.

## Limitations

- The tables are based on published scalar summaries, not posterior samples.
- The sign p-values inherit the exact-binomial convention documented by the existing sign-test outputs.
- Source/pipeline independence is partial because remnant metadata provenance can overlap.
- The paired common-event table is descriptive only.
- Gamma/damping remains systematics-limited and is not used for candidate claims.
- Remnant median mapping is not fully resolved without posterior samples.

## Deposit gate

Before any deposit or release, the generated tables should be checked against the committed docs, the limitation language should remain explicit, and ambiguous untracked interpretive documents should be either committed intentionally or removed from the release scope.
