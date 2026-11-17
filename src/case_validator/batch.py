"""Split a CSV batch into clean cases and an error report."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from .rules import RULES


@dataclass
class Result:
    clean: list[dict] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)

    @property
    def summary(self) -> str:
        total = len(self.clean) + len({e["row"] for e in self.errors})
        return f"{total} rows: {len(self.clean)} clean, {total - len(self.clean)} rejected"


def validate_rows(rows: list[dict]) -> Result:
    """Apply every rule to every row. Duplicate case IDs after the first are rejected."""
    result, seen = Result(), set()
    for row_no, rec in enumerate(rows, start=2):
        problems = [msg for rule in RULES if (msg := rule(rec))]
        case_id = rec.get("case_id", "").strip()
        if case_id and case_id in seen:
            problems.append(f"duplicate case_id {case_id}")
        seen.add(case_id)
        if problems:
            result.errors += [{"row": row_no, "case_id": case_id, "error": p} for p in problems]
        else:
            result.clean.append(rec)
    return result


def validate_file(path: str | Path) -> Result:
    with open(path, newline="", encoding="utf-8") as fh:
        return validate_rows(list(csv.DictReader(fh)))


def write_csv(rows: list[dict], path: str | Path) -> None:
    if not rows:
        Path(path).write_text("")
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
