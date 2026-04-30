# Unit tests for CleaningAgent

import pandas as pd
from src.core.state import AnalysisState
from src.agents.cleaning import CleaningAgent


def test_remove_duplicates():
    """Test duplicate row removal."""
    df = pd.DataFrame({"a": [1, 1, 2], "b": [3, 3, 4]})
    state = AnalysisState(raw_data=df)
    agent = CleaningAgent()
    result = agent.execute(state)

    assert len(result.clean_data) == 2
    assert result.cleaning_report["duplicates_removed"] == 1


def test_fill_missing_mean():
    """Test missing value filling with mean strategy."""
    df = pd.DataFrame({"x": [1, 2, None, 4]})
    state = AnalysisState(raw_data=df)
    agent = CleaningAgent()
    result = agent.execute(state)

    assert result.clean_data["x"].isnull().sum() == 0
    assert result.cleaning_report.get("missing_filled") is True


def test_drop_missing_strategy(monkeypatch):
    """Test row dropping for missing values."""
    df = pd.DataFrame({"x": [1, None, 3], "y": [4, 5, 6]})
    state = AnalysisState(raw_data=df)
    # Patch the singleton setting directly in the agent's module
    monkeypatch.setattr("src.agents.cleaning.settings.cleaning.fill_missing", "drop")

    agent = CleaningAgent()
    result = agent.execute(state)

    assert len(result.clean_data) == 2
    assert result.cleaning_report.get("rows_dropped_for_missing") == 1


def test_outlier_removal(monkeypatch):
    """Test Z-score based outlier removal."""
    # EN: Use unique values so drop_duplicates() doesn't interfere
    # FR: Utiliser des valeurs uniques pour éviter l'interférence de drop_duplicates()
    df = pd.DataFrame({"val": [10, 11, 12, 13, 100]})
    state = AnalysisState(raw_data=df)

    # Lower threshold to reliably flag 100 as an outlier
    monkeypatch.setattr("src.agents.cleaning.settings.cleaning.outlier_threshold", 1.5)

    agent = CleaningAgent()
    result = agent.execute(state)

    # EN: 100 is the outlier; 4 unique valid rows should remain
    # FR: 100 est l'outlier ; 4 lignes valides uniques doivent rester
    assert len(result.clean_data) == 4
    assert 100 not in result.clean_data["val"].values
