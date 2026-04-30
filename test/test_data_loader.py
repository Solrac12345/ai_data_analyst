# Unit tests for DataLoaderAgent

import pandas as pd
from src.core.state import AnalysisState
from src.agents.data_loader import DataLoaderAgent


def test_load_csv_success(tmp_path):
    """Test successful CSV loading."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("a,b,c\n1,2,3\n4,5,6")

    state = AnalysisState(data_path=str(csv_file))
    agent = DataLoaderAgent()
    result = agent.execute(state)

    assert result.raw_data is not None
    assert len(result.raw_data) == 2
    assert list(result.raw_data.columns) == ["a", "b", "c"]


def test_load_excel_success(tmp_path):
    """Test successful Excel loading."""
    excel_file = tmp_path / "test.xlsx"
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    df.to_excel(excel_file, index=False)

    state = AnalysisState(data_path=str(excel_file))
    agent = DataLoaderAgent()
    result = agent.execute(state)

    assert result.raw_data is not None
    assert len(result.raw_data) == 2


def test_load_missing_file():
    """Test error handling for missing file."""
    state = AnalysisState(data_path="nonexistent.csv")
    agent = DataLoaderAgent()
    result = agent.execute(state)

    assert not result.is_valid()
    assert any("not found" in err for err in result.errors)


def test_load_unsupported_format(tmp_path):
    """Test error handling for unsupported file format."""
    txt_file = tmp_path / "data.txt"
    txt_file.write_text("plain text")

    state = AnalysisState(data_path=str(txt_file))
    agent = DataLoaderAgent()
    result = agent.execute(state)

    assert not result.is_valid()
    assert any("Unsupported file format" in err for err in result.errors)
