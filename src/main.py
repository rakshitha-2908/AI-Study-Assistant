"""Entry point for the AI Study Assistant application."""

from agent.config import load_config
from agent.study_agent import StudyAgent


def main() -> None:
    """Start the AI Study Assistant application."""
    print("AI Study Assistant Started")
    _config = load_config()
    _agent = StudyAgent(_config)
    # Placeholder: extend this to accept user input and route to Azure AI Agent.
    _ = _agent.create_prompt("Introduction to Python for study planning")


if __name__ == "__main__":
    main()
