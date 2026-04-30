# Agent responsible for data cleaning and preprocessing

import pandas as pd
import numpy as np
from typing import Any
from config.settings import settings
from src.core.state import AnalysisState
from src.agents.base import BaseAgent


class CleaningAgent(BaseAgent[AnalysisState]):
    """Applies configurable cleaning operations to the raw DataFrame."""

    def __init__(self) -> None:
        super().__init__(name="CleaningAgent")

    def execute(self, state: AnalysisState) -> AnalysisState:
        """Apply cleaning operations to state.raw_data -> state.clean_data."""
        if state.raw_data is None:
            state.add_error("No raw_data to clean")
            return state

        df: pd.DataFrame = state.raw_data.copy()
        report: dict[str, Any] = {}

        if settings.cleaning.drop_duplicates:
            before = len(df)
            df = df.drop_duplicates()
            report["duplicates_removed"] = before - len(df)
            self.log(f"Removed {report['duplicates_removed']} duplicate rows")

        strategy = settings.cleaning.fill_missing
        if strategy != "drop":
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if df[col].isnull().any():
                    if strategy == "mean":
                        df[col] = df[col].fillna(df[col].mean())
                    elif strategy == "median":
                        df[col] = df[col].fillna(df[col].median())
                    elif strategy == "mode":
                        mode_val = df[col].mode()
                        if len(mode_val) > 0:
                            df[col] = df[col].fillna(mode_val[0])
            report["missing_filled"] = True
            self.log(f"Filled missing values using strategy: {strategy}")
        else:
            before = len(df)
            df = df.dropna()
            report["rows_dropped_for_missing"] = before - len(df)
            self.log(
                f"Dropped {report['rows_dropped_for_missing']} rows with missing values"
            )

        threshold = settings.cleaning.outlier_threshold
        if threshold and len(df.select_dtypes(include=[np.number]).columns) > 0:
            numeric_df = df.select_dtypes(include=[np.number])
            if len(numeric_df) > 1:
                z_scores = np.abs((numeric_df - numeric_df.mean()) / numeric_df.std())
                mask = (z_scores < threshold).all(axis=1)
                before = len(df)
                df = df[mask]  # type: ignore[assignment]
                report["outliers_removed"] = before - len(df)
                self.log(
                    f"Removed {report['outliers_removed']} outliers (Z-score > {threshold})"
                )

        state.clean_data = df
        state.cleaning_report = report
        return state
