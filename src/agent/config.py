"""Configuration management for the AI Study Assistant."""

import os
from dotenv import load_dotenv


def load_config() -> dict:
    """Load environment configuration from .env file.
    
    Returns:
        dict: Configuration dictionary with GitHub token.
        
    Raises:
        ValueError: If GITHUB_TOKEN is not set.
    """
    load_dotenv()
    
    github_token = os.getenv("GITHUB_TOKEN", "").strip()
    
    if not github_token:
        raise ValueError(
            "GITHUB_TOKEN environment variable must be set. "
            "Please create a .env file with your GitHub Personal Access Token."
        )
    
    return {
        "github_token": github_token,
        "base_url": "https://models.inference.ai.azure.com",
        "model": "gpt-4o-mini",
    }
