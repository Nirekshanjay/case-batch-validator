"""Field rules for one case record. Each rule returns an error message or None."""

from __future__ import annotations

import re
from datetime import date, datetime

METER_ID = re.compile(r"^[A-Z]{3}\d{8}$")
ALLOWED_STATUS = {"scheduled", "completed", "cancelled"}


def _date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def check_case_id(rec: dict) -> str | None:
    return None if rec.get("case_id", "").strip() else "case_id is empty"


def check_meter_ids(rec: dict) -> str | None:
    old, new = rec.get("old_meter_id", "").strip(), rec.get("new_meter_id", "").strip()
    for name, value in (("old_meter_id", old), ("new_meter_id", new)):
        if not METER_ID.match(value):
            return f"{name} {value!r} must be 3 capital letters and 8 digits"
    if old == new:
        return "old and new meter IDs are the same"
    return None


def check_status(rec: dict) -> str | None:
    status = rec.get("status", "").strip().lower()
    return None if status in ALLOWED_STATUS else f"status {status!r} not in {sorted(ALLOWED_STATUS)}"


def check_dates(rec: dict) -> str | None:
    scheduled = _date(rec.get("scheduled_date", "").strip())
    if scheduled is None:
        return "scheduled_date must be YYYY-MM-DD"
    if rec.get("status", "").strip().lower() == "completed":
        done = _date(rec.get("completed_date", "").strip())
        if done is None:
            return "completed case needs completed_date as YYYY-MM-DD"
        if done < scheduled:
            return "completed_date is before scheduled_date"
    return None


def check_reading(rec: dict) -> str | None:
    if rec.get("status", "").strip().lower() != "completed":
        return None
    raw = rec.get("final_reading_kwh", "").strip()
    try:
        value = float(raw)
    except ValueError:
        return f"final_reading_kwh {raw!r} is not a number"
    return "final_reading_kwh is negative" if value < 0 else None


RULES = (check_case_id, check_meter_ids, check_status, check_dates, check_reading)
