# EN: End-to-end integration test for the full pipeline
# FR: Test d'intégration de bout en bout pour le pipeline complet

import pandas as pd
from pathlib import Path
from src.core.supervisor import supervisor_graph


def test_full_pipeline_integration(tmp_path: Path) -> None:
    """Run CSV through Load -> Clean -> Analyze -> Visualize and verify outputs."""
    csv_file = tmp_path / "integration_data.csv"
    df = pd.DataFrame(
        {
            "feature_a": [1.0, 2.0, 3.0, 4.0, 5.0],
            "feature_b": [2.0, 4.0, 6.0, 8.0, 10.0],
            "category": ["X", "Y", "X", "Y", "X"],
        }
    )
    df.to_csv(csv_file, index=False)

    initial_state = {"data_path": str(csv_file)}
    final_state = supervisor_graph.invoke(initial_state)

    # Extract results (handle dict vs Pydantic model)
    errors = (
        final_state.get("errors", [])
        if isinstance(final_state, dict)
        else final_state.errors
    )
    insights = (
        final_state.get("insights", [])
        if isinstance(final_state, dict)
        else final_state.insights
    )
    plots = (
        final_state.get("plots_code", [])
        if isinstance(final_state, dict)
        else final_state.plots_code
    )
    stats = (
        final_state.get("summary_stats")
        if isinstance(final_state, dict)
        else final_state.summary_stats
    )

    # Verify pipeline success
    assert len(errors) == 0, f"Pipeline failed with errors: {errors}"
    assert len(insights) > 0, "Expected insights to be generated"
    assert "feature_a" in str(insights) or "feature_b" in str(insights), (
        "Insights should reference columns"
    )
    assert len(plots) == 1, "Expected one visualization code snippet"
    assert stats is not None, "Summary statistics should be computed"
    assert "feature_a" in stats, "Stats should include numeric columns"
