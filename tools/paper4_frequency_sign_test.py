#!/usr/bin/env python3
"""
Paper 4 — Frequency residual sign test (exact binomial).

Reads an existing schema-aligned 220 dataset, takes the existing
``residual_f`` column without recalculation, and tests population-level
sign coherence under the null hypothesis ``P(residual_f > 0) = 0.5``
using an exact binomial test implemented with ``math.comb`` only
(no scipy dependency).

Outputs:
- ``frequency_sign_test_summary.json``: counts, p-values, configuration.
- ``frequency_sign_test_table.csv``: per-event ``residual_f`` and sign,
  sorted by ``residual_f`` descending.

The script does not recalculate ``f_kerr_hz`` or ``residual_f``, does not
modify the input CSV, and does not produce any candidate language. It is
intended as a permanent, versionable artifact for the population-level
sign question raised in ``docs/paper4_frequency_only_residual_audit.md``.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from typing import Optional


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--input",
        required=True,
        help="Path to the schema-aligned 220 CSV containing a residual_f column.",
    )
    p.add_argument(
        "--out-dir",
        required=True,
        help="Output directory; created if missing.",
    )
    return p.parse_args()


def to_float(s: Optional[str]) -> Optional[float]:
    if s is None:
        return None
    s = s.strip()
    if s == "" or s.lower() == "nan":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _binom_pmf(k: int, n: int) -> float:
    return math.comb(n, k) / (2 ** n)


def binomial_p_at_least(k: int, n: int) -> float:
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    return sum(_binom_pmf(j, n) for j in range(k, n + 1))


def binomial_p_at_most(k: int, n: int) -> float:
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return sum(_binom_pmf(j, n) for j in range(0, k + 1))


def main() -> int:
    args = parse_args()
    os.makedirs(args.out_dir, exist_ok=True)

    rows = []
    with open(args.input, newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            res_f = to_float(row.get("residual_f"))
            if res_f is None:
                continue
            event_id = row.get("event_id") or row.get("event") or ""
            mode = row.get("mode") or ""
            f_hz = to_float(row.get("freq_hz"))
            sigma_f_hz = to_float(row.get("sigma_freq_hz"))
            f_kerr_hz = to_float(row.get("f_kerr_hz"))
            source_paper = row.get("source_paper") or row.get("pole_source") or ""

            if res_f > 0:
                sign_f = 1
            elif res_f < 0:
                sign_f = -1
            else:
                sign_f = 0

            rows.append({
                "event_id": event_id,
                "mode": mode,
                "residual_f": res_f,
                "sign_f": sign_f,
                "f_hz": f_hz,
                "sigma_f_hz": sigma_f_hz,
                "f_kerr_hz": f_kerr_hz,
                "source_paper": source_paper,
            })

    n_total = len(rows)
    n_positive = sum(1 for r in rows if r["sign_f"] > 0)
    n_negative = sum(1 for r in rows if r["sign_f"] < 0)
    n_zero = sum(1 for r in rows if r["sign_f"] == 0)

    p_geq = binomial_p_at_least(n_positive, n_total)
    p_leq = binomial_p_at_most(n_positive, n_total)
    p_one_sided_positive = p_geq
    p_two_sided = min(2.0 * min(p_geq, p_leq), 1.0)

    summary = {
        "input": args.input,
        "n_total": n_total,
        "n_positive": n_positive,
        "n_negative": n_negative,
        "n_zero": n_zero,
        "null_hypothesis": "P(residual_f > 0) = 0.5",
        "test": "exact_binomial_via_math_comb",
        "zero_handling": "zeros (residual_f == 0) counted as not-positive; binomial uses n_total",
        "p_one_sided_positive": p_one_sided_positive,
        "p_two_sided": p_two_sided,
    }

    summary_path = os.path.join(args.out_dir, "frequency_sign_test_summary.json")
    with open(summary_path, "w") as fh:
        json.dump(summary, fh, indent=2, sort_keys=False)
        fh.write("\n")

    rows.sort(key=lambda r: r["residual_f"], reverse=True)
    table_path = os.path.join(args.out_dir, "frequency_sign_test_table.csv")
    fieldnames = [
        "event_id", "mode", "residual_f", "sign_f",
        "f_hz", "sigma_f_hz", "f_kerr_hz", "source_paper",
    ]
    with open(table_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(json.dumps(summary, indent=2, sort_keys=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
