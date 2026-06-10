"""Configuration management for the Azure AI Study Assistant."""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass(frozen=True)
class AgentConfig:
    """Strongly typed configuration values for the agent."""

    project_endpoint: str
    model_deployment: str
    agent_id: str


def load_config() -> AgentConfig:
    """Load environment configuration from .env or environment variables."""
    load_dotenv()

    project_endpoint = os.getenv("PROJECT_ENDPOINT", "")
    model_deployment = os.getenv("MODEL_DEPLOYMENT", "")
    agent_id = os.getenv("AGENT_ID", "")

    if not project_endpoint or not model_deployment or not agent_id:
        raise ValueError(
            "Environment variables PROJECT_ENDPOINT, MODEL_DEPLOYMENT, and AGENT_ID must be set."
        )

    return AgentConfig(
        project_endpoint=project_endpoint,
        model_deployment=model_deployment,
        agent_id=agent_id,
    )
