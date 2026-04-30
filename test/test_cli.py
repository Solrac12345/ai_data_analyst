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

    result = runner.invoke(app, [str(csv_file)])

    assert result.exit_code == 0
    assert result.exception is None
    assert "Starting Analysis" in result.output
    # EN: Check for successful completion marker / FR: Vérifier le marqueur de fin réussie
    assert "Visualizations saved to" in result.output or "Insights" in result.output


def test_analyze_command_missing_file() -> None:
    """Test CLI run with missing file."""
    result = runner.invoke(app, ["nonexistent.csv"])

    assert result.exit_code == 0
    assert "Errors found" in result.output
