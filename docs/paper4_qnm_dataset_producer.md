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

New Phase 4 path:

```text
02b_literature_to_dataset.py
```

## SHA256 verification

The inspected copies have matching SHA256 hashes:

```text
ccbd6372e4d41a66c37d81289e330fdd775cdd2439fb0ea2d8a26997cebf24eb  02b_literature_to_dataset.py
ccbd6372e4d41a66c37d81289e330fdd775cdd2439fb0ea2d8a26997cebf24eb  /home/ignac/RINGEST/02b_literature_to_dataset.py
ccbd6372e4d41a66c37d81289e330fdd775cdd2439fb0ea2d8a26997cebf24eb  /home/ignac/ringest_fase_1/scripts/02b_literature_to_dataset.py
```

The Phase 4 producer was therefore copied without changes.

## Command executed

```bash
python3 02b_literature_to_dataset.py \
  --sources data/phase1_data/qnm_events_literature.yml \
  --out runs/paper4_initial_qnm_dataset
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

`02b_literature_to_dataset.py` is the producer that reads literature QNM YAML and writes the pipeline-style QNM dataset artifacts.

## Limitations

This step generates the initial QNM dataset only.

It does not identify physical candidates, does not execute a full Kerr audit, does not run bridge, Stage 02, Stage 03 or Stage 04, and does not resolve reporting heterogeneity across independent sources.
