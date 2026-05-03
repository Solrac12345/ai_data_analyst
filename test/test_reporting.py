# EN: Unit tests for ReportGenerator
# FR: Tests unitaires pour ReportGenerator

from pathlib import Path
from src.core.state import AnalysisState
from src.reporting.generator import ReportGenerator


def test_generate_report_success(tmp_path: Path) -> None:
    """Test successful HTML report generation."""
    state = AnalysisState(
        data_path="test.csv",
        insights=["Dataset contains 100 rows.", "Strong correlation detected."],
        summary_stats={"feature_a": {"mean": 5.0, "std": 2.1}},
        plots_code=["plt.plot([1,2,3])"],
        plot_paths=["output/plot.png"],
    )

    output_file = tmp_path / "report.html"
    generator = ReportGenerator()
    result = generator.generate(state, str(output_file))

    assert result is True
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "<title>AI Data Analysis Report</title>" in content
    assert "Dataset contains 100 rows" in content


def test_generate_report_with_errors(tmp_path: Path) -> None:
    """Test report generation when state has errors."""
    state = AnalysisState(errors=["File not found", "Invalid format"])

    output_file = tmp_path / "error_report.html"
    generator = ReportGenerator()
    result = generator.generate(state, str(output_file))

    assert result is True
    content = output_file.read_text(encoding="utf-8")
    assert "Pipeline Errors" in content
    assert "File not found" in content


def test_generate_report_missing_template(tmp_path: Path) -> None:
    """Test graceful failure when template is missing."""
    state = AnalysisState()

    # Point to non-existent template directory
    generator = ReportGenerator(template_dir="/nonexistent/path")
    result = generator.generate(state, str(tmp_path / "fail.html"))

    assert result is False
