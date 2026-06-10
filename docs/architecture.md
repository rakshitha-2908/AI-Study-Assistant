# Architecture Overview

This project is designed as a production-ready Python portfolio application for an AI Study Assistant.
It demonstrates a clean package layout, Azure AI Foundry integration points, and agent orchestration.

## Core Components

- `src/main.py`
  - Application entry point and startup logic.
- `src/agent/config.py`
  - Loads environment configuration for Azure AI settings.
- `src/agent/agent_client.py`
  - HTTP client wrapper for Azure AI Agents.
- `src/agent/study_agent.py`
  - Business logic for generating study prompts and orchestrating responses.
- `src/utils/helpers.py`
  - Shared utilities such as logging and validation.

## Azure AI Integration

The assistant is built to support:
- Azure AI Foundry project endpoint
- Azure AI Agents
- GPT-4o Mini deployment

## Project Structure

```
AI-Study-Assistant/
├── src/
│   ├── agent/
│   └── utils/
├── docs/
│   └── screenshots/
├── tests/
├── data/
├── .github/
│   └── workflows/
├── .env.example
└── requirements.txt
```

## Development Notes

- Use `.env` for local credentials and deployment settings.
- Keep sensitive values out of source control.
- Extend `AgentClient` with the Azure SDK or REST contract when ready.
