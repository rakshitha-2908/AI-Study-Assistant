"""Basic unit tests for the AI Study Assistant agent."""

import unittest
from agent.config import AgentConfig
from agent.study_agent import StudyAgent


class TestStudyAgent(unittest.TestCase):
    """Unit tests for StudyAgent behavior."""

    def setUp(self) -> None:
        self.config = AgentConfig(
            project_endpoint="https://example.azure.com",
            model_deployment="gpt-4o-mini",
            agent_id="demo-agent",
        )
        self.agent = StudyAgent(self.config)

    def test_create_prompt_returns_string(self) -> None:
        """The study prompt builder should return a non-empty string."""
        prompt = self.agent.create_prompt("Machine learning fundamentals")
        self.assertIsInstance(prompt, str)
        self.assertIn("Machine learning fundamentals", prompt)


if __name__ == "__main__":
    unittest.main()
