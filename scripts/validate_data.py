#!/usr/bin/env python3
"""Lightweight structural validator for Pantarijnweek CSV data."""

from __future__ import annotations

import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "2026"

FILES = {
    "time_slots": ("time_slots.csv", ["slot_id", "day", "part", "sequence", "start_time", "end_time"]),
    "activities": ("activities.csv", ["activity_id", "title", "description", "categories", "default_audience", "delivery_type", "external", "requirements", "status"]),
    "offerings": ("offerings.csv", ["offering_id", "activity_id", "slot_id", "audience", "capacity_ob", "capacity_bb", "choice_mode", "mandatory_target", "location_id", "room_id", "budget_eur", "status", "notes"]),
    "cohorts": ("cohorts.csv", ["cohort_id", "year", "track", "location", "build", "student_count"]),
    "locations": ("locations.csv", ["location_id", "name", "kind", "address_or_meeting_point", "external", "notes"]),
    "rooms": ("rooms.csv", ["room_id", "location_id", "name", "type", "capacity", "exclusive", "notes"]),
    "people": ("people.csv", ["person_id", "role_type", "active"]),
    "staff_availability": ("staff_availability.csv", ["person_id", "slot_id", "availability", "note"]),
    "assignments": ("assignments.csv", ["assignment_id", "person_id", "offering_id", "slot_id", "role", "status"]),
    "fixed_activities": ("fixed_activities.csv", ["fixed_activity_id", "title", "slot_id", "cohort_id", "participation_mode", "student_count", "location_id", "room_id", "status", "notes"]),
    "publication_status": ("publication_status.csv", ["offering_id", "channel", "status", "note"]),
    "budget": ("budget.csv", ["budget_item_id", "offering_id", "amount_eur", "status", "note"]),
    "external_system_records": ("external_system_records.csv", ["external_record_id", "system", "route", "offering_id", "fixed_activity_id", "external_key", "title_snapshot", "slot_snapshot", "capacity_snapshot", "participant_count_snapshot", "source", "secure_evidence_ref", "status", "captured_at", "verified_at"]),
}

PRIMARY_KEYS = {
    "time_slots": "slot_id",
    "activities": "activity_id",
    "offerings": "offering_id",
    "cohorts": "cohort_id",
    "locations": "location_id",
    "rooms": "room_id",
    "people": "person_id",
    "assignments": "assignment_id",
    "fixed_activities": "fixed_activity_id",
    "budget": "budget_item_id",
    "external_system_records": "external_record_id",
}

VALID = {
    "availability": {"available", "unavailable", "constrained", "unknown", ""},
    "choice_mode": {"choice", "mandatory", "preregistration", "fixed", ""},
    "participation_mode": {"mandatory", "preregistration", "optional", "unknown", ""},
    "channel": {"website", "magister", "zermelo", ""},
    "publication_status": {"not_ready", "ready", "published", "removed", "blocked", ""},
    "external_system": {"magister", "other", ""},
    "external_route": {"magister_choice", "magister_activity", "manual", "other", ""},
    "external_source": {"manual_quick_capture", "export", "screenshot", "photo", ""},
    "reconciliation_status": {"captured", "unreconciled", "matched", "created", "verified", "superseded", ""},
}

def read_csv(name: str):
    filename, required = FILES[name]
    path = DATA / filename
    if not path.exists():
        raise ValueError(f"missing file: {path.relative_to(ROOT)}")
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        missing = [h for h in required if h not in headers]
        if missing:
            raise ValueError(f"{filename}: missing columns {missing}")
        return list(reader)

def unique_key(name, rows, key, errors):
    seen = set()
    for line, row in enumerate(rows, 2):
        value = row.get(key, "").strip()
        if not value:
            errors.append(f"{name}:{line}: empty {key}")
        elif value in seen:
            errors.append(f"{name}:{line}: duplicate {key}={value}")
        seen.add(value)
    return seen

def number(value, label, errors, allow_blank=True):
    value = value.strip()
    if not value and allow_blank:
        return
    try:
        if float(value) < 0:
            errors.append(f"{label}: negative value {value}")
    except ValueError:
        errors.append(f"{label}: not numeric: {value}")


def parse_time(value, label, errors):
    value = value.strip()
    if not value:
        errors.append(f"{label}: empty time")
        return None
    try:
        return datetime.strptime(value, "%H:%M")
    except ValueError:
        errors.append(f"{label}: invalid HH:MM time: {value}")
        return None

