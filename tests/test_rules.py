from case_validator import rules

GOOD = {"case_id": "C-1", "old_meter_id": "ESY12345678", "new_meter_id": "ESY87654321",
        "status": "completed", "scheduled_date": "2026-11-02", "completed_date": "2026-11-03",
        "final_reading_kwh": "100"}


def test_good_record_passes_every_rule():
    assert [r(GOOD) for r in rules.RULES] == [None] * len(rules.RULES)


def test_bad_meter_format():
    assert "must be 3 capital letters" in rules.check_meter_ids({**GOOD, "new_meter_id": "LGZ5555"})


def test_same_old_and_new_meter():
    assert rules.check_meter_ids({**GOOD, "new_meter_id": GOOD["old_meter_id"]}) == "old and new meter IDs are the same"


def test_completed_before_scheduled():
    assert rules.check_dates({**GOOD, "completed_date": "2026-11-01"}) == "completed_date is before scheduled_date"


def test_scheduled_case_needs_no_reading():
    assert rules.check_reading({**GOOD, "status": "scheduled", "final_reading_kwh": ""}) is None


def test_reading_must_be_number():
    assert "is not a number" in rules.check_reading({**GOOD, "final_reading_kwh": "n/a"})


def test_unknown_status():
    assert "not in" in rules.check_status({**GOOD, "status": "done"})
