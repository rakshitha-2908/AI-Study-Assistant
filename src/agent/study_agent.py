"""AI-powered study assistant using GitHub Models with multi-turn conversation support."""

from openai import OpenAI
from .agent_client import ConversationHistory
from .config import SYSTEM_PROMPT as CONFIG_SYSTEM_PROMPT


def detect_intent(user_message: str) -> str:
    msg = user_message.lower()
    plan_keywords = ["roadmap", "plan", "schedule", "days", "weeks", "curriculum", "learning path"]
    quiz_keywords = ["quiz", "test me", "interview questions", "practice questions", "give me questions"]
    teach_keywords = ["teach me", "help me understand", "i don't get", "walk me through"]
    debug_keywords = ["what's wrong", "why isn't", "fix this", "debug", "review my", "error in"]
    explain_keywords = ["what is", "what are", "define", "how does", "how do", "explain"]
    if any(k in msg for k in plan_keywords):
        return "PLAN"
    if any(k in msg for k in quiz_keywords):
        return "QUIZ"
    if any(k in msg for k in debug_keywords):
        return "DEBUG"
    if any(k in msg for k in teach_keywords):
        return "TEACH"
    if any(k in msg for k in explain_keywords):
        return "EXPLAIN"
    return "GENERAL"


def get_intent_instruction(intent: str) -> str:
    instructions = {
        "EXPLAIN": "\n[System: EXPLAIN request. Give a direct answer, one example, key points only. No study plans.]",
        "PLAN":    "\n[System: PLAN request. Generate a detailed structured roadmap.]",
        "QUIZ":    "\n[System: QUIZ request. Generate questions directly. No explanations unless asked.]",
        "TEACH":   "\n[System: TEACH request. Use lesson format: concept → intuition → example.]",
        "DEBUG":   "\n[System: DEBUG request. Identify the issue first, then explain, then show the fix.]",
        "GENERAL": "",
    }
    return instructions.get(intent, "")


class StudyAgent:
    """Interactive study assistant that generates study plans and answers questions.
    
    Uses GitHub Models (gpt-4o-mini) via the OpenAI SDK to provide intelligent
    study guidance with multi-turn conversation memory.
    """
    
    SYSTEM_PROMPT = CONFIG_SYSTEM_PROMPT
    
    def __init__(self, config: dict) -> None:
        """Initialize the StudyAgent with GitHub Models configuration.
        
        Args:
            config: Configuration dictionary with 'github_token', 'base_url', and 'model'.
        """
        self._client = OpenAI(
            base_url=config["base_url"],
            api_key=config["github_token"]
        )
        self._model = config["model"]
        self._conversation_history = ConversationHistory()
    
    def run(self, user_input: str, topic_context: str = "", difficulty: str = "Intermediate") -> str:
        """Process user input and return an AI-generated response.
        
        Maintains multi-turn conversation memory by storing up to 10 recent messages.
        This allows the user to ask follow-up questions with context awareness.
        
        Args:
            user_input: The user's question or topic request.
            topic_context: Subject-specific context injected into the system prompt.
            difficulty: Student level — Beginner, Intermediate, or Interview-ready.
            
        Returns:
            The AI assistant's response as a string.
        """
        # Detect intent and append instruction to user message
        intent = detect_intent(user_input)
        intent_note = get_intent_instruction(intent)
        augmented_input = user_input + intent_note

        # Add user message to history
        self._conversation_history.add_message("user", augmented_input)
        
        # Build augmented system prompt with difficulty and topic context
        difficulty_note = f"\nStudent level: {difficulty}. Adjust explanation depth and vocabulary accordingly."
        topic_note = f"\n{topic_context}" if topic_context else ""
        full_system_prompt = self.SYSTEM_PROMPT + difficulty_note + topic_note

        # Get conversation history for context
        messages = [
            {"role": "system", "content": full_system_prompt}
        ] + self._conversation_history.get_messages()
        
        # Call the API
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages
        )
        
        # Extract response
        assistant_response = response.choices[0].message.content
        
        # Add assistant response to history
        self._conversation_history.add_message("assistant", assistant_response)
        
        return assistant_response
    
    def clear_history(self) -> None:
        """Clear the conversation history for a fresh start."""
        self._conversation_history.clear()