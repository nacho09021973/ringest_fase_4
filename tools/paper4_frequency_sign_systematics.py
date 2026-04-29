#!/usr/bin/env python3
"""
Paper 4 — Frequency residual sign systematics audit.

Reads the schema-aligned 220 dataset and the sign-test event table, then
audits possible systematic associations between the residual_f sign
asymmetry and physical/provenance variables.

Outputs descriptive statistics only:
- Pearson and Spearman correlations between ``residual_f``/``sign_f`` and
  numeric variables (``z``, ``M_final_Msun``, ``chi_final``,
  ``f_kerr_hz``, ``freq_hz``, ``sigma_freq_hz``, ``M_final_detector_Msun``).
- Per-sign means and standard deviations for numeric variables.
- Per-source counts (``source_paper``, ``pole_source``) split by sign.

No correlation p-values are produced; only point estimates. With N=16,
the audit is descriptive and small-N caveats apply.

The script does not recalculate ``f_kerr_hz`` or ``residual_f``; it
consumes them from the input CSV as-is.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Optional

import pandas as pd


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--input",
        required=True,
        help="Schema-aligned 220 CSV with residual_f and physical columns.",
    )
    p.add_argument(
        "--sign-table",
        required=True,
        help="Sign-test per-event table (event_id, residual_f, sign_f).",
    )
    p.add_argument(
        "--out-dir",
        required=True,
        help="Output directory; created if missing.",
    )
    return p.parse_args()


def _to_clean_pair(s1: pd.Series, s2: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame({"a": pd.to_numeric(s1, errors="coerce"),
                       "b": pd.to_numeric(s2, errors="coerce")}).dropna()
    return df


def pearson(s1: pd.Series, s2: pd.Series) -> tuple[Optional[float], int]:
    df = _to_clean_pair(s1, s2)
    n = int(len(df))
    if n < 2:
        return (None, n)
    a = df["a"]
    b = df["b"]
    am, bm = a.mean(), b.mean()
    var_a = ((a - am) ** 2).sum()
    var_b = ((b - bm) ** 2).sum()
    if var_a == 0 or var_b == 0:
        return (None, n)
    cov = ((a - am) * (b - bm)).sum()
    return (float(cov / math.sqrt(var_a * var_b)), n)


def spearman(s1: pd.Series, s2: pd.Series) -> tuple[Optional[float], int]:
    df = _to_clean_pair(s1, s2)
    n = int(len(df))
    if n < 2:
        return (None, n)
    ra = df["a"].rank(method="average")
    rb = df["b"].rank(method="average")
    return pearson(ra, rb)


def _none_if_nan(v):
    if v is None:
        return None
    try:
        return None if math.isnan(v) else float(v)
    except (TypeError, ValueError):
        return v


def main() -> int:
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    df_main = pd.read_csv(args.input)
    df_sign = pd.read_csv(args.sign_table)

    if "mode" in df_main.columns:
        df_220 = df_main[df_main["mode"].astype(str) == "220"].copy()
    else:
        df_220 = df_main.copy()

    df = df_220.merge(
        df_sign[["event_id", "sign_f"]],
        on="event_id",
        how="inner",
        suffixes=("", "_signtable"),
    )

    candidate_numeric = [
        "z", "M_final_Msun", "chi_final", "f_kerr_hz",
        "freq_hz", "sigma_freq_hz", "M_final_detector_Msun",
    ]
    numeric_vars = [c for c in candidate_numeric if c in df.columns]

    sign_f = df["sign_f"].astype(float)
    residual_f = df["residual_f"].astype(float)

    correlations = {}
    for col in numeric_vars:
        s = df[col]
        pr_rf, n_rf = pearson(residual_f, s)
        sp_rf, _ = spearman(residual_f, s)
        pr_sf, n_sf = pearson(sign_f, s)
        sp_sf, _ = spearman(sign_f, s)
        correlations[col] = {
            "n": n_rf,
            "pearson_residual_f": _none_if_nan(pr_rf),
            "spearman_residual_f": _none_if_nan(sp_rf),
            "pearson_sign_f": _none_if_nan(pr_sf),
            "spearman_sign_f": _none_if_nan(sp_sf),
        }

    numeric_rows = []
    for col, c in correlations.items():
        numeric_rows.append({
            "variable": col,
            "n": c["n"],
            "pearson_residual_f": c["pearson_residual_f"],
            "spearman_residual_f": c["spearman_residual_f"],
            "pearson_sign_f": c["pearson_sign_f"],
            "spearman_sign_f": c["spearman_sign_f"],
        })
    pd.DataFrame(numeric_rows).to_csv(
        os.path.join(args.out_dir, "frequency_sign_systematics_numeric.csv"),
        index=False,
    )

    by_sign_rows = []
    for col in numeric_vars:
        for sign_val in [-1, 1]:
            sub = df[df["sign_f"] == sign_val][col].dropna().astype(float)
            n_sub = int(len(sub))
            mean = float(sub.mean()) if n_sub > 0 else float("nan")
            std = float(sub.std(ddof=0)) if n_sub > 0 else float("nan")
            by_sign_rows.append({
                "variable": col,
                "sign": int(sign_val),
                "n": n_sub,
                "mean": _none_if_nan(mean),
                "std": _none_if_nan(std),
            })
    pd.DataFrame(by_sign_rows).to_csv(
        os.path.join(args.out_dir, "frequency_sign_systematics_by_sign.csv"),
        index=False,
    )

    src_cols = [c for c in ["source_paper", "pole_source"] if c in df.columns]
    source_rows = []
    source_uniqueness = {}
    for col in src_cols:
        unique_vals = sorted(map(str, df[col].dropna().unique()))
        source_uniqueness[col] = {
            "n_unique": len(unique_vals),
            "values_preview": unique_vals[:5],
        }
        for sign_val in [-1, 1]:
            sub = df[df["sign_f"] == sign_val]
            counts = sub[col].astype(str).value_counts(dropna=False).to_dict()
            for val, n in counts.items():
                source_rows.append({
                    "column": col,
                    "sign": int(sign_val),
                    "value": str(val),
                    "n": int(n),
                })
    pd.DataFrame(source_rows).to_csv(
        os.path.join(args.out_dir, "frequency_sign_systematics_sources.csv"),
        index=False,
    )

    largest = []
    for col, c in correlations.items():
        for metric in [
            "pearson_residual_f", "spearman_residual_f",
            "pearson_sign_f", "spearman_sign_f",
        ]:
            v = c.get(metric)
            if v is None:
                continue
            largest.append({
                "variable": col,
                "metric": metric,
                "value": float(v),
                "abs_value": abs(float(v)),
            })
    largest.sort(key=lambda r: r["abs_value"], reverse=True)

    summary = {
        "input": args.input,
        "sign_table": args.sign_table,
        "n_rows": int(len(df)),
        "n_positive": int((df["sign_f"] > 0).sum()),
        "n_negative": int((df["sign_f"] < 0).sum()),
        "numeric_variables_audited": numeric_vars,
        "correlations": correlations,
        "largest_abs_correlations": largest[:5],
        "source_uniqueness": source_uniqueness,
        "p_value_note": (
            "Correlation p-values are NOT computed. Only Pearson/Spearman "
            "point estimates are reported. With N=16, moderate |r| can "
            "occur under any null and the audit is descriptive."
        ),
    }

    summary_path = os.path.join(args.out_dir, "frequency_sign_systematics_summary.json")
    with open(summary_path, "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=False)
        fh.write("\n")

    print(json.dumps(summary, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
