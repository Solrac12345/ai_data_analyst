# EN: Agent responsible for generating visualization code and paths
# FR: Agent responsable de la génération de code de visualisation et des chemins

import pandas as pd
import numpy as np
from config.settings import settings
from src.core.state import AnalysisState
from src.agents.base import BaseAgent


class VizAgent(BaseAgent[AnalysisState]):
    """
    Generates visualization code snippets for the first numeric column found.
    Supports Matplotlib and Plotly based on configuration.
    """

    def __init__(self) -> None:
        super().__init__(name="VizAgent")

    def execute(self, state: AnalysisState) -> AnalysisState:
        """Generate viz code for state.clean_data -> populate plots_code, plot_paths."""
        if state.clean_data is None:
            state.add_error("No clean_data available for visualization")
            return state

        df: pd.DataFrame = (
            state.clean_data
        )  # EN: Removed unused type: ignore / FR: Ignore supprimé
        numeric_df = df.select_dtypes(include=[np.number])

        if numeric_df.empty:
            self.log("No numeric columns found for visualization")
            return state

        col = numeric_df.columns[0]
        library = settings.visualization.library

        code = ""
        path = ""

        try:
            if library == "matplotlib":
                code = (
                    f"import matplotlib.pyplot as plt\n"
                    f"plt.figure(figsize=(10, 6))\n"
                    f"plt.hist(df['{col}'], bins=10, color='skyblue', edgecolor='black')\n"
                    f"plt.title(f'Distribution of {{col}}')\n"
                    f"plt.xlabel('{col}')\n"
                    f"plt.ylabel('Frequency')\n"
                    f"plt.savefig('output/plots/hist_{col}.png', bbox_inches='tight')\n"
                    f"plt.show()"
                )
                path = f"output/plots/hist_{col}.png"

            elif library == "plotly":
                code = (
                    f"import plotly.express as px\n"
                    f"fig = px.histogram(df, x='{col}', title=f'Distribution of {{col}}')\n"
                    f"fig.update_layout(bargap=0.1)\n"
                    f"fig.show()\n"
                    f"fig.write_html('output/plots/hist_{col}.html')"
                )
                path = f"output/plots/hist_{col}.html"

            else:
                state.add_error(f"Unsupported visualization library: {library}")
                return state

            state.plots_code.append(code)
            state.plot_paths.append(path)
            self.log(f"Generated {library} visualization code for '{col}'")

        except Exception as e:
            state.add_error(f"Visualization generation failed: {str(e)}")
            self.log(f"Error during viz generation: {str(e)}", level="ERROR")

        return state
