# EN: Production server entrypoint for Uvicorn
# FR: Point d'entrée du serveur de production pour Uvicorn

import uvicorn

if __name__ == "__main__":
    # EN: Run FastAPI app on all interfaces, port 8000 / FR: Exécuter l'application FastAPI sur toutes les interfaces, port 8000
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False,  # EN: Disable reload in production / FR: Désactiver le rechargement en production
    )
