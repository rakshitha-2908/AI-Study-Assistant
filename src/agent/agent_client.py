"""Conversation history manager for multi-turn conversations."""

from typing import List, Dict


class ConversationHistory:
    """Manages conversation history with a configurable message limit.
    
    Stores messages in a sliding window to maintain context while limiting
    the total number of messages sent to the API.
    """
    
    MAX_MESSAGES: int = 10
    
    def __init__(self, max_messages: int = MAX_MESSAGES) -> None:
        """Initialize the conversation history.
        
        Args:
            max_messages: Maximum number of messages to keep in history.
        """
        self.messages: List[Dict[str, str]] = []
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history.
        
        Args:
            role: The role of the message sender ("user" or "assistant").
            content: The message content.
        """
        self.messages.append({"role": role, "content": content})
        
        # Keep only the last max_messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self) -> List[Dict[str, str]]:
        """Get the current conversation history.
        
        Returns:
            List of message dictionaries with 'role' and 'content' keys.
        """
        return self.messages.copy()
    
    def clear(self) -> None:
        """Clear the conversation history."""
        self.messages = []
