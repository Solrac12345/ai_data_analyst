# EN: HTML report generator using Jinja2 templating engine
# FR: Générateur de rapports HTML utilisant le moteur de template Jinja2

import json
from pathlib import Path
from typing import Optional
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import markdown

from src.core.state import AnalysisState


class ReportGenerator:
    """
    Generates rich HTML reports from AnalysisState.
    Supports Markdown rendering for insights and Plotly integration.
    """

    def __init__(self, template_dir: Optional[str] = None) -> None:
        """
        Initialize the report generator.

        Args:
            template_dir: Path to Jinja2 templates (defaults to src/reporting/templates)
        """
        if template_dir is None:
            # EN: Robust path resolution that works in tests and production / FR: Résolution de chemin robuste pour tests et production
            base_dir = Path(__file__).resolve().parent
            template_dir = str(base_dir / "templates")

        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=True,  # EN: Prevent XSS / FR: Prévenir les attaques XSS
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["to_json"] = (
            json.dumps
        )  # EN: Custom filter for Plotly / FR: Filtre personnalisé pour Plotly

    def generate(
        self,
        state: AnalysisState,
        output_path: str,
        title: str = "AI Data Analysis Report",
    ) -> bool:
        """
        Generate an HTML report from AnalysisState.

        Args:
            state: The populated AnalysisState from the pipeline
            output_path: Where to save the HTML file
            title: Report title

        Returns:
            True if successful, False otherwise
        """
        try:
            template = self.env.get_template("report.html")

            # EN: Prepare context data / FR: Préparer les données de contexte
            context = {
                "title": title,
                "data_path": state.data_path,
                "insights": [
                    markdown.markdown(i) for i in state.insights
                ],  # EN: Convert insights to HTML / FR: Convertir les insights en HTML
                "summary_stats": state.summary_stats or {},
                "correlations": state.correlations or {},
                "cleaning_report": state.cleaning_report or {},
                "plots_code": state.plots_code,
                "plot_paths": state.plot_paths,
                "errors": state.errors,
            }

            # EN: Render template / FR: Rendre le template
            html_content = template.render(**context)

            # EN: Ensure output directory exists / FR: S'assurer que le répertoire de sortie existe
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            # EN: Write report / FR: Écrire le rapport
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            return True

        except TemplateNotFound as e:
            print(f"[ReportGenerator:ERROR] Template not found: {e}")
            return False
        except Exception as e:
            print(f"[ReportGenerator:ERROR] Report generation failed: {e}")
            return False
