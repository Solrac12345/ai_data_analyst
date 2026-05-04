# EN: FastAPI application with async pipeline integration
# FR: Application FastAPI avec intégration async du pipeline

import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException
from src.api.schemas import AnalyzeRequest, AnalyzeResponse
from src.core.supervisor import supervisor_graph

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
    Trigger the full analysis pipeline asynchronously.
    Offloads synchronous LangGraph execution to a background thread.
    """
    data_path = Path(request.data_path)
    if not data_path.exists():
        return AnalyzeResponse(
            status="error",
            message=f"File not found: {request.data_path}",
            errors=[f"File not found: {request.data_path}"],
        )

    try:
        # EN: Offload sync pipeline to thread pool / FR: Déléguer le pipeline synchrone au pool de threads
        final_state = await asyncio.to_thread(
            supervisor_graph.invoke, {"data_path": request.data_path}
        )

        # Extract results (handle dict vs Pydantic model)
        if isinstance(final_state, dict):
            errors = final_state.get("errors", [])
            insights = final_state.get("insights", [])
        else:
            errors = final_state.errors
            insights = final_state.insights

        if errors:
            return AnalyzeResponse(
                status="error",
                message="Pipeline completed with errors",
                errors=errors,
                insights=insights,
            )

        return AnalyzeResponse(
            status="success",
            message="Analysis completed successfully",
            report_url=request.report_path,
            insights=insights,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Pipeline execution failed: {str(e)}"
        )
