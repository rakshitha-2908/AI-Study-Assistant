"""Azure AI Study Assistant agent package.

This package contains the configuration and client logic for the study agent.
"""

from .config import AgentConfig, load_config
from .agent_client import AgentClient
from .study_agent import StudyAgent

__all__ = ["AgentConfig", "load_config", "AgentClient", "StudyAgent"]
