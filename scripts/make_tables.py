#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS_ROOT = REPO_ROOT.parent / "RINGEST" / "runs_sync" / "active"
DEFAULT_OUT_DIR = REPO_ROOT / "paper" / "tables"

CRITICAL_EVENTS = ["GW150914", "GW170104", "GW190521_074359"]


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def write_latex(df: pd.DataFrame, path: Path) -> None:
    latex = df.to_latex(
        index=False,
        escape=True,
        float_format=lambda x: f"{x:.6g}",
        longtable=False,
        na_rep="",
    )
    path.write_text(latex)


def build_source_audit_table(t66: pd.DataFrame, t82a: pd.DataFrame) -> pd.DataFrame:
    left = t66[t66["event"].isin(CRITICAL_EVENTS)][
        ["event", "max_abs_residual", "residual_f", "residual_gamma", "verdict_kerr"]
    ].rename(
        columns={
            "max_abs_residual": "max_abs_residual_t66",
            "residual_f": "residual_f_t66",
            "residual_gamma": "residual_gamma_t66",
            "verdict_kerr": "verdict_t66",
        }
    )
    right = t82a[t82a["event"].isin(CRITICAL_EVENTS)][
        ["event", "max_abs_residual", "residual_f", "residual_gamma", "verdict_kerr"]
    ].rename(
        columns={
            "max_abs_residual": "max_abs_residual_t82a",
            "residual_f": "residual_f_t82a",
            "residual_gamma": "residual_gamma_t82a",
            "verdict_kerr": "verdict_t82a",
        }
    )
    merged = left.merge(right, on="event", how="inner")
    order = pd.Categorical(merged["event"], categories=CRITICAL_EVENTS, ordered=True)
    return merged.assign(_order=order).sort_values("_order").drop(columns="_order")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    runs = args.runs_root
    t66_audit = load_csv(runs / "kerr_audit_20260424_t66_sigmas" / "kerr_audit_table.csv")
    t82a_audit = load_csv(
        runs / "kerr_audit_gwtc4_pseobnr_t82a_verified" / "kerr_audit_table.csv"
    )
    t9_stats = load_csv(runs / "kerr_population_tail_t9" / "population_tail_stats_table.csv")
    t10_audit = load_csv(runs / "kerr_snr_systematics_t10" / "snr_residual_audit_table.csv")
    t10_overlap = load_csv(runs / "kerr_snr_systematics_t10" / "snr_overlap_decomposition.csv")

    tables: list[tuple[str, pd.DataFrame, str, str]] = [
        (
            "t66_kerr_audit_table.tex",
            t66_audit[
                [
                    "event",
                    "f_obs_hz",
                    "f_kerr_hz",
                    "gamma_obs_hz",
                    "gamma_kerr_hz",
                    "residual_f",
                    "residual_gamma",
                    "max_abs_residual",
                    "verdict_kerr",
                ]
            ],
            "T6.6 Kerr audit rows used in Phase 2.",
            "tab:t66-kerr-audit",
        ),
        (
            "t82a_kerr_audit_table.tex",
            t82a_audit[
                [
                    "event",
                    "f_obs_hz",
                    "f_kerr_hz",
                    "gamma_obs_hz",
                    "gamma_kerr_hz",
                    "residual_f",
                    "residual_gamma",
                    "max_abs_residual",
                    "verdict_kerr",
                ]
            ],
            "T8.2a Kerr audit rows used in Phase 2.",
            "tab:t82a-kerr-audit",
        ),
        (
            "t9_population_tail_stats_table.tex",
            t9_stats[
                [
                    "cohort",
                    "event",
                    "verdict_kerr",
                    "max_abs_residual",
                    "network_matched_filter_snr",
                    "population_tail_rank",
                    "population_tail_rank_combined",
                    "population_tail_top_tertile",
                    "population_tail_top_tertile_combined",
                ]
            ],
            "Population-tail statistics table derived from T9 inputs.",
            "tab:t9-population-tail",
        ),
        (
            "t10_snr_residual_audit_table.tex",
            t10_audit[
                [
                    "cohort",
                    "event",
                    "verdict_kerr",
                    "max_abs_residual",
                    "network_matched_filter_snr",
                    "snr_rank_cohort_desc",
                    "residual_rank_cohort_desc",
                    "population_tail_rank",
                    "audit_flags",
                ]
            ],
            "SNR-residual audit rows used for T10.",
            "tab:t10-snr-audit",
        ),
        (
            "t10_overlap_decomposition_table.tex",
            t10_overlap[
                [
                    "event",
                    "SNR",
                    "max_abs_residual_t66",
                    "max_abs_residual_t82a",
                    "delta_max_abs_residual",
                    "shapley_OBS_SHIFT",
                    "shapley_OBS_SIGMA_CHANGE",
                    "shapley_KERR_PREDICTION_CHANGE",
                    "shapley_KERR_SIGMA_CHANGE",
                    "dominant_driver",
                    "lost_high_tail_in_t82a",
                ]
            ],
            "Six-event overlap decomposition used for T10.1.",
            "tab:t10-overlap-decomposition",
        ),
        (
            "source_audit_critical_events_table.tex",
            build_source_audit_table(t66_audit, t82a_audit),
            "Critical-event source audit comparison for T6.6 and T8.2a.",
            "tab:source-audit-critical",
        ),
    ]

    manifest = []
    for filename, df, caption, label in tables:
        path = out_dir / filename
        write_latex(df, path)
        manifest.append(
            {
                "path": str(path),
                "rows": int(len(df)),
                "columns": list(df.columns),
                "caption": caption,
            }
        )

    (out_dir / "table_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
