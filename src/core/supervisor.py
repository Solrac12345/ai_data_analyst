# Builds the LangGraph state machine that routes execution between agents

from typing import Literal
from langgraph.graph import StateGraph, END
from .state import AnalysisState


def route_next_step(
    state: AnalysisState,
) -> Literal["clean", "analyze", "visualize", "end"]:
    """
    Determine the next node to execute based on state completion flags.
    Linear progression: load -> clean -> analyze -> visualize -> end
    """
    if state.raw_data is not None and state.clean_data is None:
        return "clean"
    elif state.clean_data is not None and state.summary_stats is None:
        return "analyze"
    elif state.summary_stats is not None and not state.plots_code:
        return "visualize"
    else:
        return "end"


def create_supervisor_graph() -> StateGraph:
    """
    Construct and compile the LangGraph workflow.
    Agent nodes are registered as placeholders; actual logic attaches in Phase 2.
    """
    workflow = StateGraph(AnalysisState)

    # Placeholder nodes (will be replaced with actual agent callables)
    workflow.add_node("clean", lambda s: s)
    workflow.add_node("analyze", lambda s: s)
    workflow.add_node("visualize", lambda s: s)

    # Conditional routing from start
    workflow.add_conditional_edges(
        "__start__",
        route_next_step,
        {
            "clean": "clean",
            "analyze": "analyze",
            "visualize": "visualize",
            "end": END,
        },
    )

    # Linear chaining after conditional entry
    workflow.add_edge("clean", "analyze")
    workflow.add_edge("analyze", "visualize")
    workflow.add_edge("visualize", END)

    return workflow.compile()


# Pre-compiled graph instance for reuse
supervisor_graph = create_supervisor_graph()
