#!/usr/bin/env python3
"""Build a deterministic dashboard demo from input facts, not hand-set colors."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "dashboard" / "demo_scenario.json"


def severity_for_margin(margin: int, safety: int) -> str:
    if margin < 0:
        return "critical"
    if margin < safety:
        return "warning"
    return "ok"


def build_capacity_signal(slot, build: str, safety: int):
    values = slot[build]
    demand = int(values["demand"])
    before = int(values["supply_before"])
    change = int(values.get("change", 0))
    after = before + change
    margin_before = before - demand
    margin_after = after - demand
    return {
        "signal_id": f"DEMO-CAP-{slot['slot_id']}-{build.upper()}",
        "scope_type": "slot",
        "scope_id": slot["slot_id"],
        "rule_id": f"{build}_capacity_margin",
        "severity": severity_for_margin(margin_after, safety),
        "title": f"{slot['label']} · {build.upper()}",
        "explanation": (
            f"Vraag {demand}, aanbod {after}, marge {margin_after:+d}. "
            f"Veiligheidsdoel in deze demo: {safety} plaatsen."
        ),
        "observed_value": margin_after,
        "threshold_or_expectation": safety,
        "source_refs": ["dashboard/demo_scenario.json"],
        "metrics": {
            "demand": demand,
            "supply_before": before,
            "supply_after": after,
            "change": change,
            "margin_before": margin_before,
            "margin_after": margin_after,
        },
    }


def workflow_signal(signal_id, title, value, severity, explanation):
    return {
        "signal_id": signal_id,
        "scope_type": "edition",
        "scope_id": "2026-demo",
        "rule_id": signal_id.lower().replace("-", "_"),
        "severity": severity,
        "title": title,
        "explanation": explanation,
        "observed_value": value,
        "threshold_or_expectation": 0,
        "source_refs": ["dashboard/demo_scenario.json"],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(DEFAULT_INPUT))
    p.add_argument("--output", required=True)
    args = p.parse_args()

    src = json.loads(Path(args.input).read_text(encoding="utf-8"))
    signals = []

    safety = src["capacity_safety_margin"]
    for slot in src["slots"]:
        signals.append(build_capacity_signal(slot, "ob", int(safety["ob"])))
        signals.append(build_capacity_signal(slot, "bb", int(safety["bb"])))

    wf = src["workflow"]
    signals.extend([
        workflow_signal(
            "DEMO-REG-EXT", "Buitenom-items", wf["outside_in_unreconciled"],
            "critical" if wf["outside_in_unreconciled"] else "ok",
            f"{wf['outside_in_unreconciled']} item(s) zijn nog niet met de centrale hub gereconcilieerd."
        ),
        workflow_signal(
            "DEMO-REG-ROOM", "Lokalen", wf["offerings_without_room"],
            "warning" if wf["offerings_without_room"] else "ok",
            f"{wf['offerings_without_room']} offering(s) hebben nog geen lokaal."
        ),
        workflow_signal(
            "DEMO-REG-STAFF", "Begeleiding", wf["offerings_without_staff"],
            "warning" if wf["offerings_without_staff"] else "ok",
            f"{wf['offerings_without_staff']} offering(s) hebben nog geen bevestigde begeleiding."
        ),
        workflow_signal(
            "DEMO-REG-WEB", "Website", wf["website_pending"],
            "warning" if wf["website_pending"] else "ok",
            f"{wf['website_pending']} item(s) zijn nog niet publiceerbaar of gepubliceerd."
        ),
        workflow_signal(
            "DEMO-REG-MAG", "Magister", wf["magister_pending"],
            "warning" if wf["magister_pending"] else "ok",
            f"{wf['magister_pending']} Magisterrecord(s) moeten nog worden ingevoerd of gecontroleerd."
        ),
        workflow_signal(
            "DEMO-REG-MAG-CHANGED", "Gewijzigd na Magisterinvoer", wf["magister_changed_after_entry"],
            "critical" if wf["magister_changed_after_entry"] else "ok",
            f"{wf['magister_changed_after_entry']} centraal gewijzigde record(s) vragen opnieuw controle in Magister."
        ),
    ])

    activity_progress = 0.0
    if wf["activities_total"]:
        activity_progress = wf["activities_complete"] / wf["activities_total"]

    payload = {
        "edition": src["edition"],
        "scenario_title": src["scenario_title"],
        "calculated_at": datetime.now(timezone.utc).isoformat(),
        "progress": {
            "activities_total": wf["activities_total"],
            "activities_complete": wf["activities_complete"],
            "activities_fraction": activity_progress,
        },
        "change_event": src["change_event"],
        "signals": signals,
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(signals)} demo dashboard signals")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
