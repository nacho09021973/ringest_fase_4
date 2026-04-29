# Paper 4 — QNM Dataset Producer Provenance

## Script provenance

Producer copied from:

```text
/home/ignac/RINGEST/02b_literature_to_dataset.py
```

Equivalent copy found at:

```text
/home/ignac/ringest_fase_1/scripts/02b_literature_to_dataset.py
```

Initial Phase 4 path:

```text
02b_literature_to_dataset.py
```

Active Paper 4 path after the schema/provenance patch:

```text
02c_paper4_literature_to_dataset.py
```

## SHA256 verification

The inspected copies have matching SHA256 hashes:

```text
ccbd6372e4d41a66c37d81289e330fdd775cdd2439fb0ea2d8a26997cebf24eb  02b_literature_to_dataset.py
ccbd6372e4d41a66c37d81289e330fdd775cdd2439fb0ea2d8a26997cebf24eb  /home/ignac/RINGEST/02b_literature_to_dataset.py
ccbd6372e4d41a66c37d81289e330fdd775cdd2439fb0ea2d8a26997cebf24eb  /home/ignac/ringest_fase_1/scripts/02b_literature_to_dataset.py
```

The initial Phase 4 producer was therefore copied without changes. It was later renamed and adapted as `02c_paper4_literature_to_dataset.py` to materialize Paper 4 schema/provenance fields while preserving the original copy provenance.

## Command executed

The initial dataset run was executed before the Paper 4 rename:

```bash
python3 02b_literature_to_dataset.py \
  --sources data/phase1_data/qnm_events_literature.yml \
  --out runs/paper4_initial_qnm_dataset
```

The active producer for subsequent Paper 4 QNM dataset generation is:

```text
02c_paper4_literature_to_dataset.py
```

The source path used in Phase 4 is `data/phase1_data/qnm_events_literature.yml`.

## Real outputs

```text
runs/paper4_initial_qnm_dataset/qnm_dataset.csv
runs/paper4_initial_qnm_dataset/qnm_dataset_220.csv
```

The run artifacts under `runs/` are not meant to be added to normal git history unless a later explicit policy says so.

## Script summary

The producer reported:

```text
rows total          : 19
is_220_candidate    : 16
theory-seed rows    : 0
literature rows     : 19
```

The inspected files contain:

```text
20 runs/paper4_initial_qnm_dataset/qnm_dataset.csv
17 runs/paper4_initial_qnm_dataset/qnm_dataset_220.csv
```

The extra line in each file is the CSV header.

## Why this producer is needed

The earlier Phase 4 fallback used `scripts/paper3/build_baseline_a_coverage.py`, which is a Paper 3 coverage-table producer. It can write `baseline_a_coverage.csv`, but it is not the canonical producer for `qnm_dataset.csv`.

The copied `02b_literature_to_dataset.py` was the initial producer that read literature QNM YAML and wrote the pipeline-style QNM dataset artifacts. The active Paper 4-specific producer is now `02c_paper4_literature_to_dataset.py`.

## Limitations

This step generates the initial QNM dataset only.

It does not identify physical candidates, does not execute a full Kerr audit, does not run bridge, Stage 02, Stage 03 or Stage 04, and does not resolve reporting heterogeneity across independent sources.
