# Paper 4 — Initial QNM Input Diagnostic

## Scope

This diagnostic uses the existing pipeline and repository inputs only.

It does not run bridge, Stage 02, Stage 03 or Stage 04. It does not modify source data, YAML, README or configs. It does not discover candidates yet: it only records what canonical QNM input is available and which physical fields are missing or incomplete before any Kerr/candidate claim.

## Pre-run state

`git status --short` was clean before the first diagnostic action.

The requested path `data/qnm_events_literature.yml` does not exist in this Phase 4 workspace. The canonical local source is:

```text
data/phase1_data/qnm_events_literature.yml
```

`PIPELINE_ROUTES.md` is not present in this Phase 4 workspace.

`02b_literature_to_dataset.py` was not initially present in Phase 4. It was found in:

```text
/home/ignac/ringest_fase_1/scripts/02b_literature_to_dataset.py
/home/ignac/RINGEST/02b_literature_to_dataset.py
```

Both copies are byte-identical. The copy used here was brought into Phase 4 as:

```text
02b_literature_to_dataset.py
```

After the initial diagnostic, the Paper 4-specific producer was renamed and adapted as:

```text
02c_paper4_literature_to_dataset.py
```

The original provenance remains `/home/ignac/RINGEST/02b_literature_to_dataset.py`; the first run documented below was performed with the copied `02b_literature_to_dataset.py`.

## Command executed

The operational command executed in Phase 4 was:

```bash
python3 02b_literature_to_dataset.py \
  --sources data/phase1_data/qnm_events_literature.yml \
  --out runs/paper4_initial_qnm_dataset
```

The requested literal source path was adapted from `data/qnm_events_literature.yml` to the actual canonical Phase 4 path `data/phase1_data/qnm_events_literature.yml`. No YAML was modified.

## Outputs generated

```text
runs/paper4_initial_qnm_dataset/qnm_dataset.csv
runs/paper4_initial_qnm_dataset/qnm_dataset_220.csv
```

## Row/event/mode coverage

The script reported:

```text
rows total          : 19
is_220_candidate    : 16
theory-seed rows    : 0
literature rows     : 19
```

The source input therefore contains 19 literature QNM rows. The 220-filtered output contains 16 rows according to the producer's internal `is_220_candidate` criterion.

This is still a canonical input diagnostic. It is not an A/B/C/D/E reporting-heterogeneity matrix and it is not a candidate list.

An earlier fallback attempt used `scripts/paper3/build_baseline_a_coverage.py`, which can produce `baseline_a_coverage.csv`. That was the wrong or incomplete producer for this objective because it does not generate `qnm_dataset.csv`. The current `runs/paper4_initial_qnm_dataset` listing contains the two intended initial `02b_literature_to_dataset.py` outputs and no `baseline_a_coverage.csv`.

## Generated CSV columns

Both generated CSV files expose the same columns:

```text
event
ifo
pole_source
mode_rank
freq_hz
damping_hz
tau_ms
omega_re
omega_im
amp_abs
relative_rms
M_final_Msun
chi_final
z
M_final_detector_Msun
is_220_candidate
kerr_220_distance
kerr_220_chi_ref
omega_re_norm
omega_im_norm
sigma_freq_hz
sigma_damping_hz
sigma_M_final_Msun
sigma_chi_final
f_kerr_hz
gamma_kerr_hz
sigma_f_kerr_hz
sigma_gamma_kerr_hz
residual_f
residual_gamma
kerr_sigma_source
```

## Candidate-criteria fields present

| required field | status in generated CSV |
|---|---|
| event identifier | present as `event` |
| mode information | partially present as `mode_rank` and `is_220_candidate` |
| frequency | present as `freq_hz` |
| frequency uncertainty | present as `sigma_freq_hz` |
| damping time | present as `tau_ms` |
| damping rate | present as `damping_hz` |
| damping-rate uncertainty | present as `sigma_damping_hz` |
| final mass | present as `M_final_Msun` |
| final spin | present as `chi_final` |
| redshift | present as `z` |
| detector-frame final mass | present as `M_final_detector_Msun` |
| source declaration | present as `ifo` and `pole_source` |
| Kerr frequency prediction | present as `f_kerr_hz` |
| Kerr damping-rate prediction | present as `gamma_kerr_hz` |
| Kerr prediction uncertainties | present as `sigma_f_kerr_hz` and `sigma_gamma_kerr_hz` |
| preliminary residual columns | present as `residual_f` and `residual_gamma` |
| Kerr uncertainty provenance | present as `kerr_sigma_source` |

These fields are enough to audit the canonical baseline input and to identify which rows are mechanically Kerr-ready under the existing producer.

## Missing or incomplete fields before candidate claims

| field / requirement | status | consequence |
|---|---|---|
| explicit `event_id` column | absent; equivalent is `event` | Candidate matrix should normalize naming before review. |
| explicit mode label `l,m,n` or `220` | absent; only `mode_rank` and `is_220_candidate` are emitted | Modal identification is not fully auditable from this CSV alone. |
| A/B/C/D/E source family | absent | Reporting-heterogeneity class must be joined from Paper 3 docs/YAML. |
| multiple independent source support | absent | A candidate cannot be defended as source-robust from this output alone. |
| asymmetric uncertainty intervals | absent | Capano/GWTC-4 style asymmetric intervals are not represented. |
| frame/convention notes | absent | Detector/source-frame and convention checks still require source documentation. |
| pipeline/catalog evolution labels | absent | Pipeline-evolution classification must be added from documentation. |
| modal-label ambiguity | not represented | Agnostic labels and posterior identifications are outside this baseline table. |
| candidate classification | absent | No `consistent`, `tension`, `input_dominated` or `method_dominated` class is assigned here. |
| physical-candidate provenance bundle | incomplete | Table path, source paper, convention and uncertainty model still need a row-level review document. |

## Physical interpretation limit

This run answers an input question:

> What canonical QNM input does the repo expose today for Paper 4 diagnostics?

It does not answer:

> Is any event/mode a physical Kerr tension or discovery candidate?

The generated output includes Kerr predictions and residual columns from the existing producer, but this diagnostic does not interpret them as candidate evidence. Before any candidate claim, the rows must be audited against reporting heterogeneity, pipeline evolution, parameterization, modal-label ambiguity, redshift/frame conventions and uncertainty completeness.

## Recommended next step

Inspect the generated columns and required fields directly against `docs/paper4_candidate_criteria.md` before creating any candidate matrix.
