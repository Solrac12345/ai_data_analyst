# EN: CLI entrypoint using Typer for command-line interaction
# FR: Point d'entrée CLI utilisant Typer pour l'interaction en ligne de commande

import typer
from rich.console import Console
from src.core.supervisor import supervisor_graph
from src.core.state import AnalysisState
from src.reporting.generator import ReportGenerator

app = typer.Typer(help="AI Data Analyst CLI", add_completion=False)
console = Console()


@app.command()
def analyze(
    input_path: str = typer.Option(
        ..., "--path", "-p", help="Path to the CSV or Excel file"
    ),
    output_dir: str = typer.Option(
        "output", "--output-dir", "-o", help="Directory for saving outputs"
    ),
    report_path: str = typer.Option(
        "output/report.html", "--report", "-r", help="Path for the HTML report"
    ),
) -> None:
    """
    Run the full data analysis pipeline on the specified file.
    """
    console.print(f"[bold blue]Starting Analysis for:[/bold blue] {input_path}")

    initial_state = {"data_path": input_path}

    try:
        final_state = supervisor_graph.invoke(initial_state)

        # Safe access to state attributes (Handle both dict and Pydantic model)
        if isinstance(final_state, dict):
            errors = final_state.get("errors", [])
            insights = final_state.get("insights", [])
            plot_paths = final_state.get("plot_paths", [])
        else:
            errors = final_state.errors
            insights = final_state.insights
            plot_paths = final_state.plot_paths

        if errors:
            console.print(f"[red]Errors found:[/red] {errors}")
            return

        # EN: Generate Report / FR: Générer le rapport
        console.print("\n[yellow]Generating HTML Report...[/yellow]")

        # Ensure we pass an AnalysisState object to the generator
        state_for_report = (
            final_state
            if not isinstance(final_state, dict)
            else AnalysisState(**final_state)
        )

        generator = ReportGenerator()
        success = generator.generate(state_for_report, report_path)

        if success:
            console.print(f"[green]✅ Report saved to:[/green] {report_path}")
        else:
            console.print("[red]❌ Failed to save report.[/red]")

        if insights:
            console.print("\n[bold green]Insights:[/bold green]")
            for insight in insights:
                console.print(f"💡 {insight}")

        if plot_paths:
            console.print(f"\n[yellow]Visualizations saved to:[/yellow] {output_dir}")

    except Exception as e:
        console.print(f"[red]Critical Error:[/red] {str(e)}")


if __name__ == "__main__":
    app()
