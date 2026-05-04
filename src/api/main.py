# EN: FastAPI application entrypoint with health check
# FR: Point d'entrée de l'application FastAPI avec vérification de santé

from fastapi import FastAPI
from src.api.schemas import AnalyzeRequest, AnalyzeResponse

app = FastAPI(
    title="AI Data Analyst API",
    description="Async REST API for automated data analysis & reporting",
    version="0.1.0",
)


@app.get("/health", tags=["System"])
async def health_check() -> dict[str, str]:
    """Verify API is running and dependencies are loaded."""
    return {"status": "healthy", "version": "0.1.0"}


@app.post("/analyze", response_model=AnalyzeResponse, tags=["Analysis"])
async def run_analysis(request: AnalyzeRequest) -> AnalyzeResponse:
    """
    Trigger the full analysis pipeline.
    (Async integration will be implemented in Phase 6 Step 2)
    """
    return AnalyzeResponse(
        status="pending",
        message="Endpoint scaffolded. Full async integration coming in Step 2.",
    )
