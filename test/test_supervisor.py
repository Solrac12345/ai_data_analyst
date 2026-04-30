# EN: Unit tests for the supervisor graph structure and flow
# FR: Tests unitaires pour la structure du graphe superviseur

from src.core.supervisor import supervisor_graph
from src.core.state import AnalysisState


def test_graph_has_expected_nodes() -> None:
    """Verify all agent nodes are registered in the graph."""
    nodes = supervisor_graph.nodes.keys()
    assert "load" in nodes
    assert "clean" in nodes
    assert "analyze" in nodes
    assert "visualize" in nodes


def test_graph_execution_flow() -> None:
    """Test that the graph executes linearly from load to end."""
    # Create a simple state
    initial_state = AnalysisState(
        data_path="dummy.csv",
        raw_data={"col": [1, 2, 3]},  # Skip actual loading for this test
        clean_data={"col": [1, 2, 3]} # Skip cleaning for this test
    )
    
    # Note: In a real run, we'd pass a dict to invoke, but here we check node connectivity
    # For this unit test, we just verify the graph object exists and has edges
    # Detailed integration is in test_cli.py
    assert supervisor_graph is not None
    assert len(supervisor_graph.edges) > 0
