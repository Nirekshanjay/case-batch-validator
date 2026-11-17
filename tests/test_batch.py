from pathlib import Path

from case_validator import batch, cli

SAMPLE = Path(__file__).resolve().parents[1] / "data" / "sample_cases.csv"


def test_sample_batch_split():
    result = batch.validate_file(SAMPLE)
    assert [r["case_id"] for r in result.clean] == ["C-001", "C-002"]
    assert {(e["row"], e["case_id"]) for e in result.errors} == {
        (4, "C-003"), (5, "C-004"), (6, "C-005"), (7, "C-001"), (8, "C-006")}
    assert result.summary == "7 rows: 2 clean, 5 rejected"


def test_duplicate_reported_on_later_row_only():
    result = batch.validate_file(SAMPLE)
    dups = [e for e in result.errors if e["error"].startswith("duplicate")]
    assert dups == [{"row": 7, "case_id": "C-001", "error": "duplicate case_id C-001"}]


def test_cli_writes_outputs_and_exit_code(tmp_path, capsys):
    clean, errors = tmp_path / "clean.csv", tmp_path / "errors.csv"
    code = cli.main([str(SAMPLE), "--clean-out", str(clean), "--errors-out", str(errors)])
    assert code == 1
    assert clean.read_text().count("\n") == 3  # header + 2 rows
    assert "row 4 C-003" in capsys.readouterr().out
