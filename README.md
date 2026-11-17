# case-batch-validator

Checks a batch of meter-exchange service cases **before** it is pushed into a CRM or billing system in bulk. Clean rows go to one file, every problem goes to an error report with the row number, so nothing bad reaches the target system and nothing good is held back.

It reflects the validation step I built into a bulk case-update automation in residential energy operations.

## Run it

```bash
pip install -e ".[dev]"
case-validator data/sample_cases.csv --clean-out clean_cases.csv --errors-out errors.csv
```

```
7 rows: 2 clean, 5 rejected
  row 4 C-003: old and new meter IDs are the same
  row 5 C-004: new_meter_id 'LGZ5555' must be 3 capital letters and 8 digits
  row 6 C-005: completed_date is before scheduled_date
  row 7 C-001: duplicate case_id C-001
  row 8 C-006: final_reading_kwh 'n/a' is not a number
```

The exit code is `1` when any row is rejected, so it can gate a pipeline step.

## Rules

| rule | checks |
|---|---|
| case ID | present, and not repeated in the batch (the first occurrence wins) |
| meter IDs | old and new both match `AAA00000000`, and differ |
| status | one of `scheduled`, `completed`, `cancelled` |
| dates | `scheduled_date` valid; a completed case needs a `completed_date` on or after it |
| reading | a completed case needs a non-negative numeric `final_reading_kwh` |

Each rule is a small function in `src/case_validator/rules.py`, so adding one is a single function and a test.

## Tests

```bash
pytest -q
```

GitHub Actions runs the suite on Python 3.10 and 3.12.
