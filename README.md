# AI Data Analyst Multi-Agent
Automated data analysis pipeline with specialized agents.
### ✅ Phase 0: CI Foundation & Configuration (Complete)
- [x] GitHub Actions CI/CD pipeline
- [x] Ruff linting & formatting
- [x] MyPy strict type checking
- [x] Pytest configuration with coverage
- [x] Pydantic settings with YAML + env var support
- [x] Configuration validation & testing

**Status**: ✅ All tests passing, CI green

### ✅ Phase 1: Core Architecture (Complete)
- [x] `AnalysisState` Pydantic model for shared state
- [x] LangGraph `StateGraph` supervisor
- [x] Conditional routing logic
- [x] State validation & error handling
- [x] Unit tests for state & supervisor

**Status**: ✅ All tests passing, CI green

### ✅ Phase 2: Agent Implementation (Complete)
- [x] `BaseAgent` abstract class with type generics
- [x] `DataLoaderAgent`: CSV/Excel loading with encoding handling
- [x] `CleaningAgent`: 
  - Duplicate removal
  - Missing value imputation (mean/median/mode/drop)
  - Z-score outlier detection
- [x] Integration with supervisor graph
- [x] Comprehensive unit tests for all agents

**Status**: ✅ All tests passing, CI green

### ✅ Phase 3: Analysis & Visualization (Complete)
- [x] `AnalysisAgent`: Descriptive statistics, correlation matrices, natural language insights
- [x] `VizAgent`: Auto-generation of Matplotlib/Plotly code snippets
- [x] CLI entrypoint: `python -m src.cli.main analyze data.csv`
- [x] Full pipeline integration test
- [x] Updated documentation & badges

**Status**: ✅ All tests passing, CI green

## 📦 Installation

### Prerequisites
- Python 3.11+
- Git

### Setup
    ```bash
    # Clone repository
    git clone https://github.com/YOUR_USERNAME/ai-data-analyst.git
    cd ai-data-analyst

    # Create virtual environment
    python -m venv .venv
    source .venv/Scripts/activate  # Windows Git Bash
    # source .venv/bin/activate    # macOS/Linux

    # Install dependencies
    pip install -e ".[dev]"

Verify Installation

    # Run tests
    pytest test/ -v

    # Run linter
    ruff check .

    # Type check
    mypy src/