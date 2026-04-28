"""
Paper 3 — case study comparator: GW190910 baseline A vs GWTC-4.0 Table 3.

Reads:
  - outputs/paper3/baseline_a_coverage.csv
  - data/phase1_data/qnm_events_gwtc4_remnants_table3.yml

Selects:
  - baseline A row with event_id=GW190910_112807 and mode=220
  - GWTC-4.0 Remnants Table 3 row with event_id=GW190910_112807

Writes:
  - outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.csv
  - outputs/paper3/gw190910_a_vs_gwtc4_table3_comparison.md

Metrics computed:
  - delta_f_hz   = f_A_double_prime - f_A
  - delta_tau_ms = tau_A_double_prime - tau_A
  - A intervals from symmetric baseline sigmas
  - A_double_prime intervals from asymmetric Table 3 uncertainties
  - overlap_f_interval and overlap_tau_interval

Deliberately NOT computed:
  - p-values
  - combined sigma residuals
  - symmetrisation of A_double_prime intervals
  - any claim of physical tension
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_BASELINE_A = REPO_ROOT / "outputs" / "paper3" / "baseline_a_coverage.csv"
DEFAULT_GWTC4_YAML = REPO_ROOT / "data" / "phase1_data" / "qnm_events_gwtc4_remnants_table3.yml"
DEFAULT_OUT_CSV = REPO_ROOT / "outputs" / "paper3" / "gw190910_a_vs_gwtc4_table3_comparison.csv"
DEFAULT_OUT_MD = REPO_ROOT / "outputs" / "paper3" / "gw190910_a_vs_gwtc4_table3_comparison.md"

EVENT_ID = "GW190910_112807"
MODE = "220"

CSV_COLUMNS = [
    "event_id",
    "a_source_family",
    "a_mode",
    "b_source_family",
    "b_source_classification",
    "b_secondary_classification",
    "b_pipeline",
    "b_table",
    "b_mode",
    "f_a_hz",
    "sigma_f_a_hz",
    "tau_a_ms",
    "sigma_tau_a_ms",
    "f_b_hz",
    "f_b_hz_minus",
    "f_b_hz_plus",
    "tau_b_ms",
    "tau_b_ms_minus",
    "tau_b_ms_plus",
    "delta_f_hz",
    "delta_tau_ms",
    "A_f_low_hz",
    "A_f_high_hz",
    "A_tau_low_ms",
    "A_tau_high_ms",
    "B_f_low_hz",
    "B_f_high_hz",
    "B_tau_low_ms",
    "B_tau_high_ms",
    "overlap_f_interval",
    "overlap_tau_interval",
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


def load_gwtc4_event(path: Path, event_id: str) -> tuple[dict, dict]:
    if not path.exists():
        raise FileNotFoundError(f"GWTC-4 Table 3 YAML not found: {path}")
    with path.open(encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    for event in doc.get("events", []) or []:
        if event.get("event_id") == event_id:
            return doc, event
    raise LookupError(f"GWTC-4 Table 3 event not found for event_id={event_id} in {path}")


def intervals_overlap(a_low: float, a_high: float, b_low: float, b_high: float) -> bool:
    return max(a_low, b_low) <= min(a_high, b_high)


def build_comparison(a_row: dict, gwtc4_doc: dict, gwtc4_event: dict) -> dict:
    f_a = float(a_row["f_hz"])
    sigma_f_a = float(a_row["sigma_f_hz"])
    tau_a = float(a_row["tau_ms"])
    sigma_tau_a = float(a_row["sigma_tau_ms"])

    f_b = float(gwtc4_event["f220_hz"])
    f_b_minus = float(gwtc4_event["f220_hz_minus"])
    f_b_plus = float(gwtc4_event["f220_hz_plus"])
    tau_b = float(gwtc4_event["tau220_ms"])
    tau_b_minus = float(gwtc4_event["tau220_ms_minus"])
    tau_b_plus = float(gwtc4_event["tau220_ms_plus"])

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
        "b_source_family": gwtc4_doc.get("source_family", ""),
        "b_source_classification": gwtc4_doc.get("source_classification", ""),
        "b_secondary_classification": gwtc4_doc.get("secondary_classification", ""),
        "b_pipeline": gwtc4_doc.get("pipeline", ""),
        "b_table": gwtc4_doc.get("table", ""),
        "b_mode": gwtc4_doc.get("mode", ""),
        "f_a_hz": f_a,
        "sigma_f_a_hz": sigma_f_a,
        "tau_a_ms": tau_a,
        "sigma_tau_a_ms": sigma_tau_a,
        "f_b_hz": f_b,
        "f_b_hz_minus": f_b_minus,
        "f_b_hz_plus": f_b_plus,
        "tau_b_ms": tau_b,
        "tau_b_ms_minus": tau_b_minus,
        "tau_b_ms_plus": tau_b_plus,
        "delta_f_hz": round(f_b - f_a, 4),
        "delta_tau_ms": round(tau_b - tau_a, 4),
        "A_f_low_hz": A_f_low,
        "A_f_high_hz": A_f_high,
        "A_tau_low_ms": A_tau_low,
        "A_tau_high_ms": A_tau_high,
        "B_f_low_hz": B_f_low,
        "B_f_high_hz": B_f_high,
        "B_tau_low_ms": B_tau_low,
        "B_tau_high_ms": B_tau_high,
        "overlap_f_interval": intervals_overlap(A_f_low, A_f_high, B_f_low, B_f_high),
        "overlap_tau_interval": intervals_overlap(A_tau_low, A_tau_high, B_tau_low, B_tau_high),
    }


def write_csv(row: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerow(row)


def write_markdown(row: dict, gwtc4_doc: dict, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# GW190910_112807 — baseline A vs GWTC-4.0 Table 3",
        "",
        "Esta es una comparación preliminar de **reporting**, no un test físico.",
        "",
        "La fuente A_double_prime procede de LVK/GWTC-4.0 Remnants; no es una fuente B externa independiente.",
        "",
        "## Selección",
        "",
        f"- Baseline A: `event_id={EVENT_ID}`, `mode={MODE}` desde `outputs/paper3/baseline_a_coverage.csv`.",
        f"- A_double_prime: `event_id={EVENT_ID}`, `pipeline={row['b_pipeline']}`, `table={row['b_table']}` desde `data/phase1_data/qnm_events_gwtc4_remnants_table3.yml`.",
        f"- Fuente: `{gwtc4_doc.get('source_paper', '')}`.",
        "",
        "## Valores comparados",
        "",
        "| Magnitud | Baseline A (220) | GWTC-4 Table 3 / pSEOBNRV5PHM (220) |",
        "|---|---|---|",
        f"| f_hz | {row['f_a_hz']} ± {row['sigma_f_a_hz']} | {row['f_b_hz']} +{row['f_b_hz_plus']}/-{row['f_b_hz_minus']} |",
        f"| tau_ms | {row['tau_a_ms']} ± {row['sigma_tau_a_ms']} | {row['tau_b_ms']} +{row['tau_b_ms_plus']}/-{row['tau_b_ms_minus']} |",
        "",
        "## Intervalos derivados",
        "",
        "| Magnitud | A_low | A_high | A_double_prime_low | A_double_prime_high |",
        "|---|---:|---:|---:|---:|",
        f"| f_hz | {row['A_f_low_hz']} | {row['A_f_high_hz']} | {row['B_f_low_hz']} | {row['B_f_high_hz']} |",
        f"| tau_ms | {row['A_tau_low_ms']} | {row['A_tau_high_ms']} | {row['B_tau_low_ms']} | {row['B_tau_high_ms']} |",
        "",
        "## Diferencias brutas (sin estadística)",
        "",
        f"- delta_f_hz = f_A_double_prime - f_A = {row['delta_f_hz']}",
        f"- delta_tau_ms = tau_A_double_prime - tau_A = {row['delta_tau_ms']}",
        "",
        "## Solapamiento de intervalos",
        "",
        f"- f intervals overlap: **{row['overlap_f_interval']}**",
        f"- tau intervals overlap: **{row['overlap_tau_interval']}**",
        "",
        "## Cautelas",
        "",
        "- No se calculan p-values ni residual sigma combinado.",
        "- Los intervalos de GWTC-4 Table 3 son asimétricos y se preservan así; no se han simetrizado.",
        "- Los valores IMR-GR internos de Table 3 se preservan en el YAML, pero no sustituyen baseline A.",
        "- Esto es un estudio de caso de reporting heterogeneity, no una afirmación de tensión física con Kerr.",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-a-csv", type=Path, default=DEFAULT_BASELINE_A)
    parser.add_argument("--gwtc4-yaml", type=Path, default=DEFAULT_GWTC4_YAML)
    parser.add_argument("--out-csv", type=Path, default=DEFAULT_OUT_CSV)
    parser.add_argument("--out-md", type=Path, default=DEFAULT_OUT_MD)
    args = parser.parse_args(argv)

    a_row = load_baseline_a_row(args.baseline_a_csv, EVENT_ID, MODE)
    gwtc4_doc, gwtc4_event = load_gwtc4_event(args.gwtc4_yaml, EVENT_ID)
    comparison = build_comparison(a_row, gwtc4_doc, gwtc4_event)

    write_csv(comparison, args.out_csv)
    write_markdown(comparison, gwtc4_doc, args.out_md)

    print(f"Wrote {args.out_csv}")
    print(f"Wrote {args.out_md}")
    print(f"  delta_f_hz           = {comparison['delta_f_hz']}")
    print(f"  delta_tau_ms         = {comparison['delta_tau_ms']}")
    print(f"  overlap_f_interval   = {comparison['overlap_f_interval']}")
    print(f"  overlap_tau_interval = {comparison['overlap_tau_interval']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
