# 🤖 AI Data Analyst Pipeline

A modular, agent-driven data analysis pipeline built with **LangGraph**, **Typer**, and **Rich**. Automatically loads, cleans, analyzes, and visualizes datasets, then generates interactive HTML reports. Fully containerized with Docker and production-ready CI/CD.

## ✨ Features

- 🧠 **Agent Architecture**: LangGraph state machine orchestrating `DataLoader`, `Cleaning`, `Analysis`, and `Viz` agents
- 🖥️ **CLI Interface**: Typer-powered commands with Rich console output & progress logging
- 📊 **Statistical Analysis**: Automatic descriptive stats, correlation matrices, and natural language insights
- 🎨 **Visualization Code**: Auto-generates ready-to-run Matplotlib/Plotly snippets
- 📄 **HTML Reporting**: Jinja2 + Markdown engine produces responsive, interactive reports
- 🐳 **Docker Ready**: Multi-stage build, non-root user, Trivy security scanning, `docker-compose` dev workflow
- ✅ **Tested & CI**: 28 unit/integration tests, GitHub Actions pipeline (lint → type → test → docker)
- ⚙️ **Configurable**: Override strategies, thresholds, and libraries via YAML or environment variables

## 🚀 Quick Start

### Local Installation
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run analysis
python -m src.cli.main --path data/sample.csv --report output/report.html

### Docker Installation
# Build & run in one command
docker compose build
docker compose run --rm --entrypoint "" app python -m src.cli.main --path /app/data/sample.csv --report /app/output/report.html

💡 Windows/Git Bash Users: Path conversion can cause issues. Prepend commands with MSYS_NO_PATHCONV=1:

MSYS_NO_PATHCONV=1 docker compose run --rm --entrypoint "" app python -m src.cli.main --path /app/data/sample.csv --report /app/output/report.html

## Example Run:

$ python -m src.cli.main --path data/sample.csv --report output/report.html
Starting Analysis for: data/sample.csv
[DataLoaderAgent:INFO] Loaded 3 rows, 3 columns
[CleaningAgent:INFO] Removed 0 duplicate rows
[AnalysisAgent:INFO] Generated 2 insights
[VizAgent:INFO] Generated matplotlib visualization code for 'Age'
✅ Report saved to: output/report.html

## ⚙️ Configuration
# Change missing value strategy
APP_CLEANING__MISSING_STRATEGY=median python -m src.cli.main --path data.csv

# Adjust outlier threshold
APP_CLEANING__OUTLIER_THRESHOLD=2.5 python -m src.cli.main --path data.csv

# Switch visualization library
APP_VISUALIZATION__LIBRARY=plotly python -m src.cli.main --path data.csv

## Docker Workflow
Development:
# Interactive shell (bypass entrypoint)
MSYS_NO_PATHCONV=1 docker compose run --rm --entrypoint "" app bash

# Mount local changes for live dev
MSYS_NO_PATHCONV=1 docker compose run --rm -v ${PWD}/src:/app/src:ro app --path /app/data/sample.csv

## Testing in Container
# Run full test suite with coverage
docker compose --profile testing run --build test

## Security Scanning
trivy image ai-data-analyst:latest

## 📄 HTML Reporting
The pipeline generates rich, responsive HTML reports containing:
📊 Descriptive statistics tables (mean, std, min, max, quartiles)
💡 Markdown-rendered insights with natural language explanations
🎨 Generated Matplotlib/Plotly code snippets ready to execute
📈 Plotly CDN integration for interactive charts in the browser
⚠️ Error tracking & pipeline status visibility
📱 Responsive design (mobile & desktop)

## Open the report:
# Linux/macOS
xdg-open output/report.html  # or open -a Preview

# Windows
start output/report.html

## Testing & CI/CD
# Run all tests locally
pytest test/ -v --cov=src

# Type checking
mypy src/ test/

# Lint & format
ruff check .
ruff format .

GitHub Actions Pipeline:
lint → Ruff linting & formatting check
type-check → MyPy static type validation
test → Pytest with coverage
docker-build → Multi-stage build + Trivy vulnerability scan
All jobs must pass before merging to main.

🙏 Acknowledgments
LangGraph for agent orchestration
Typer for CLI framework
Jinja2 for HTML templating
Plotly for interactive visualizations

---

##  REST API (Phase 6)

The pipeline is exposed via a production-ready FastAPI server with async support, Swagger UI, and thread-pool offloading for heavy computation.

### 🚀 Start API Server
```bash
# Launch API service (accessible at http://localhost:8000)
docker compose up -d api

📜 Final Archive Statement
Project: AI Data Analyst Pipeline
Owner: @carld
Completion Date: May 2026
Status: ✅ Production-Ready, Fully Tested, CI-Gated, Containerized
License: MIT
"A modular, agent-driven system that transforms raw data into actionable insights — with CLI, Docker, and API interfaces, all built to professional standards."
