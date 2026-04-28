# Paper 3 — Outline: reporting heterogeneity in QNM ringdown results

## Working title

Reporting heterogeneity in published ringdown/QNM measurements: a two-case audit from GWTC-2 to GWTC-4.0

## Core question

For the same gravitational-wave event and nominal ringdown mode, how stable are the reported QNM observables when the source, pipeline, parametrization or reporting convention changes?

## Main claim

Paper 3 does not claim a new physical deviation from Kerr or GR.

It claims that, in the audited cases, reporting heterogeneity is reproducible and traceable:

- `f_hz` remains compatible under a conservative interval-overlap criterion;
- `tau_ms` does not overlap across the compared reports.

## What the paper is not

This paper is not:

- a new QNM extraction from strain;
- an ESPRIT analysis;
- a claim of new physics;
- a Kerr violation claim;
- a population-level statistical test;
- a p-value or sigma-residual study;
- a discovery paper.

## Data architecture

### Baseline A

- LVK/TGR GWTC-2-derived baseline.
- 19 events.
- mode 220.
- artefact: `outputs/paper3/baseline_a_coverage.csv`.

### Source B: Capano 2023

- Event: GW190521.
- Classification: `B_abs_agnostic_labels`.
- Artefact: `data/phase1_data/qnm_events_capano2023.yml`.
- Role: external/semiindependent agnostic absolute source.

### Source A_double_prime: GWTC-4.0 Remnants Table 3

- Event used in current case study: GW190910_112807.
- Classification: `A_double_prime_LVK_O4a_remnants / B_param_with_reconstructed_abs`.
- Artefact: `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`.
- Role: later LVK parametric/reconstructed source, not an external B source.

### Coverage source: GWTC-4.0 Remnants Table 1

- Role: coverage/selection/elegibility matrix.
- Not a result table for QNM values.
- Useful for future expansion.

## Taxonomy

### A

Canonical baseline.

### A_prime

Internal LVK/TGR alternative reporting or decomposition.

### A_double_prime

Later LVK remnant analysis with changed model, catalogue, pipeline, parametrization or reporting convention.

### B_abs

Independent absolute source with direct `f_hz/tau_ms`.

### B_abs_agnostic_labels

Independent or semiindependent source with absolute `f/tau`, but original labels are agnostic and modal identification is posterior.

### B_param

Source reporting deviations, Bayes factors or parametric quantities rather than direct absolute QNM observables.

### No_tabular

Methodological or theoretical source not suitable for direct YAML/data ingestion.

## Method

Use a conservative interval-overlap audit.

For each case:

1. select the same event;
2. select the closest matching 220 or 220_candidate observable;
3. preserve source labels and provenance;
4. convert symmetric baseline uncertainties only to interval ranges;
5. preserve asymmetric intervals in secondary sources;
6. compute:
   - `delta_f_hz`;
   - `delta_tau_ms`;
   - `overlap_f_interval`;
   - `overlap_tau_interval`;
7. do not compute p-values or combined-sigma residuals.

## Case study 1 — GW190521

Comparison:

- baseline A / LVK-TGR GWTC-2, mode 220;
- Capano et al. 2023, range A / 220_candidate.

Artefacts:

- `data/phase1_data/qnm_events_capano2023.yml`
- `scripts/paper3/compare_gw190521_a_vs_capano2023.py`
- `outputs/paper3/gw190521_a_vs_capano2023_comparison.csv`
- `outputs/paper3/gw190521_a_vs_capano2023_comparison.md`
- `docs/paper3_case_study_GW190521_A_vs_Capano2023.md`

Result:

- `overlap_f_interval = True`
- `overlap_tau_interval = False`

Interpretation:

- evidence of reporting heterogeneity in `tau_ms`;
- no physical tension claim;
- Capano range B / 330_candidate remains outside this comparison because baseline A has no 330 entry.

## Case study 2 — GW190910_112807

Comparison:

- baseline A / LVK-TGR GWTC-2, mode 220;
- GWTC-4.0 Remnants Table 3 / pSEOBNRV5PHM, mode 220.

Artefacts:

- `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`
- `scripts/paper3/compare_gw190910_a_vs_gwtc4_table3.py`
- `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.csv`
- `outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.md`
- `docs/paper3_case_study_GW190910_A_vs_GWTC4_table3.md`

Result:

- `overlap_f_interval = True`
- `overlap_tau_interval = False`

Interpretation:

- second traceable case with the same qualitative pattern;
- not an external source;
- not a Kerr tension claim.

## Common pattern

Across the two audited cases:

- frequency is stable under the conservative interval-overlap criterion;
- damping time is not stable under the same criterion;
- `tau_ms` appears more sensitive to reporting convention, pipeline or parametrization than `f_hz`.

This is a documentary and methodological statement, not a population-level physical claim.

## Figures and tables

### Minimal Figure 1

Pipeline/provenance diagram:

Baseline A → case comparators → outputs → interpretation.

### Minimal Table 1

Taxonomy of source classes:

A, A_prime, A_double_prime, B_abs, B_abs_agnostic_labels, B_param, No_tabular.

### Minimal Table 2

Two-case result summary:

| Event | Comparison | Source class | f overlap | tau overlap |
|---|---|---|---|---|

### Optional Table 3

Bibliographic triage:

sources accepted, rejected, methodological-only.

## Discussion

Topics:

- why `tau_ms` is more fragile than `f_hz`;
- start-time sensitivity;
- damping-time sensitivity to noise tails;
- agnostic versus modal labels;
- LVK internal evolution from GWTC-2 to GWTC-4.0;
- why scarcity of clean external `B_abs` sources is itself a reporting result.

## Limitations

- only two audited cases;
- heterogeneous source classes;
- no direct strain reanalysis;
- no posterior-level density comparison;
- no p-values;
- no claim of physical inconsistency;
- no cohort-level inference.

## Conclusion

Paper 3 supports a narrow but defensible claim:

Published QNM/ringdown reporting is heterogeneous in a reproducible, provenance-preserving way. In the two audited cases, the frequency observable remains compatible under conservative interval overlap, while the damping-time observable does not.

## Next work

Before expanding conclusions:

1. optionally ingest more GWTC-4 Table 3 events;
2. optionally build a Table 1 coverage matrix;
3. only then consider whether a larger cohort result is justified.
