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

    def generate_quiz(self, topic: str, difficulty: str = "Intermediate", num_questions: int = 5) -> str:
        """Generate quiz questions for a given topic.
        
        Args:
            topic: The topic to generate questions about.
            difficulty: Student level — Beginner, Intermediate, or Interview-ready.
            num_questions: Number of questions to generate.
            
        Returns:
            The AI-generated quiz questions as a string.
        """
        quiz_prompt = (
            f"Generate exactly {num_questions} quiz questions about: {topic}. "
            f"Difficulty level: {difficulty}. "
            "Number each question. Do not include answers or explanations yet. "
            "Mix conceptual questions with at least one practical/coding question if relevant. "
            "Keep each question concise."
        )
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": quiz_prompt}
        ]
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages
        )
        
        return response.choices[0].message.content

    def evaluate_quiz_answers(self, topic: str, questions: str, user_answers: str) -> str:
        """Evaluate user's quiz answers and provide feedback with a score.
        
        Args:
            topic: The original quiz topic.
            questions: The quiz questions that were asked.
            user_answers: The user's submitted answers.
            
        Returns:
            Evaluation feedback including a score and corrections.
        """
        eval_prompt = (
            f"Here are quiz questions about {topic}:\n\n{questions}\n\n"
            f"Here are the student's answers:\n\n{user_answers}\n\n"
            "Evaluate each answer. For each question, mark it Correct or Incorrect, "
            "give the correct answer if they got it wrong, and a brief explanation. "
            "At the end, give a score out of the total questions in the format 'Score: X/Y'."
        )
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": eval_prompt}
        ]
        
        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages
        )
        
        return response.choices[0].message.content
    
    def clear_history(self) -> None:
        """Clear the conversation history for a fresh start."""
        self._conversation_history.clear()