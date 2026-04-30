# Unit tests for the AnalysisState Pydantic model

from src.core.state import AnalysisState


def test_state_initialization():
    """Verify state initializes with correct defaults."""
    state = AnalysisState()
    assert state.current_step == "load"
    assert state.errors == []
    assert state.is_valid() is True


def test_add_error():
    """Test error accumulation toggles validity."""
    state = AnalysisState()
    state.add_error("Missing file")
    assert len(state.errors) == 1
    assert state.is_valid() is False


def test_field_assignment():
    """Test that nested/complex fields accept expected types."""
    state = AnalysisState(
        raw_data={"col": [1, 2]},
        data_path="test.csv",
        cleaning_report={"dropped_rows": 5},
        insights=["High correlation detected"],
    )
    assert state.raw_data is not None
    assert state.raw_data["col"] == [1, 2]
    assert state.data_path == "test.csv"
    assert state.cleaning_report["dropped_rows"] == 5
    assert state.insights[0] == "High correlation detected"
