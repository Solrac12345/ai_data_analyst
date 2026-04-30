# Orchestrates agent execution using LangGraph state machine pattern

from typing import Literal
from langgraph.graph import StateGraph, END
from .state import AnalysisState
from src.agents.data_loader import DataLoaderAgent
from src.agents.cleaning import CleaningAgent


def route_with_load(state: AnalysisState) -> Literal["load", "clean", "analyze", "visualize", "end"]:
    """
    Determine the next node based on state completion.
    Logic: If path exists but no data -> Load. If data exists but not clean -> Clean. Etc.
    """
    if state.raw_data is None and state.data_path is not None:
        return "load"
    elif state.raw_data is not None and state.clean_data is None:
        return "clean"
    elif state.clean_data is not None and state.summary_stats is None:
        return "analyze"
    elif state.summary_stats is not None and not state.plots_code:
        return "visualize"
    else:
        return "end"


def create_supervisor_graph() -> StateGraph:
    """
    Build and compile the LangGraph workflow with real agents.
    """
    workflow = StateGraph(AnalysisState)
    
    # Initialize real agents
    loader = DataLoaderAgent()
    cleaner = CleaningAgent()
    
    # Register nodes
    workflow.add_node("load", loader.execute)
    workflow.add_node("clean", cleaner.execute)
    workflow.add_node("analyze", lambda s: s)      # Placeholder for Phase 3
    workflow.add_node("visualize", lambda s: s)    # Placeholder for Phase 3
    
    # Define conditional routing from start
    workflow.add_conditional_edges(
        "__start__",
        route_with_load,
        {
            "load": "load",
            "clean": "clean",
            "analyze": "analyze",
            "visualize": "visualize",
            "end": END,
        },
    )
    
    # Chain nodes linearly after entry
    workflow.add_edge("load", "clean")
    workflow.add_edge("clean", "analyze")
    workflow.add_edge("analyze", "visualize")
    workflow.add_edge("visualize", END)
    
    return workflow.compile()


# Global graph instance
supervisor_graph = create_supervisor_graph()
