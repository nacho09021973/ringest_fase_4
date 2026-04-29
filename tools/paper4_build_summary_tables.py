#!/usr/bin/env python3
"""
Paper 4 — Build final summary tables.

This script consolidates existing Paper 4 scalar-summary outputs into final
regenerable tables. It consumes existing ``residual_f`` values only; it does
not recalculate Kerr predictions, Kerr sigmas, gamma residuals, or candidates.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional


SCRIPT_PATH = Path("tools/paper4_build_summary_tables.py")
OUT_DIR = Path("runs/paper4_summary_tables")

DATASETS = [
    {
        "dataset_id": "phase1_gwtc2_tgr_imr",
        "source_family": "GWTC-2 TGR IMR",
        "input_csv": Path("runs/paper4_qnm_dataset_schema_v2_renamed/qnm_dataset_220.csv"),
        "sign_summary_json": Path("runs/paper4_frequency_sign_test_v1/frequency_sign_test_summary.json"),
    },
    {
        "dataset_id": "gwtc4_pseobnr",
        "source_family": "GWTC-4 pSEOBNR",
        "input_csv": Path("runs/paper4_qnm_dataset_gwtc4_pseobnr_v1/qnm_dataset_220.csv"),
        "sign_summary_json": Path("runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/frequency_sign_test_summary.json"),
    },
]

PREVIOUS_OUTPUTS = [
    Path("runs/paper4_frequency_sign_test_v1/frequency_sign_test_summary.json"),
    Path("runs/paper4_frequency_sign_test_v1/frequency_sign_test_table.csv"),
    Path("runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/frequency_sign_test_summary.json"),
    Path("runs/paper4_frequency_sign_test_gwtc4_pseobnr_v1/frequency_sign_test_table.csv"),
    Path("runs/paper4_frequency_sign_systematics_v1/frequency_sign_systematics_summary.json"),
    Path("runs/paper4_multisource_paired_comparison_v1/paired_comparison_summary.json"),
    Path("runs/paper4_multisource_paired_comparison_v1/paired_common_events.csv"),
]

REQUIRED_COLUMNS = [
    "event",
    "event_id",
    "freq_hz",
    "sigma_freq_hz",
    "M_final_Msun",
    "sigma_M_final_Msun",
    "chi_final",
    "sigma_chi_final",
    "f_kerr_hz",
    "sigma_f_kerr_hz",
    "residual_f",
    "source_paper",
]


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _read_csv(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required input CSV: {path}")
    with path.open(newline="") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError(f"{path}: missing CSV header")
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise ValueError(f"{path}: missing required columns: {', '.join(missing)}")
    return rows


def _to_float(value: object, *, field: str, path: Path) -> float:
    try:
        x = float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        raise ValueError(f"{path}: field {field} is not numeric: {value!r}") from None
    if not math.isfinite(x):
        raise ValueError(f"{path}: field {field} is not finite: {value!r}")
    return x


def _binom_pmf(k: int, n: int) -> float:
    return math.comb(n, k) / (2**n)


def _binomial_p_at_least(k: int, n: int) -> float:
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return sum(_binom_pmf(j, n) for j in range(k, n + 1))


def _load_json(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    with path.open() as fh:
        return json.load(fh)


def _git_status_short() -> str:
    proc = subprocess.run(
        ["git", "status", "--short"],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return f"git status failed: {proc.stderr.strip()}"
    return proc.stdout


def _sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _summarize_dataset(dataset: dict, rows: List[Dict[str, str]]) -> dict:
    input_csv: Path = dataset["input_csv"]
    residuals = [_to_float(r["residual_f"], field="residual_f", path=input_csv) for r in rows]
    n_events = len(residuals)
    if n_events == 0:
        raise ValueError(f"{input_csv}: no rows found")
    n_positive = sum(1 for r in residuals if r > 0)
    n_abs_ge_2 = sum(1 for r in residuals if abs(r) >= 2.0)

    sign_summary = _load_json(dataset["sign_summary_json"])
    if sign_summary is not None:
        sign_p_value = sign_summary.get("p_one_sided_positive")
        p_value_convention = (
            f"{sign_summary.get('test', 'unknown')}; "
            f"one-sided positive; {sign_summary.get('zero_handling', 'zero handling unspecified')}"
        )
    else:
        sign_p_value = _binomial_p_at_least(n_positive, n_events)
        p_value_convention = (
            "exact_binomial_via_math_comb; one-sided positive; "
            "zeros counted as not-positive; computed by paper4_build_summary_tables.py"
        )

    return {
        "dataset_id": dataset["dataset_id"],
        "source_family": dataset["source_family"],
        "input_csv": str(input_csv),
        "n_events": n_events,
        "n_positive": n_positive,
        "fraction_positive": n_positive / n_events,
        "n_abs_residual_ge_2": n_abs_ge_2,
        "sign_p_value": sign_p_value,
        "p_value_convention": p_value_convention,
        "residual_column": "residual_f",
    }


def _write_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict]) -> None:
    fields = list(fieldnames)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field) for field in fields})


def _build_paired_common_events(
    phase1_rows: List[Dict[str, str]], gwtc4_rows: List[Dict[str, str]]
) -> List[dict]:
    phase1_by_event = {r["event_id"] or r["event"]: r for r in phase1_rows}
    gwtc4_by_event = {r["event_id"] or r["event"]: r for r in gwtc4_rows}
    common = sorted(set(phase1_by_event) & set(gwtc4_by_event))
    rows = []
    for event in common:
        r1 = _to_float(phase1_by_event[event]["residual_f"], field="residual_f", path=DATASETS[0]["input_csv"])
        r2 = _to_float(gwtc4_by_event[event]["residual_f"], field="residual_f", path=DATASETS[1]["input_csv"])
        s1 = _sign(r1)
        s2 = _sign(r2)
        rows.append(
            {
                "event": event,
                "residual_f_phase1": r1,
                "residual_f_gwtc4": r2,
                "sign_phase1": s1,
                "sign_gwtc4": s2,
                "sign_agrees": s1 == s2,
                "both_positive": s1 > 0 and s2 > 0,
            }
        )
    return rows


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    dataset_rows = {}
    summaries = []
    for dataset in DATASETS:
        rows = _read_csv(dataset["input_csv"])
        dataset_rows[dataset["dataset_id"]] = rows
        summaries.append(_summarize_dataset(dataset, rows))

    frequency_summary_path = OUT_DIR / "frequency_sign_summary.csv"
    _write_csv(
        frequency_summary_path,
        [
            "dataset_id",
            "input_csv",
            "n_events",
            "n_positive",
            "fraction_positive",
            "n_abs_residual_ge_2",
            "sign_p_value",
            "p_value_convention",
            "residual_column",
        ],
        summaries,
    )

    multisource_rows = []
    for s in summaries:
        multisource_rows.append(
            {
                "dataset_id": s["dataset_id"],
                "source_family": s["source_family"],
                "n_events": s["n_events"],
                "n_positive": s["n_positive"],
                "sign_pattern": f"{s['n_positive']}/{s['n_events']}_positive",
                "interpretation": "positive_sign_asymmetry_methodological_systematics_limited",
            }
        )
    multisource_path = OUT_DIR / "multisource_comparison.csv"
    _write_csv(
        multisource_path,
        ["dataset_id", "source_family", "n_events", "n_positive", "sign_pattern", "interpretation"],
        multisource_rows,
    )

    paired_rows = _build_paired_common_events(
        dataset_rows["phase1_gwtc2_tgr_imr"],
        dataset_rows["gwtc4_pseobnr"],
    )
    paired_path = OUT_DIR / "paired_common_events.csv"
    _write_csv(
        paired_path,
        [
            "event",
            "residual_f_phase1",
            "residual_f_gwtc4",
            "sign_phase1",
            "sign_gwtc4",
            "sign_agrees",
            "both_positive",
        ],
        paired_rows,
    )

    no_frequency_outlier_claim = all(s["n_abs_residual_ge_2"] == 0 for s in summaries)
    positive_sign_asymmetry_observed = all(s["n_positive"] > (s["n_events"] / 2.0) for s in summaries)
    verdict = {
        "no_frequency_outlier_claim": no_frequency_outlier_claim,
        "positive_sign_asymmetry_observed": positive_sign_asymmetry_observed,
        "damping_gamma_status": "systematics_limited",
        "remnant_mapping_level1a_status": "implemented_in_current_csv",
        "remnant_mapping_level2_status": "pending_posterior_samples",
        "interpretation": "methodological_systematics_limited",
        "forbidden_interpretation": [
            "beyond_kerr_claim",
            "candidate_catalogue",
            "population_kerr_violation_claim",
        ],
    }
    verdict_path = OUT_DIR / "methodological_verdict.json"
    with verdict_path.open("w") as fh:
        json.dump(verdict, fh, indent=2, sort_keys=False)
        fh.write("\n")

    output_paths = [
        frequency_summary_path,
        multisource_path,
        paired_path,
        verdict_path,
        OUT_DIR / "manifest.json",
    ]
    manifest = {
        "script": str(SCRIPT_PATH),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "inputs": [
            {"path": str(d["input_csv"]), "sha256": _sha256(d["input_csv"])}
            for d in DATASETS
        ],
        "previous_outputs_detected": [
            str(p) for p in PREVIOUS_OUTPUTS if p.exists()
        ],
        "outputs": [str(p) for p in output_paths],
        "git_status_short": _git_status_short(),
        "notes": [
            "Consumes existing residual_f values only.",
            "Does not recalculate f_kerr_hz.",
            "Does not recalculate sigma_f_kerr_hz.",
            "Does not recalculate or declare candidates.",
            "Gamma/damping is carried only as systematics_limited verdict context.",
            "Sign p-values reuse existing Paper 4 sign-test JSON files when present.",
        ],
    }
    manifest_path = OUT_DIR / "manifest.json"
    with manifest_path.open("w") as fh:
        json.dump(manifest, fh, indent=2, sort_keys=False)
        fh.write("\n")

    for path in output_paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
