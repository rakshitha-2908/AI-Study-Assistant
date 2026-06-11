"""Study agent orchestration for the AI Study Assistant."""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class StudyAgent:
    """High-level agent logic for study planning and responses."""

    def __init__(self) -> None:
        self._client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ["GITHUB_TOKEN"]
        )
        self._model = "gpt-4o-mini"

    def create_prompt(self, topic: str) -> str:
        """Create a study prompt for the user based on the given topic."""
        return (
            f"You are an educational assistant. Create a study plan for the topic: {topic}. "
            "Provide objectives, key concepts, and practice tasks."
        )

    def run(self, user_question: str) -> str:
        """Send a request to GitHub Models and return the response."""
        prompt = self.create_prompt(user_question)
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content