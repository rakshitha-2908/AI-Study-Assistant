"""AI-powered study assistant using GitHub Models with multi-turn conversation support."""

from openai import OpenAI
from .agent_client import ConversationHistory


class StudyAgent:
    """Interactive study assistant that generates study plans and answers questions.
    
    Uses GitHub Models (gpt-4o-mini) via the OpenAI SDK to provide intelligent
    study guidance with multi-turn conversation memory.
    """
    
    SYSTEM_PROMPT = (
        "You are an expert educational assistant. Your role is to help students learn effectively. "
        "When asked about a topic, create comprehensive study plans with clear objectives, key concepts, "
        "and practice tasks. When asked general questions, provide clear, concise explanations. "
        "Be encouraging and supportive in your responses."
    )
    
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
    
    def create_prompt(self, topic: str) -> str:
        """Create a study prompt for a given topic.
        
        Args:
            topic: The topic to create a study plan for.
            
        Returns:
            A formatted prompt string for the study assistant.
        """
        # Detect if input looks like a question vs a topic
        is_question = any(topic.strip().lower().startswith(q) for q in ["what", "how", "why", "when", "where", "who", "can", "is", "does", "should"])
        
        if is_question:
            return (
                f"Please answer the following question clearly and concisely: {topic}"
            )
        else:
            return (
                f"Create a comprehensive study plan for the topic: {topic}. "
                "Include: learning objectives, key concepts to master, important subtopics, "
                "and practical exercises or projects to reinforce learning."
            )
    
    def run(self, user_input: str) -> str:
        """Process user input and return an AI-generated response.
        
        Maintains multi-turn conversation memory by storing up to 10 recent messages.
        This allows the user to ask follow-up questions with context awareness.
        
        Args:
            user_input: The user's question or topic request.
            
        Returns:
            The AI assistant's response as a string.
        """
        # Create the appropriate prompt
        prompt = self.create_prompt(user_input)
        
        # Add user message to history
        self._conversation_history.add_message("user", prompt)
        
        # Get conversation history for context
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
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