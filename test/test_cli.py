# EN: Unit tests for CLI entrypoint
# FR: Tests unitaires pour le point d'entrée CLI

import pandas as pd
from pathlib import Path
from typer.testing import CliRunner

from src.cli.main import app

runner = CliRunner()


def test_analyze_command_success(tmp_path: Path) -> None:
    """Test successful CLI run with valid data."""
    csv_file = tmp_path / "data.csv"
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    df.to_csv(csv_file, index=False)

    report_file = tmp_path / "report.html"
    result = runner.invoke(app, ["--path", str(csv_file), "--report", str(report_file)])

    assert result.exit_code == 0
    assert "Starting Analysis" in result.output
    assert "Report saved to" in result.output
    assert report_file.exists(), "Expected report.html to be created"


def test_analyze_command_missing_file() -> None:
    """Test CLI run with missing file."""
    result = runner.invoke(app, ["--path", "nonexistent.csv"])

    assert result.exit_code == 0
    assert "Errors found" in result.output
