# Orchestrates agent execution using LangGraph state machine pattern

from typing import Any
from langgraph.graph import StateGraph, END
from .state import AnalysisState
from src.agents.data_loader import DataLoaderAgent
from src.agents.cleaning import CleaningAgent
from src.agents.analysis import AnalysisAgent
from src.agents.viz import VizAgent


def create_supervisor_graph() -> Any:
    """Build and compile a strict linear LangGraph workflow."""
    workflow = StateGraph(AnalysisState)

    workflow.add_node("load", DataLoaderAgent().execute)
    workflow.add_node("clean", CleaningAgent().execute)
    workflow.add_node("analyze", AnalysisAgent().execute)
    workflow.add_node("visualize", VizAgent().execute)

    workflow.set_entry_point("load")
    workflow.add_edge("load", "clean")
    workflow.add_edge("clean", "analyze")
    workflow.add_edge("analyze", "visualize")
    workflow.add_edge("visualize", END)

    return workflow.compile()


supervisor_graph = create_supervisor_graph()
