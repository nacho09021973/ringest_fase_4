# Paper 4 — QNM Schema Patch

## Scope

This patch only materializes canonical Paper 4 schema and provenance fields that already exist in the YAML source or are already read by the QNM producer. It does not change physical values, Kerr formulas, residual definitions, thresholds, row filtering, or candidate criteria.

## Code change

`02c_paper4_literature_to_dataset.py` now emits these additional columns at the end of each CSV row:

| column | source |
|---|---|
| `event_id` | copied from the existing `event` value |
| `l` | copied from the YAML mode entry |
| `m` | copied from the YAML mode entry |
| `n` | copied from the YAML mode entry |
| `mode` | canonical string `f"{l}{m}{n}"` when `l`, `m`, and `n` exist |
| `sigma_tau_ms` | copied from the YAML mode entry |
| `source_paper` | same provenance text currently emitted as `pole_source` |

Existing columns are preserved. The patch separates raw YAML mode labels from the producer's existing internal defaults, so the emitted canonical fields reflect source metadata when present.

The active Paper 4 producer was originally copied from `/home/ignac/RINGEST/02b_literature_to_dataset.py`. The first Phase 4 dataset run used the copied `02b_literature_to_dataset.py`; after the schema/provenance patch, the active Paper 4 producer was renamed to `02c_paper4_literature_to_dataset.py` to avoid cross-phase provenance ambiguity.

## Command

```bash
python3 02b_literature_to_dataset.py \
  --sources data/phase1_data/qnm_events_literature.yml \
  --out runs/paper4_qnm_dataset_schema_v2
```

Renamed-producer verification command:

```bash
python3 02c_paper4_literature_to_dataset.py \
  --sources data/phase1_data/qnm_events_literature.yml \
  --out runs/paper4_qnm_dataset_schema_v2_renamed
```

## Outputs

- `runs/paper4_qnm_dataset_schema_v2/qnm_dataset.csv`
- `runs/paper4_qnm_dataset_schema_v2/qnm_dataset_220.csv`
- `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset.csv`
- `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv`

## Validation

| file | line count | data rows |
|---|---:|---:|
| `runs/paper4_qnm_dataset_schema_v2/qnm_dataset.csv` | 20 | 19 |
| `runs/paper4_qnm_dataset_schema_v2/qnm_dataset_220.csv` | 17 | 16 |
| `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset.csv` | 20 | 19 |
| `runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv` | 17 | 16 |

New-column coverage:

| file | `event_id` | `l` | `m` | `n` | `mode` | `sigma_tau_ms` | `source_paper` |
|---|---:|---:|---:|---:|---:|---:|---:|
| `qnm_dataset.csv` | 19/19 | 19/19 | 19/19 | 19/19 | 19/19 | 19/19 | 19/19 |
| `qnm_dataset_220.csv` | 16/16 | 16/16 | 16/16 | 16/16 | 16/16 | 16/16 | 16/16 |

The renamed-producer verification run under `runs/paper4_qnm_dataset_schema_v2_renamed` has the same complete coverage for these columns: 19/19 in `qnm_dataset.csv` and 16/16 in `qnm_dataset_220.csv`.

The producer reported the same row totals as the initial dataset run: 19 total rows and 16 rows passing the existing `is_220_candidate` filter.

## Non-changes

- Kerr formulas were not changed.
- Residual definitions were not changed.
- Thresholds were not changed.
- Candidate criteria were not changed.
- The `is_220_candidate` logic was not changed.
- Bridge, Stage 02, Stage 03, and Stage 04 were not executed.

## Next step

Audit whether schema v2 supports a first residual table by event, without declaring candidates.
