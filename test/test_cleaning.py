# Unit tests for CleaningAgent

import pandas as pd
from typing import Any, cast
from src.core.state import AnalysisState
from src.agents.cleaning import CleaningAgent


def test_remove_duplicates() -> None:
    """Test duplicate row removal."""
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    state = AnalysisState(raw_data=df)
    agent = CleaningAgent()
    result = agent.execute(state)

    assert result.clean_data is not None
    clean_df = cast(pd.DataFrame, result.clean_data)
    assert len(clean_df) == 2
    assert result.cleaning_report["duplicates_removed"] == 1


def test_fill_missing_mean() -> None:
    """Test missing value filling with mean strategy."""
    df = pd.DataFrame({"x": [1, 2, None, 4]})
    state = AnalysisState(raw_data=df)
    agent = CleaningAgent()
    result = agent.execute(state)

    assert result.clean_data is not None
    clean_df = cast(pd.DataFrame, result.clean_data)
    assert clean_df["x"].isnull().sum() == 0
    assert result.cleaning_report.get("missing_filled") is True


def test_drop_missing_strategy(monkeypatch: Any) -> None:
    """Test row dropping for missing values."""
    df = pd.DataFrame({"x": [1, None, 3], "y": [4, 5, 6]})
    state = AnalysisState(raw_data=df)
    monkeypatch.setattr("src.agents.cleaning.settings.cleaning.fill_missing", "drop")

    agent = CleaningAgent()
    result = agent.execute(state)

    assert result.clean_data is not None
    clean_df = cast(pd.DataFrame, result.clean_data)
    assert len(clean_df) == 2
    assert result.cleaning_report.get("rows_dropped_for_missing") == 1


def test_outlier_removal(monkeypatch: Any) -> None:
    """Test Z-score based outlier removal."""
    df = pd.DataFrame({"val": [10, 11, 12, 13, 100]})
    state = AnalysisState(raw_data=df)
    monkeypatch.setattr("src.agents.cleaning.settings.cleaning.outlier_threshold", 1.5)

    agent = CleaningAgent()
    result = agent.execute(state)

    assert result.clean_data is not None
    clean_df = cast(pd.DataFrame, result.clean_data)
    assert len(clean_df) == 4
    assert 100 not in clean_df["val"].values
