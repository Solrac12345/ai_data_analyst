# EN: Agent responsible for statistical analysis and insight generation
# FR: Agent responsable de l'analyse statistique et de la génération d'insights

import pandas as pd
import numpy as np
from typing import Any
from config.settings import settings
from src.core.state import AnalysisState
from src.agents.base import BaseAgent


class AnalysisAgent(BaseAgent[AnalysisState]):
    """
    Performs statistical analysis on cleaned data.
    Computes descriptive statistics, correlation matrices, and generates insights.
    """

    def __init__(self) -> None:
        super().__init__(name="AnalysisAgent")

    def execute(self, state: AnalysisState) -> AnalysisState:
        """Analyze state.clean_data -> populate summary_stats, correlations, insights."""
        if state.clean_data is None:
            state.add_error("No clean_data available for analysis")
            return state

        df: pd.DataFrame = (
            state.clean_data
        )  # EN: Removed unused type: ignore / FR: Ignore supprimé
        stats: dict[str, Any] = {}
        correlations: dict[str, Any] = {}
        insights: list[str] = []

        try:
            # 1. Descriptive Statistics
            numeric_df = df.select_dtypes(include=[np.number])
            if not numeric_df.empty:
                # EN: pandas-stubs returns dict[Hashable, Any] / FR: pandas-stubs renvoie dict[Hashable, Any]
                stats = numeric_df.describe().to_dict()  # type: ignore[assignment]
                self.log(
                    f"Computed descriptive statistics for {len(numeric_df.columns)} numeric columns"
                )

            # 2. Correlation Matrix
            if len(numeric_df.columns) > 1:
                method = settings.analysis.correlation_method
                corr_matrix = numeric_df.corr(method=method)
                # EN: pandas-stubs returns dict[Hashable, Any] / FR: pandas-stubs renvoie dict[Hashable, Any]
                correlations = corr_matrix.to_dict()  # type: ignore[assignment]
                self.log(f"Computed {method} correlation matrix")

            # 3. Generate Insights
            insights = self._generate_insights(df, numeric_df, correlations)
            state.summary_stats = stats
            state.correlations = correlations
            state.insights = insights[: settings.analysis.top_insights]
            self.log(f"Generated {len(state.insights)} insights")

        except Exception as e:
            state.add_error(f"Analysis failed: {str(e)}")
            self.log(f"Error during analysis: {str(e)}", level="ERROR")

        return state

    def _generate_insights(
        self, df: pd.DataFrame, numeric_df: pd.DataFrame, corr: dict[str, Any]
    ) -> list[str]:
        """Generate simple, actionable insights from the data."""
        insights: list[str] = []

        insights.append(
            f"Dataset contains {len(df)} rows and {len(df.columns)} columns."
        )

        if not numeric_df.empty:
            insights.append(
                f"Found {len(numeric_df.columns)} numeric columns suitable for analysis."
            )

        if corr:
            max_corr = 0.0
            max_pair = ("", "")
            for col1, values in corr.items():
                for col2, val in values.items():
                    if col1 != col2 and abs(val) > abs(max_corr):
                        max_corr = val
                        max_pair = (col1, col2)
            if max_pair[0] and abs(max_corr) > 0.5:
                insights.append(
                    f"Strong {'positive' if max_corr > 0 else 'negative'} correlation detected "
                    f"between '{max_pair[0]}' and '{max_pair[1]}' (r={max_corr:.2f})."
                )

        missing_counts = df.isnull().sum()
        if missing_counts.any():
            col_with_most_missing = missing_counts.idxmax()
            insights.append(
                f"Column '{col_with_most_missing}' has {missing_counts.max()} remaining missing values."
            )

        return insights
