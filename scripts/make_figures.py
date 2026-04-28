#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNS_ROOT = REPO_ROOT.parent / "RINGEST" / "runs_sync" / "active"
DEFAULT_OUT_DIR = REPO_ROOT / "paper" / "figures"

CRITICAL_EVENTS = ["GW150914", "GW170104", "GW190521_074359"]


def save_figure(fig: plt.Figure, stem: str, out_dir: Path) -> list[str]:
    outputs = []
    for ext in ("png", "pdf"):
        path = out_dir / f"{stem}.{ext}"
        fig.savefig(path, bbox_inches="tight", dpi=220)
        outputs.append(str(path))
    plt.close(fig)
    return outputs


def fig_t10_spearman(summary: dict, out_dir: Path) -> list[str]:
    df = pd.DataFrame(summary["primary_spearman"])
    label_map = {
        "T6.6_O3_literature": "T6.6\nO3 literature",
        "T8.2a_GWTC4_pSEOBNR": "T8.2a\nGWTC-4 pSEOBNR",
        "COMBINED": "Combined",
    }
    df["label"] = df["group"].map(label_map).fillna(df["group"])

    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    colors = ["#1f3b73", "#8aa59a", "#b36a3c"]
    bars = ax.bar(df["label"], df["spearman_rho"], color=colors, edgecolor="black", linewidth=0.8)
    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.set_ylabel("Spearman $\\rho$ between SNR and max residual")
    ax.set_title("T10: SNR-residual correlation by cohort")
    ax.set_ylim(0.0, max(0.85, df["spearman_rho"].max() + 0.1))

    for bar, (_, row) in zip(bars, df.iterrows()):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"$\\rho$={row['spearman_rho']:.3f}\nperm. $p$={row['p_perm_positive']:.3g}",
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.text(
        0.01,
        0.98,
        "Robust in T6.6 only",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=10,
        color="#333333",
    )
    fig.tight_layout()
    return save_figure(fig, "t10_snr_residual_by_cohort", out_dir)


def fig_t10_overlap(overlap: pd.DataFrame, out_dir: Path) -> list[str]:
    df = overlap.copy().sort_values("SNR", ascending=True)
    components = [
        ("shapley_OBS_SHIFT", "Observed shift", "#35608d"),
        ("shapley_OBS_SIGMA_CHANGE", "Observed sigma", "#5b8f74"),
        ("shapley_KERR_PREDICTION_CHANGE", "Kerr prediction", "#c47c3c"),
        ("shapley_KERR_SIGMA_CHANGE", "Kerr sigma", "#8b5e9f"),
    ]

    fig, (ax0, ax1) = plt.subplots(
        1,
        2,
        figsize=(13.0, 5.8),
        gridspec_kw={"width_ratios": [0.9, 1.6]},
        sharey=True,
    )
    y = range(len(df))

    # Panel A: total change in max residual.
    colors_total = ["#b23b3b" if row["lost_high_tail_in_t82a"] else "#4d7c67" for _, row in df.iterrows()]
    ax0.barh(list(y), df["delta_max_abs_residual"], color=colors_total, edgecolor="black", linewidth=0.8)
    ax0.axvline(0.0, color="black", linewidth=1.0)
    ax0.set_xlabel("$\\Delta$ max residual")
    ax0.set_title("Total shift")
    ax0.set_yticks(list(y), df["event"])
    for idx, (_, row) in enumerate(df.iterrows()):
        marker = "lost" if row["lost_high_tail_in_t82a"] else "retained"
        ax0.text(
            row["delta_max_abs_residual"] * 0.55,
            idx,
            f"{row['delta_max_abs_residual']:.3f}\n{marker}",
            va="center",
            ha="center",
            fontsize=8,
            color="white" if abs(row["delta_max_abs_residual"]) > 0.08 else "black",
        )

    # Panel B: stacked Shapley contributions.
    pos_left = [0.0] * len(df)
    neg_left = [0.0] * len(df)
    for col, label, color in components:
        values = df[col].tolist()
        pos_vals = [v if v > 0 else 0.0 for v in values]
        neg_vals = [v if v < 0 else 0.0 for v in values]
        ax1.barh(y, pos_vals, left=pos_left, color=color, edgecolor="white", label=label)
        ax1.barh(y, neg_vals, left=neg_left, color=color, edgecolor="white")
        pos_left = [l + v for l, v in zip(pos_left, pos_vals)]
        neg_left = [l + v for l, v in zip(neg_left, neg_vals)]

    ax1.axvline(0.0, color="black", linewidth=1.0)
    ax1.set_xlabel("Shapley contribution to $\\Delta$ max residual")
    ax1.set_title("Driver decomposition")
    ax1.legend(loc="lower right", frameon=False)

    for idx, (_, row) in enumerate(df.iterrows()):
        ax1.text(
            0.01,
            idx,
            f"SNR={row['SNR']:.1f} | {row['dominant_driver']}",
            va="center",
            ha="left",
            fontsize=8,
            transform=ax1.get_yaxis_transform(),
        )
    fig.suptitle("T10.1: Paired overlap decomposition for the six shared events", y=0.98)
    fig.tight_layout()
    return save_figure(fig, "t10_1_overlap_shapley", out_dir)


