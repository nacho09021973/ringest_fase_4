#!/usr/bin/env python3
"""
Paper 4 — Multi-source paired comparison (descriptive).

Reads two schema-aligned 220 datasets (phase1/GWTC-2 TGR IMR and
GWTC-4 pSEOBNR), inner-joins them on ``event_id``, and produces a
descriptive paired comparison of ``residual_f`` and ``f_hz`` across
pipelines.

The script does not recalculate ``f_kerr_hz`` or ``residual_f``; it
consumes them from the inputs as-is. It does not compute paired
p-values: with n_common likely ≤ 6 and partial source dependence
(remnant metadata shares GWOSC PE provenance), only descriptive
statistics are produced.

Outputs:
- ``paired_common_events.csv``: per-event side-by-side comparison.
- ``paired_comparison_summary.json``: counts and median deltas.
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
        "--phase1",
        required=True,
        help="Phase 1 schema-aligned 220 CSV (GWTC-2 TGR IMR baseline).",
    )
    p.add_argument(
        "--gwtc4",
        required=True,
        help="GWTC-4 pSEOBNR schema-aligned 220 CSV.",
    )
    p.add_argument(
        "--out-dir",
        required=True,
        help="Output directory; created if missing.",
    )
    return p.parse_args()


def _sign(value: Optional[float]) -> Optional[int]:
    if value is None:
        return None
    try:
        if math.isnan(value):
            return None
    except TypeError:
        return None
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _none_if_nan(v):
    if v is None:
        return None
    try:
        return None if math.isnan(float(v)) else float(v)
    except (TypeError, ValueError):
        return v


def main() -> int:
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    df1 = pd.read_csv(args.phase1)
    df2 = pd.read_csv(args.gwtc4)

    if "mode" in df1.columns:
        df1 = df1[df1["mode"].astype(str) == "220"].copy()
    if "mode" in df2.columns:
        df2 = df2[df2["mode"].astype(str) == "220"].copy()

    keep1 = ["event_id", "mode", "residual_f", "freq_hz", "sigma_freq_hz",
             "f_kerr_hz", "source_paper"]
    keep2 = ["event_id", "mode", "residual_f", "freq_hz", "sigma_freq_hz",
             "f_kerr_hz", "source_paper"]
    df1 = df1[[c for c in keep1 if c in df1.columns]].copy()
    df2 = df2[[c for c in keep2 if c in df2.columns]].copy()

    merged = df1.merge(
        df2,
        on="event_id",
        how="inner",
        suffixes=("_phase1", "_gwtc4"),
    )

    rows = []
    for _, r in merged.iterrows():
        rf1 = _none_if_nan(r.get("residual_f_phase1"))
        rf2 = _none_if_nan(r.get("residual_f_gwtc4"))
        f1 = _none_if_nan(r.get("freq_hz_phase1"))
        f2 = _none_if_nan(r.get("freq_hz_gwtc4"))
        s1 = _sign(rf1)
        s2 = _sign(rf2)
        sign_match = (s1 is not None and s2 is not None and s1 == s2)
        delta_rf = (rf2 - rf1) if (rf1 is not None and rf2 is not None) else None
        delta_f = (f2 - f1) if (f1 is not None and f2 is not None) else None
        rows.append({
            "event_id": r["event_id"],
            "mode_phase1": r.get("mode_phase1"),
            "mode_gwtc4": r.get("mode_gwtc4"),
            "residual_f_phase1": rf1,
            "residual_f_gwtc4": rf2,
            "sign_f_phase1": s1,
            "sign_f_gwtc4": s2,
            "sign_match": bool(sign_match),
            "f_hz_phase1": f1,
            "f_hz_gwtc4": f2,
            "delta_f_hz": delta_f,
            "sigma_f_hz_phase1": _none_if_nan(r.get("sigma_freq_hz_phase1")),
            "sigma_f_hz_gwtc4": _none_if_nan(r.get("sigma_freq_hz_gwtc4")),
            "f_kerr_hz_phase1": _none_if_nan(r.get("f_kerr_hz_phase1")),
            "f_kerr_hz_gwtc4": _none_if_nan(r.get("f_kerr_hz_gwtc4")),
            "delta_residual_f": delta_rf,
            "source_paper_phase1": r.get("source_paper_phase1"),
            "source_paper_gwtc4": r.get("source_paper_gwtc4"),
        })

    rows.sort(key=lambda r: (r["delta_residual_f"] if r["delta_residual_f"] is not None else float("inf")))

    paired_df = pd.DataFrame(rows)
    paired_path = os.path.join(args.out_dir, "paired_common_events.csv")
    paired_df.to_csv(paired_path, index=False)

    n_common = int(len(paired_df))
    n_sign_match = int(paired_df["sign_match"].sum()) if n_common > 0 else 0
    n_both_positive = int(((paired_df["sign_f_phase1"] == 1) & (paired_df["sign_f_gwtc4"] == 1)).sum()) if n_common > 0 else 0
    n_phase1_positive = int((paired_df["sign_f_phase1"] == 1).sum()) if n_common > 0 else 0
    n_gwtc4_positive = int((paired_df["sign_f_gwtc4"] == 1).sum()) if n_common > 0 else 0

    delta_rf = pd.to_numeric(paired_df["delta_residual_f"], errors="coerce").dropna()
    delta_f = pd.to_numeric(paired_df["delta_f_hz"], errors="coerce").dropna()

    summary = {
        "phase1_input": args.phase1,
        "gwtc4_input": args.gwtc4,
        "n_common": n_common,
        "n_sign_match": n_sign_match,
        "n_both_positive": n_both_positive,
        "n_phase1_positive": n_phase1_positive,
        "n_gwtc4_positive": n_gwtc4_positive,
        "all_common_both_positive": (n_common > 0 and n_both_positive == n_common),
        "median_delta_residual_f": float(delta_rf.median()) if len(delta_rf) else None,
        "median_abs_delta_residual_f": float(delta_rf.abs().median()) if len(delta_rf) else None,
        "median_delta_f_hz": float(delta_f.median()) if len(delta_f) else None,
        "median_abs_delta_f_hz": float(delta_f.abs().median()) if len(delta_f) else None,
        "p_value_note": (
            "No paired p-value is computed: with small n_common and only "
            "partial source independence (remnant metadata shares GWOSC PE "
            "provenance), formal paired tests would overstate inferential "
            "weight. Only descriptive statistics are reported."
        ),
    }

    summary_path = os.path.join(args.out_dir, "paired_comparison_summary.json")
    with open(summary_path, "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=False)
        fh.write("\n")

    print(json.dumps(summary, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
