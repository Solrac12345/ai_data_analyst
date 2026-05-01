# EN: Unit tests for the supervisor graph structure and flow
# FR: Tests unitaires pour la structure du graphe superviseur

from src.core.supervisor import supervisor_graph


def test_graph_has_expected_nodes() -> None:
    """Verify all agent nodes are registered in the graph."""
    nodes = supervisor_graph.nodes.keys()
    assert "load" in nodes
    assert "clean" in nodes
    assert "analyze" in nodes
    assert "visualize" in nodes


def test_graph_is_compiled() -> None:
    """Test that the graph is compiled and has valid structure."""
    assert supervisor_graph is not None
    assert hasattr(supervisor_graph, "nodes")
    # LangGraph automatically adds a '__start__' node, so total is 5
    assert len(supervisor_graph.nodes) == 5
