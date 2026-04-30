# Agent responsible for loading data from CSV, Excel, or other sources

import pandas as pd
from pathlib import Path
from src.core.state import AnalysisState
from src.agents.base import BaseAgent


class DataLoaderAgent(BaseAgent[AnalysisState]):
    """Loads data from file paths into a pandas DataFrame."""

    def __init__(self) -> None:
        super().__init__(name="DataLoaderAgent")

    def execute(self, state: AnalysisState) -> AnalysisState:
        """Load data from state.data_path into state.raw_data."""
        if state.data_path is None:
            state.add_error("No data_path specified in state")
            return state

        try:
            path = Path(state.data_path)
            self.log(f"Loading data from {path}")

            if path.suffix.lower() == ".csv":
                df = pd.read_csv(path, encoding="utf-8")
            elif path.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(path, engine="openpyxl")
            else:
                state.add_error(f"Unsupported file format: {path.suffix}")
                return state

            state.raw_data = df
            state.data_path = str(path)
            self.log(f"Loaded {len(df)} rows, {len(df.columns)} columns")
            return state

        except FileNotFoundError:
            state.add_error(f"File not found: {state.data_path}")
            return state
        except Exception as e:
            state.add_error(f"Error loading data: {str(e)}")
            return state