def fig_source_audit(t66: pd.DataFrame, t82a: pd.DataFrame, out_dir: Path) -> list[str]:
    left = t66[t66["event"].isin(CRITICAL_EVENTS)][["event", "max_abs_residual", "verdict_kerr"]]
    right = t82a[t82a["event"].isin(CRITICAL_EVENTS)][["event", "max_abs_residual", "verdict_kerr"]]
    merged = left.merge(right, on="event", suffixes=("_t66", "_t82a"))
    merged["event"] = pd.Categorical(merged["event"], categories=CRITICAL_EVENTS, ordered=True)
    merged = merged.sort_values("event")

    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    x = [0, 1]
    colors = ["#1f3b73", "#5b8f74", "#c47c3c"]
    for color, (_, row) in zip(colors, merged.iterrows()):
        y = [row["max_abs_residual_t66"], row["max_abs_residual_t82a"]]
        ax.plot(x, y, marker="o", linewidth=2.2, color=color, label=row["event"])
        ax.text(-0.03, y[0], f"{y[0]:.3f}", color=color, fontsize=8, ha="right", va="center")
        ax.text(1.03, y[1], f"{row['event']}  ({row['verdict_kerr_t82a']})", color=color, fontsize=9, ha="left", va="center")

    ax.set_xticks(x, ["T6.6\n(all marginal)", "T8.2a\n(all consistent)"])
    ax.set_ylabel("Max absolute Kerr residual")
    ax.set_title("Critical-event source audit: T6.6 vs T8.2a")
    fig.tight_layout()
    return save_figure(fig, "source_audit_critical_events", out_dir)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-root", type=Path, default=DEFAULT_RUNS_ROOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    out_dir = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    runs = args.runs_root
    snr_summary = json.loads((runs / "kerr_snr_systematics_t10" / "snr_residual_summary.json").read_text())
    overlap = pd.read_csv(runs / "kerr_snr_systematics_t10" / "snr_overlap_decomposition.csv")
    t66 = pd.read_csv(runs / "kerr_audit_20260424_t66_sigmas" / "kerr_audit_table.csv")
    t82a = pd.read_csv(runs / "kerr_audit_gwtc4_pseobnr_t82a_verified" / "kerr_audit_table.csv")

    manifest = {
        "t10_snr_residual_by_cohort": fig_t10_spearman(snr_summary, out_dir),
        "t10_1_overlap_shapley": fig_t10_overlap(overlap, out_dir),
        "source_audit_critical_events": fig_source_audit(t66, t82a, out_dir),
    }
    (out_dir / "figure_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
