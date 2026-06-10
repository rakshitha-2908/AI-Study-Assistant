"""Study agent orchestration for the AI Study Assistant."""

from typing import Dict
from .config import AgentConfig
from .agent_client import AgentClient


class StudyAgent:
    """High-level agent logic for study planning and responses."""

    def __init__(self, config: AgentConfig) -> None:
        self._config = config
        self._client = AgentClient(config)

    def create_prompt(self, topic: str) -> str:
        """Create a study prompt for the user based on the given topic."""
        return (
            f"You are an educational assistant. Create a study plan for the topic: {topic}. "
            "Provide objectives, key concepts, and practice tasks."
        )

    def run(self, user_question: str) -> Dict[str, str]:
        """Send a request to Azure AI Agents and return the structured response."""
        prompt = self.create_prompt(user_question)
        payload = {
            "agent_id": self._config.agent_id,
            "deployment": self._config.model_deployment,
            "prompt": prompt,
        }
        return self._client.request_agent_response(payload)
