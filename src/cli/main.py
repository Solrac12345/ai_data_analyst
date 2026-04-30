# EN: CLI entrypoint using Typer for command-line interaction
# FR: Point d'entrée CLI utilisant Typer pour l'interaction en ligne de commande

import typer
from rich.console import Console
from src.core.supervisor import supervisor_graph

app = typer.Typer(help="AI Data Analyst CLI")
console = Console()


@app.command()
def analyze(
    path: str = typer.Argument(..., help="Path to the CSV or Excel file"),
    output_dir: str = typer.Option("output", help="Directory for saving outputs"),
) -> None:
    """
    Run the full data analysis pipeline on the specified file.
    """
    console.print(f"[bold blue]Starting Analysis for:[/bold blue] {path}")

    # 1. Create initial state dictionary
    initial_state = {"data_path": path}

    try:
        # 2. Run Graph
        # Note: LangGraph may return a dict or the state object depending on version
        final_state = supervisor_graph.invoke(initial_state)

        # 3. Safe access to state attributes (Handle both dict and Pydantic model)
        if isinstance(final_state, dict):
            errors = final_state.get("errors", [])
            insights = final_state.get("insights", [])
            plot_paths = final_state.get("plot_paths", [])
        else:
            errors = final_state.errors
            insights = final_state.insights
            plot_paths = final_state.plot_paths

        # 4. Output Results
        if errors:
            console.print(f"[red]Errors found:[/red] {errors}")
            return

        # Print Insights
        if insights:
            console.print("\n[bold green]Insights:[/bold green]")
            for insight in insights:
                console.print(f"💡 {insight}")

        # Print Viz Info
        if plot_paths:
            console.print(f"\n[yellow]Visualizations saved to:[/yellow] {output_dir}")

    except Exception as e:
        console.print(f"[red]Critical Error:[/red] {str(e)}")


if __name__ == "__main__":
    app()
