# Agent responsible for data cleaning and preprocessing

import numpy as np
from config.settings import settings
from src.core.state import AnalysisState
from src.agents.base import BaseAgent


class CleaningAgent(BaseAgent[AnalysisState]):
    """
    Applies configurable cleaning operations to the raw DataFrame.
    Handles duplicates, missing values, and outlier detection.
    """

    def __init__(self):
        super().__init__(name="CleaningAgent")

    def execute(self, state: AnalysisState) -> AnalysisState:
        """Apply cleaning operations to state.raw_data -> state.clean_data."""
        if state.raw_data is None:
            state.add_error("No raw_data to clean")
            return state

        df = state.raw_data.copy()
        report = {}

        # Remove duplicates if configured
        if settings.cleaning.drop_duplicates:
            before = len(df)
            df = df.drop_duplicates()
            report["duplicates_removed"] = before - len(df)
            self.log(f"Removed {report['duplicates_removed']} duplicate rows")

        # Handle missing values
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
                        df[col] = df[col].fillna(df[col].mode()[0])
            report["missing_filled"] = True
            self.log(f"Filled missing values using strategy: {strategy}")
        else:
            before = len(df)
            df = df.dropna()
            report["rows_dropped_for_missing"] = before - len(df)
            self.log(
                f"Dropped {report['rows_dropped_for_missing']} rows with missing values"
            )

        # Outlier removal using Z-score (optional)
        threshold = settings.cleaning.outlier_threshold
        if threshold and len(df.select_dtypes(include=[np.number]).columns) > 0:
            numeric_df = df.select_dtypes(include=[np.number])
            z_scores = np.abs((numeric_df - numeric_df.mean()) / numeric_df.std())
            mask = (z_scores < threshold).all(axis=1)
            before = len(df)
            df = df[mask]
            report["outliers_removed"] = before - len(df)
            self.log(
                f"Removed {report['outliers_removed']} outliers (Z-score > {threshold})"
            )

        state.clean_data = df
        state.cleaning_report = report
        return state
