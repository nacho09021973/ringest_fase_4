"""
Paper 3 — case study comparator: GW190521 baseline A vs Capano et al. 2023.

Reads:
  - outputs/paper3/baseline_a_coverage.csv         (baseline A, source_family=A)
  - data/phase1_data/qnm_events_capano2023.yml    (B_abs_agnostic_labels)

Selects:
  - baseline A row with event_id=GW190521 and mode=220
  - Capano resonance with kerr_identification=220_candidate

Writes:
  - outputs/paper3/gw190521_a_vs_capano2023_comparison.csv
  - outputs/paper3/gw190521_a_vs_capano2023_comparison.md

Metrics computed (deliberately conservative):
  - delta_f_hz   = f_B - f_A
  - delta_tau_ms = tau_B - tau_A
  - A intervals (symmetric) and B intervals (asymmetric, preserved)
  - overlap_f_interval   : intervals A and B for f intersect?
  - overlap_tau_interval : intervals A and B for tau intersect?

Deliberately NOT computed:
  - p-values
  - combined sigma residuals
  - symmetrisation of B intervals
  - any claim of physical tension

The Capano range B / 330_candidate resonance is excluded from this comparator
because baseline A only contains the (2,2,0) mode for GW190521.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE_A = REPO_ROOT / "outputs" / "paper3" / "baseline_a_coverage.csv"
DEFAULT_CAPANO_YAML = REPO_ROOT / "data" / "phase1_data" / "qnm_events_capano2023.yml"
DEFAULT_OUT_CSV = REPO_ROOT / "outputs" / "paper3" / "gw190521_a_vs_capano2023_comparison.csv"
DEFAULT_OUT_MD = REPO_ROOT / "outputs" / "paper3" / "gw190521_a_vs_capano2023_comparison.md"

EVENT_ID = "GW190521"
A_MODE = "220"
B_KERR_ID = "220_candidate"

CSV_COLUMNS = [
    "event_id",
    "a_source_family",
    "a_mode",
    "b_source_family",
    "b_kerr_identification",
    "b_agnostic_range",
    "b_mode_label_original",
    "f_a_hz", "sigma_f_a_hz",
    "tau_a_ms", "sigma_tau_a_ms",
    "f_b_hz", "f_b_hz_minus", "f_b_hz_plus",
    "tau_b_ms", "tau_b_ms_minus", "tau_b_ms_plus",
    "delta_f_hz", "delta_tau_ms",
    "A_f_low_hz", "A_f_high_hz",
    "A_tau_low_ms", "A_tau_high_ms",
    "B_f_low_hz", "B_f_high_hz",
    "B_tau_low_ms", "B_tau_high_ms",
    "overlap_f_interval", "overlap_tau_interval",
]


def load_baseline_a_row(path: Path, event_id: str, mode: str) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"Baseline A CSV not found: {path}")
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            if row["event_id"] == event_id and row["mode"] == mode:
                return row
    raise LookupError(f"Baseline A row not found for event_id={event_id} mode={mode} in {path}")


def load_capano_resonance(path: Path, event_id: str, kerr_identification: str) -> tuple[dict, dict]:
    if not path.exists():
        raise FileNotFoundError(f"Capano YAML not found: {path}")
    with path.open(encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    for ev in doc.get("events", []) or []:
        if ev.get("event_id") != event_id:
            continue
        for res in ev.get("resonances", []) or []:
            if res.get("kerr_identification") == kerr_identification:
                return doc, {**ev, **{"_resonance": res}}
    raise LookupError(
        f"Capano resonance not found for event_id={event_id} kerr_identification={kerr_identification} in {path}"
    )


def intervals_overlap(a_low: float, a_high: float, b_low: float, b_high: float) -> bool:
    return max(a_low, b_low) <= min(a_high, b_high)


def build_comparison(a_row: dict, capano_doc: dict, capano_event: dict) -> dict:
    res = capano_event["_resonance"]

    f_a = float(a_row["f_hz"])
    sigma_f_a = float(a_row["sigma_f_hz"])
    tau_a = float(a_row["tau_ms"])
    sigma_tau_a = float(a_row["sigma_tau_ms"])

    f_b = float(res["f_hz"])
    f_b_minus = float(res["f_hz_minus"])
    f_b_plus = float(res["f_hz_plus"])
    tau_b = float(res["tau_ms"])
    tau_b_minus = float(res["tau_ms_minus"])
    tau_b_plus = float(res["tau_ms_plus"])

    A_f_low = round(f_a - sigma_f_a, 4)
    A_f_high = round(f_a + sigma_f_a, 4)
    A_tau_low = round(tau_a - sigma_tau_a, 4)
    A_tau_high = round(tau_a + sigma_tau_a, 4)

    B_f_low = round(f_b - f_b_minus, 4)
    B_f_high = round(f_b + f_b_plus, 4)
    B_tau_low = round(tau_b - tau_b_minus, 4)
    B_tau_high = round(tau_b + tau_b_plus, 4)

    return {
        "event_id": EVENT_ID,
        "a_source_family": a_row.get("source_family", ""),
        "a_mode": a_row["mode"],
        "b_source_family": capano_doc.get("source_family", ""),
        "b_kerr_identification": res.get("kerr_identification", ""),
        "b_agnostic_range": res.get("agnostic_range", ""),
        "b_mode_label_original": res.get("mode_label_original", ""),
        "f_a_hz": f_a, "sigma_f_a_hz": sigma_f_a,
        "tau_a_ms": tau_a, "sigma_tau_a_ms": sigma_tau_a,
        "f_b_hz": f_b, "f_b_hz_minus": f_b_minus, "f_b_hz_plus": f_b_plus,
        "tau_b_ms": tau_b, "tau_b_ms_minus": tau_b_minus, "tau_b_ms_plus": tau_b_plus,
        "delta_f_hz": round(f_b - f_a, 4),
        "delta_tau_ms": round(tau_b - tau_a, 4),
        "A_f_low_hz": A_f_low, "A_f_high_hz": A_f_high,
        "A_tau_low_ms": A_tau_low, "A_tau_high_ms": A_tau_high,
        "B_f_low_hz": B_f_low, "B_f_high_hz": B_f_high,
        "B_tau_low_ms": B_tau_low, "B_tau_high_ms": B_tau_high,
        "overlap_f_interval": intervals_overlap(A_f_low, A_f_high, B_f_low, B_f_high),
        "overlap_tau_interval": intervals_overlap(A_tau_low, A_tau_high, B_tau_low, B_tau_high),
    }


def write_csv(row: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerow(row)


def write_markdown(row: dict, capano_doc: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# GW190521 — baseline A vs Capano 2023 (preliminary reporting comparison)",
        "",
        "Esta es una comparación preliminar de **reporting**, no un test físico.",
        "",
        "## Selección",
        "",
        f"- Baseline A: `event_id={EVENT_ID}`, `mode={A_MODE}` desde `outputs/paper3/baseline_a_coverage.csv`.",
        f"- Capano 2023: resonancia con `kerr_identification={B_KERR_ID}` desde `data/phase1_data/qnm_events_capano2023.yml`.",
        f"- Fuente B: `{capano_doc.get('source_paper', '')}`.",
        "",
        "## Valores comparados",
        "",
        "| Magnitud | Baseline A (220) | Capano 2023 (range A / 220_candidate) |",
        "|---|---|---|",
        f"| f_hz | {row['f_a_hz']} ± {row['sigma_f_a_hz']} | {row['f_b_hz']} +{row['f_b_hz_plus']}/-{row['f_b_hz_minus']} |",
        f"| tau_ms | {row['tau_a_ms']} ± {row['sigma_tau_a_ms']} | {row['tau_b_ms']} +{row['tau_b_ms_plus']}/-{row['tau_b_ms_minus']} |",
        "",
        "## Intervalos derivados",
        "",
        "| Magnitud | A_low | A_high | B_low | B_high |",
        "|---|---:|---:|---:|---:|",
        f"| f_hz | {row['A_f_low_hz']} | {row['A_f_high_hz']} | {row['B_f_low_hz']} | {row['B_f_high_hz']} |",
        f"| tau_ms | {row['A_tau_low_ms']} | {row['A_tau_high_ms']} | {row['B_tau_low_ms']} | {row['B_tau_high_ms']} |",
        "",
        "## Diferencias brutas (sin estadística)",
        "",
        f"- delta_f_hz = f_B - f_A = {row['delta_f_hz']}",
        f"- delta_tau_ms = tau_B - tau_A = {row['delta_tau_ms']}",
        "",
        "## Solapamiento de intervalos",
        "",
        f"- f intervals overlap: **{row['overlap_f_interval']}**",
        f"- tau intervals overlap: **{row['overlap_tau_interval']}**",
        "",
        "## Cautelas",
        "",
        "- No se calculan p-values ni residual sigma combinado.",
        "- Los intervalos de Capano son asimétricos y se preservan así; no se han simetrizado.",
        "- La Capano range B / 330_candidate queda fuera de esta comparación porque baseline A no contiene 330 para GW190521.",
        "- Esto es un estudio de caso de reporting heterogeneity, no una afirmación de tensión física.",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-a-csv", type=Path, default=DEFAULT_BASELINE_A)
    parser.add_argument("--capano-yaml", type=Path, default=DEFAULT_CAPANO_YAML)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    a_row = load_baseline_a_row(args.baseline_a_csv, EVENT_ID, A_MODE)
    capano_doc, capano_event = load_capano_resonance(args.capano_yaml, EVENT_ID, B_KERR_ID)
    comparison = build_comparison(a_row, capano_doc, capano_event)

    write_csv(comparison, args.out_csv)
    write_markdown(comparison, capano_doc, args.out_md)

    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")
    print(f"  delta_f_hz           = {comparison['delta_f_hz']}")
    print(f"  delta_tau_ms         = {comparison['delta_tau_ms']}")
    print(f"  overlap_f_interval   = {comparison['overlap_f_interval']}")
    print(f"  overlap_tau_interval = {comparison['overlap_tau_interval']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
