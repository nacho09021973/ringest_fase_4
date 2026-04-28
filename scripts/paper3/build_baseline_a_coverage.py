"""
Paper 3 — baseline A coverage table.

Reads the canonical literature YAML (LVK/TGR GWTC-2 reported QNM modes plus
Kerr metadata) and writes one row per (event, mode) covering the columns
needed to declare baseline A coverage for Paper 3. This is *not* yet the
A/B/C/D/E reporting heterogeneity matrix; only the baseline A audit.

Stdlib-only on purpose: this script is meant to run anywhere without
installing extra dependencies. It contains a focused parser for the exact
schema of `data/phase1_data/qnm_events_literature.yml`.
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUT = REPO_ROOT / "data" / "phase1_data" / "qnm_events_literature.yml"
DEFAULT_OUTPUT = REPO_ROOT / "outputs" / "paper3" / "baseline_a_coverage.csv"

SOURCE_FAMILY_BASELINE_A = "A"

COLUMNS = [
    "event_id",
    "source_family",
    "source_paper",
    "mode",
    "f_hz",
    "sigma_f_hz",
    "tau_ms",
    "sigma_tau_ms",
    "M_final_Msun",
    "chi_final",
    "redshift",
    "sigma_M_final_Msun",
    "sigma_chi_final",
    "has_qnm_uncertainty",
    "has_kerr_metadata",
    "has_kerr_uncertainty",
    "usable_for_baseline_A",
    "usable_for_full_kerr_uncertainty",
]


def _parse_scalar(raw: str):
    s = raw.strip()
    if s == "" or s.lower() == "null" or s == "~":
        return None
    if (s.startswith("'") and s.endswith("'")) or (s.startswith('"') and s.endswith('"')):
        return s[1:-1]
    try:
        if "." in s or "e" in s or "E" in s:
            return float(s)
        return int(s)
    except ValueError:
        return s


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def parse_literature_yaml(path: Path) -> list[dict]:
    """Parse the literature QNM YAML.

    Schema assumed:
        metadata: { ... }
        events:
          - event: <id>
            <key>: <value>
            ...
            modes:
              - l: <int>
                m: <int>
                n: <int>
                <key>: <value>
                ...

    Tabs are not allowed; indentation uses spaces. The parser is strict to
    that schema and will raise if the file deviates.
    """
    if not path.exists():
        raise FileNotFoundError(f"Literature YAML not found: {path}")

    raw_lines = path.read_text(encoding="utf-8").splitlines()

    in_events = False
    events: list[dict] = []
    current_event: dict | None = None
    in_modes = False
    current_mode: dict | None = None

    for raw in raw_lines:
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        ind = _indent(line)
        body = line.strip()

        if ind == 0:
            in_events = body == "events:"
            current_event = None
            current_mode = None
            in_modes = False
            continue

        if not in_events:
            continue

        if ind == 2 and body.startswith("- event:"):
            if current_event is not None:
                events.append(current_event)
            key, _, value = body[2:].partition(":")
            current_event = {key.strip(): _parse_scalar(value), "modes": []}
            in_modes = False
            current_mode = None
            continue

        if current_event is None:
            continue

        if ind == 4 and body.endswith(":") and ":" not in body[:-1]:
            in_modes = body == "modes:"
            current_mode = None
            continue

        if ind == 4 and ":" in body:
            key, _, value = body.partition(":")
            current_event[key.strip()] = _parse_scalar(value)
            in_modes = False
            current_mode = None
            continue

        if in_modes and ind == 6 and body.startswith("- "):
            key, _, value = body[2:].partition(":")
            current_mode = {key.strip(): _parse_scalar(value)}
            current_event["modes"].append(current_mode)
            continue

        if in_modes and ind == 8 and current_mode is not None and ":" in body:
            key, _, value = body.partition(":")
            current_mode[key.strip()] = _parse_scalar(value)
            continue

    if current_event is not None:
        events.append(current_event)

    return events


def _present(value) -> bool:
    return value is not None and value != ""


def build_rows(events: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for ev in events:
        event_id = ev.get("event")
        z = ev.get("z")
        m_final = ev.get("M_final_Msun")
        chi_final = ev.get("chi_final")
        sigma_m = ev.get("sigma_M_final_Msun")
        sigma_chi = ev.get("sigma_chi_final")
        for mode in ev.get("modes") or []:
            l = mode.get("l")
            m = mode.get("m")
            n = mode.get("n")
            mode_label = f"{l}{m}{n}" if None not in (l, m, n) else ""
            f_hz = mode.get("f_hz")
            sigma_f_hz = mode.get("sigma_f_hz")
            tau_ms = mode.get("tau_ms")
            sigma_tau_ms = mode.get("sigma_tau_ms")
            source_paper = mode.get("source_paper", "")

            has_qnm_uncertainty = _present(sigma_f_hz) and _present(sigma_tau_ms)
            has_kerr_metadata = _present(m_final) and _present(chi_final)
            has_kerr_uncertainty = _present(sigma_m) and _present(sigma_chi)
            usable_baseline = (
                _present(f_hz)
                and _present(tau_ms)
                and has_qnm_uncertainty
                and has_kerr_metadata
                and _present(z)
            )
            usable_full = usable_baseline and has_kerr_uncertainty

            rows.append(
                {
                    "event_id": event_id,
                    "source_family": SOURCE_FAMILY_BASELINE_A,
                    "source_paper": source_paper,
                    "mode": mode_label,
                    "f_hz": f_hz,
                    "sigma_f_hz": sigma_f_hz,
                    "tau_ms": tau_ms,
                    "sigma_tau_ms": sigma_tau_ms,
                    "M_final_Msun": m_final,
                    "chi_final": chi_final,
                    "redshift": z,
                    "sigma_M_final_Msun": sigma_m,
                    "sigma_chi_final": sigma_chi,
                    "has_qnm_uncertainty": has_qnm_uncertainty,
                    "has_kerr_metadata": has_kerr_metadata,
                    "has_kerr_uncertainty": has_kerr_uncertainty,
                    "usable_for_baseline_A": usable_baseline,
                    "usable_for_full_kerr_uncertainty": usable_full,
                }
            )
    return rows


def write_csv(rows: list[dict], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)

    events = parse_literature_yaml(args.input)
    if not events:
        print(f"ERROR: no events parsed from {args.input}", file=sys.stderr)
        return 2

    rows = build_rows(events)
    write_csv(rows, args.output)

    n_events = len({r["event_id"] for r in rows})
    n_usable = sum(1 for r in rows if r["usable_for_baseline_A"])
    n_full = sum(1 for r in rows if r["usable_for_full_kerr_uncertainty"])

    print(f"Wrote {len(rows)} rows ({n_events} events) to {args.output}")
    print(f"  usable_for_baseline_A:           {n_usable}/{len(rows)}")
    print(f"  usable_for_full_kerr_uncertainty: {n_full}/{len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
