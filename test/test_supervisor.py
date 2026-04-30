# Unit tests for the supervisor routing logic

from src.core.supervisor import route_with_load
from src.core.state import AnalysisState


def test_route_start_to_load():
    """When only data_path is set, next step must be load."""
    state = AnalysisState(data_path="test.csv", raw_data=None)
    assert route_with_load(state) == "load"


def test_route_load_to_clean():
    """After raw_data is set, next step must be clean."""
    state = AnalysisState(raw_data={"data": "loaded"}, clean_data=None)
    assert route_with_load(state) == "clean"


def test_route_clean_to_analyze():
    """After clean_data is set, next step must be analyze."""
    state = AnalysisState(clean_data={"clean": True}, summary_stats=None)
    assert route_with_load(state) == "analyze"


def test_route_analyze_to_visualize():
    """After summary_stats is set, next step must be visualize."""
    state = AnalysisState(summary_stats={"mean": 1.0}, plots_code=[])
    assert route_with_load(state) == "visualize"


def test_route_complete_to_end():
    """When plots_code is populated, pipeline ends."""
    state = AnalysisState(plots_code=["plt.show()"])
    assert route_with_load(state) == "end"
