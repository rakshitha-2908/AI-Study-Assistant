"""Unit tests for the AI Study Assistant agent."""

import unittest
import os
from dotenv import load_dotenv
from agent.config import load_config
from agent.study_agent import StudyAgent


class TestStudyAgent(unittest.TestCase):
    """Unit tests for StudyAgent behavior."""
    
    @classmethod
    def setUpClass(cls) -> None:
        """Set up test fixtures once for all tests."""
        load_dotenv()
    
    def test_study_agent_initializes(self) -> None:
        """Test that StudyAgent initializes without errors."""
        try:
            config = load_config()
            agent = StudyAgent(config)
            self.assertIsNotNone(agent)
            self.assertIsNotNone(agent._client)
            self.assertEqual(agent._model, "gpt-4o-mini")
        except ValueError:
            # If GITHUB_TOKEN is not set, skip this test
            self.skipTest("GITHUB_TOKEN not configured")
    
    def test_create_prompt_returns_string(self) -> None:
        """Test that create_prompt returns a non-empty string."""
        try:
            config = load_config()
            agent = StudyAgent(config)
            
            # Test with a topic
            prompt = agent.create_prompt("Machine Learning Fundamentals")
            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)
            self.assertIn("Machine Learning Fundamentals", prompt)
            
            # Test with a question
            prompt_question = agent.create_prompt("What is supervised learning?")
            self.assertIsInstance(prompt_question, str)
            self.assertGreater(len(prompt_question), 0)
            
        except ValueError:
            self.skipTest("GITHUB_TOKEN not configured")
    
    def test_conversation_history_management(self) -> None:
        """Test that conversation history is properly managed."""
        try:
            config = load_config()
            agent = StudyAgent(config)
            
            # Check initial state
            self.assertEqual(len(agent._conversation_history.get_messages()), 0)
            
            # Add messages
            agent._conversation_history.add_message("user", "What is Python?")
            self.assertEqual(len(agent._conversation_history.get_messages()), 1)
            
            agent._conversation_history.add_message("assistant", "Python is a programming language.")
            self.assertEqual(len(agent._conversation_history.get_messages()), 2)
            
            # Test clear
            agent._conversation_history.clear()
            self.assertEqual(len(agent._conversation_history.get_messages()), 0)
            
        except ValueError:
            self.skipTest("GITHUB_TOKEN not configured")


if __name__ == "__main__":
    unittest.main()
