"""Utility helpers for the AI Study Assistant project."""

import logging
import os
from typing import List
from datetime import datetime


def setup_logging(level: int = logging.INFO) -> None:
    """Configure basic logging for development and production.
    
    Args:
        level: Logging level (default: INFO).
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def format_response(response: str) -> str:
    """Format the agent's markdown response for nice terminal output.
    
    Adds visual separation and enhances readability of multi-line responses.
    
    Args:
        response: The raw response text from the agent.
        
    Returns:
        A formatted string suitable for terminal display.
    """
    lines = []
    lines.append("\n" + "=" * 80)
    lines.append(response)
    lines.append("=" * 80 + "\n")
    
    return "\n".join(lines)


def save_session_transcript(messages: List[dict], filename: str = None) -> str:
    """Save a session transcript to a file.
    
    Creates a /transcripts folder if it doesn't exist and saves the conversation
    history with timestamps.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys.
        filename: Optional custom filename. If None, generates one with timestamp.
        
    Returns:
        The path to the saved transcript file.
    """
    # Create transcripts directory if it doesn't exist
    transcript_dir = "transcripts"
    os.makedirs(transcript_dir, exist_ok=True)
    
    # Generate filename if not provided
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"session_{timestamp}.txt"
    
    filepath = os.path.join(transcript_dir, filename)
    
    # Write transcript
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("AI Study Assistant - Session Transcript\n")
        f.write("=" * 80 + "\n")
        f.write(f"Saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        for i, msg in enumerate(messages, 1):
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")
            f.write(f"[{i}] {role}:\n{content}\n\n")
            f.write("-" * 80 + "\n\n")
    
    return filepath
