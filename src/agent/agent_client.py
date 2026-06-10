"""Client wrapper for Azure AI Agent interactions."""

import json
import logging
from typing import Any, Dict
import requests
from .config import AgentConfig


class AgentClient:
    """Simplified HTTP client for Azure AI Agents."""

    def __init__(self, config: AgentConfig) -> None:
        self._config = config
        self._logger = logging.getLogger(__name__)

    def request_agent_response(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to the Azure AI Foundry agent endpoint.

        This method is a starter implementation. Replace the request body with
        the Azure-provided SDK call or REST contract when the integration is ready.
        """
        url = f"{self._config.project_endpoint.rstrip('/')}/agents/{self._config.agent_id}/responses"
        headers = {
            "Content-Type": "application/json",
        }

        self._logger.debug("Sending request to Azure AI Agent endpoint: %s", url)
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        return response.json()
