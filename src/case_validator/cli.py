"""Command-line entry point."""

from __future__ import annotations

import argparse

from .batch import validate_file, write_csv


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="case-validator", description="Validate a case batch before bulk update.")
    p.add_argument("csv")
    p.add_argument("--clean-out", default="clean_cases.csv")
    p.add_argument("--errors-out", default="errors.csv")
    args = p.parse_args(argv)
    result = validate_file(args.csv)
    write_csv(result.clean, args.clean_out)
    write_csv(result.errors, args.errors_out)
    print(result.summary)
    for e in result.errors:
        print(f"  row {e['row']} {e['case_id'] or '(no id)'}: {e['error']}")
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
