#!/usr/bin/env python3
"""Build derived dashboard health signals from canonical Pantarijnweek data."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "2026"
CONFIG = ROOT / "config" / "2026_dashboard.json"


def read_csv(name: str):
    path = DATA / name
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def signal(signal_id, scope_type, scope_id, rule_id, severity, title,
           explanation, observed_value=None, threshold_or_expectation=None,
           source_refs=None):
    return {
        "signal_id": signal_id,
        "scope_type": scope_type,
        "scope_id": scope_id,
        "rule_id": rule_id,
        "severity": severity,
        "title": title,
        "explanation": explanation,
        "observed_value": observed_value,
        "threshold_or_expectation": threshold_or_expectation,
        "source_refs": source_refs or [],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="")
    args = p.parse_args()

    activities = read_csv("activities.csv")
    offerings = read_csv("offerings.csv")
    publications = read_csv("publication_status.csv")
    external = read_csv("external_system_records.csv")
    cohorts = read_csv("cohorts.csv")
    rooms = read_csv("rooms.csv")
    assignments = read_csv("assignments.csv")

    cfg = json.loads(CONFIG.read_text(encoding="utf-8")) if CONFIG.exists() else {}

    signals = []

    unreconciled = [r for r in external if r.get("status", "").strip() in {"captured", "unreconciled"}]
    signals.append(signal(
        "REG-EXT-001", "edition", "2026", "external_records_reconciled",
        "critical" if unreconciled else "ok",
        "Buitenom-records",
        f"{len(unreconciled)} extern(e) record(s) wachten nog op reconciliatie."
        if unreconciled else "Geen open buitenom-records.",
        len(unreconciled), 0,
        ["data/2026/external_system_records.csv"],
    ))

    missing_room = [r for r in offerings if not r.get("room_id", "").strip()]
    signals.append(signal(
        "REG-ROOM-001", "edition", "2026", "offerings_have_room",
        "warning" if missing_room else "ok",
        "Lokalen",
        f"{len(missing_room)} offering(s) hebben nog geen lokaal."
        if missing_room else "Alle offerings hebben een lokaal.",
        len(missing_room), 0,
        ["data/2026/offerings.csv", "data/2026/rooms.csv"],
    ))

    published_offerings = {r.get("offering_id", "").strip() for r in publications if r.get("status", "").strip() == "published"}
    untracked_publication = [
        r for r in offerings
        if r.get("offering_id", "").strip()
        and r.get("offering_id", "").strip() not in {
            x.get("offering_id", "").strip() for x in publications
        }
    ]
    signals.append(signal(
        "REG-PUB-001", "edition", "2026", "offerings_have_publication_state",
        "warning" if untracked_publication else "ok",
        "Publicatiestatus",
        f"{len(untracked_publication)} offering(s) hebben nog geen publicatiestatus."
        if untracked_publication else "Alle offerings hebben een publicatiestatus.",
        len(untracked_publication), 0,
        ["data/2026/offerings.csv", "data/2026/publication_status.csv"],
    ))

    no_cohort_counts = not cohorts or any(not r.get("student_count", "").strip() for r in cohorts)
    signals.append(signal(
        "CAP-POP-001", "edition", "2026", "cohort_counts_known",
        "unknown" if no_cohort_counts else "ok",
        "Leerlingaantallen",
        "Capaciteit kan nog niet volledig worden beoordeeld: leerlingaantallen zijn niet compleet."
        if no_cohort_counts else "Leerlingaantallen zijn beschikbaar voor capaciteitsberekeningen.",
        None if no_cohort_counts else sum(int(float(r["student_count"])) for r in cohorts if r.get("student_count", "").strip()),
        "alle relevante cohorten hebben student_count",
        ["data/2026/cohorts.csv"],
    ))

    for build in ("ob", "bb"):
        key = f"capacity_safety_margin_{build}"
        value = cfg.get(key)
        signals.append(signal(
            f"CAP-MARGIN-{build.upper()}",
            "edition", "2026", f"{build}_safety_margin_configured",
            "unknown" if value is None else "ok",
            f"Veiligheidsmarge {build.upper()}",
            f"De veiligheidsmarge voor {build.upper()} is nog niet vastgesteld."
            if value is None else f"Veiligheidsmarge {build.upper()} is ingesteld op {value}.",
            value,
            "door organisatie vastgestelde grens",
            ["config/2026_dashboard.json"],
        ))

    no_assignments = bool(offerings) and not assignments
    signals.append(signal(
        "RES-STAFF-001", "edition", "2026", "staff_assignment_coverage",
        "unknown" if no_assignments else "ok",
        "Begeleiding",
        "Er zijn offerings maar nog geen personele assignments; dekking is nog niet beoordeelbaar."
        if no_assignments else "Personele assignments zijn aanwezig of er zijn nog geen offerings.",
        len(assignments),
        "begeleidingsnorm nog te bevestigen",
        ["data/2026/assignments.csv", "data/2026/offerings.csv"],
    ))

    payload = {
        "edition": "2026",
        "calculated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "activities": len(activities),
            "offerings": len(offerings),
            "published_offerings": len(published_offerings),
            "rooms": len(rooms),
            "assignments": len(assignments),
            "external_records": len(external),
        },
        "signals": signals,
    }

    out = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(out, encoding="utf-8")
    else:
        print(out, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