def main() -> int:
    errors = []
    data = {}
    try:
        for name in FILES:
            data[name] = read_csv(name)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    ids = {}
    for name, key in PRIMARY_KEYS.items():
        ids[name] = unique_key(name, data[name], key, errors)

    slot_ids = ids["time_slots"]
    activity_ids = ids["activities"]
    offering_ids = ids["offerings"]
    cohort_ids = ids["cohorts"]
    location_ids = ids["locations"]
    room_ids = ids["rooms"]
    person_ids = ids["people"]
    fixed_activity_ids = ids["fixed_activities"]


    expected_times = {
        "ochtend": ("10:00", "12:30"),
        "middag": ("13:15", "15:45"),
    }
    for line, row in enumerate(data["time_slots"], 2):
        part = row["part"].strip().lower()
        start = row["start_time"].strip()
        end = row["end_time"].strip()
        start_dt = parse_time(start, f"time_slots:{line}:start_time", errors)
        end_dt = parse_time(end, f"time_slots:{line}:end_time", errors)
        if start_dt and end_dt:
            minutes = int((end_dt - start_dt).total_seconds() // 60)
            if minutes != 150:
                errors.append(f"time_slots:{line}: expected 150-minute workshop block, got {minutes}")
        if part in expected_times:
            expected_start, expected_end = expected_times[part]
            if start != expected_start or end != expected_end:
                errors.append(
                    f"time_slots:{line}: {part} must be {expected_start}-{expected_end}, got {start}-{end}"
                )

    for line, row in enumerate(data["rooms"], 2):
        loc = row["location_id"].strip()
        if loc and loc not in location_ids:
            errors.append(f"rooms:{line}: unknown location_id={loc}")
        number(row["capacity"], f"rooms:{line}:capacity", errors)

    for line, row in enumerate(data["offerings"], 2):
        if row["activity_id"].strip() not in activity_ids:
            errors.append(f"offerings:{line}: unknown activity_id={row['activity_id']}")
        if row["slot_id"].strip() not in slot_ids:
            errors.append(f"offerings:{line}: unknown slot_id={row['slot_id']}")
        room = row["room_id"].strip()
        loc = row["location_id"].strip()
        if room and room not in room_ids:
            errors.append(f"offerings:{line}: unknown room_id={room}")
        if loc and loc not in location_ids:
            errors.append(f"offerings:{line}: unknown location_id={loc}")
        if row["choice_mode"].strip() not in VALID["choice_mode"]:
            errors.append(f"offerings:{line}: invalid choice_mode={row['choice_mode']}")
        if row["choice_mode"].strip() == "mandatory" and not row["mandatory_target"].strip():
            errors.append(f"offerings:{line}: mandatory offering without mandatory_target")
        number(row["capacity_ob"], f"offerings:{line}:capacity_ob", errors)
        number(row["capacity_bb"], f"offerings:{line}:capacity_bb", errors)
        number(row["budget_eur"], f"offerings:{line}:budget_eur", errors)

    for line, row in enumerate(data["staff_availability"], 2):
        if row["person_id"].strip() not in person_ids:
            errors.append(f"staff_availability:{line}: unknown person_id={row['person_id']}")
        if row["slot_id"].strip() not in slot_ids:
            errors.append(f"staff_availability:{line}: unknown slot_id={row['slot_id']}")
        if row["availability"].strip() not in VALID["availability"]:
            errors.append(f"staff_availability:{line}: invalid availability={row['availability']}")

    assignments_by_person_slot = defaultdict(list)
    for line, row in enumerate(data["assignments"], 2):
        person = row["person_id"].strip()
        offering = row["offering_id"].strip()
        slot = row["slot_id"].strip()
        if person not in person_ids:
            errors.append(f"assignments:{line}: unknown person_id={person}")
        if offering not in offering_ids:
            errors.append(f"assignments:{line}: unknown offering_id={offering}")
        if slot not in slot_ids:
            errors.append(f"assignments:{line}: unknown slot_id={slot}")
        assignments_by_person_slot[(person, slot)].append(line)

    for key, lines in assignments_by_person_slot.items():
        if key[0] and key[1] and len(lines) > 1:
            errors.append(f"assignments: multiple assignments for person/slot {key}: rows {lines}")

    for line, row in enumerate(data["fixed_activities"], 2):
        if row["slot_id"].strip() and row["slot_id"].strip() not in slot_ids:
            errors.append(f"fixed_activities:{line}: unknown slot_id={row['slot_id']}")
        if row["cohort_id"].strip() and row["cohort_id"].strip() not in cohort_ids:
            errors.append(f"fixed_activities:{line}: unknown cohort_id={row['cohort_id']}")
        if row["participation_mode"].strip() not in VALID["participation_mode"]:
            errors.append(f"fixed_activities:{line}: invalid participation_mode={row['participation_mode']}")
        number(row["student_count"], f"fixed_activities:{line}:student_count", errors)

    for line, row in enumerate(data["publication_status"], 2):
        if row["offering_id"].strip() not in offering_ids:
            errors.append(f"publication_status:{line}: unknown offering_id={row['offering_id']}")
        if row["channel"].strip() not in VALID["channel"]:
            errors.append(f"publication_status:{line}: invalid channel={row['channel']}")
        if row["status"].strip() not in VALID["publication_status"]:
            errors.append(f"publication_status:{line}: invalid status={row['status']}")

    for line, row in enumerate(data["budget"], 2):
        if row["offering_id"].strip() and row["offering_id"].strip() not in offering_ids:
            errors.append(f"budget:{line}: unknown offering_id={row['offering_id']}")
        number(row["amount_eur"], f"budget:{line}:amount_eur", errors, allow_blank=False)

    for line, row in enumerate(data["external_system_records"], 2):
        offering = row["offering_id"].strip()
        fixed = row["fixed_activity_id"].strip()
        status = row["status"].strip()
        if offering and offering not in offering_ids:
            errors.append(f"external_system_records:{line}: unknown offering_id={offering}")
        if fixed and fixed not in fixed_activity_ids:
            errors.append(f"external_system_records:{line}: unknown fixed_activity_id={fixed}")
        if offering and fixed:
            errors.append(f"external_system_records:{line}: both offering_id and fixed_activity_id set")
        if status in {"matched", "created", "verified"} and not (offering or fixed):
            errors.append(f"external_system_records:{line}: status={status} requires central match")
        if row["system"].strip() not in VALID["external_system"]:
            errors.append(f"external_system_records:{line}: invalid system={row['system']}")
        if row["route"].strip() not in VALID["external_route"]:
            errors.append(f"external_system_records:{line}: invalid route={row['route']}")
        if row["source"].strip() not in VALID["external_source"]:
            errors.append(f"external_system_records:{line}: invalid source={row['source']}")
        if status not in VALID["reconciliation_status"]:
            errors.append(f"external_system_records:{line}: invalid status={status}")
        number(row["capacity_snapshot"], f"external_system_records:{line}:capacity_snapshot", errors)
        number(row["participant_count_snapshot"], f"external_system_records:{line}:participant_count_snapshot", errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
