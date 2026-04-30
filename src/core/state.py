# EN: Core state management using Pydantic v2 for type-safe agent routing / FR: Gestion d'état principale avec Pydantic v2 pour un routage d'agents typé
from __future__ import annotations

from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class PipelineState(BaseModel):
    # EN: Allow pandas DataFrames while enforcing strict validation on metadata / FR: Autoriser les DataFrames pandas tout en validant strictement les métadonnées
    model_config = ConfigDict(arbitrary_types_allowed=True, strict=True)

    # EN: Ingested dataset reference (DataFrame or secure file path) / FR: Référence du jeu de données ingéré (DataFrame ou chemin sécurisé)
    raw_data: Optional[Any] = Field(default=None, description="EN: Initial loaded data / FR: Données initialement chargées")

    # EN: Cleaned, validated & analysis-ready dataset / FR: Jeu de données nettoyé, validé & prêt pour l'analyse
    clean_data: Optional[Any] = Field(default=None, description="EN: Processed dataset / FR: Jeu de données traité")

    # EN: Statistical summaries, correlation maps & actionable insights / FR: Résumés statistiques, cartes de corrélation & insights actionnables
    summary: Optional[dict[str, Any]] = Field(default=None, description="EN: Analytical output / FR: Sortie analytique")

    # EN: Generated visualization code snippets (Plotly/Matplotlib) / FR: Extraits de code de visualisation générés (Plotly/Matplotlib)
    plots_code: list[str] = Field(default_factory=list, description="EN: Plotting scripts / FR: Scripts de tracé")

    # EN: Execution tracking, security flags & error recovery context / FR: Suivi d'exécution, drapeaux de sécurité & contexte de récupération d'erreurs
    created_at: datetime = Field(default_factory=datetime.now, description="EN: Pipeline initiation time / FR: Heure d'initialisation")
    current_step: str = Field(default="initialized", description="EN: Active orchestration phase / FR: Phase d'orchestration active")
    error_log: list[str] = Field(default_factory=list, description="EN: Sanitized exception traces / FR: Traces d'exceptions assainies")
    is_secure: bool = Field(default=True, description="EN: Input validation & sandbox status / FR: Statut de validation & sandbox")

    def to_serializable(self) -> dict:
        # EN: Export state for CI/logs while stripping heavy in-memory objects / FR: Exporter l'état pour CI/logs en retirant les objets mémoire lourds
        return self.model_dump(exclude={"raw_data", "clean_data"})