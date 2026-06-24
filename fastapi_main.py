"""FastAPI backend for the AI Study Assistant.

Wraps the existing StudyAgent class with HTTP endpoints so a separate
frontend (React, etc.) can talk to it. No changes were made to the
original agent logic (study_agent.py, agent_client.py, config.py) —
this file only exposes it over HTTP.
"""

import uuid
import traceback
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent.config import load_config
from src.agent.study_agent import StudyAgent

app = FastAPI(title="AI Study Assistant API")

# Allow the React frontend (running on a different port/domain) to call this API.
# Vite's default dev server port is 5173; 3000 is included in case you're on CRA.
# Add your deployed frontend URL here once it's live.
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "https://ai-study-assistant-beryl.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store: one StudyAgent instance per session_id.
# This is the FastAPI equivalent of Streamlit's st.session_state — Streamlit
# gave you this for free per browser tab; here we do it manually with a dict.
# NOTE: this resets if the server restarts, and doesn't scale across multiple
# server processes. Fine for a portfolio project / single-instance deploy.
sessions: Dict[str, StudyAgent] = {}

try:
    config = load_config()
except ValueError as e:
    # Fail loudly at startup if GITHUB_TOKEN is missing, same as the CLI version did.
    raise RuntimeError(f"Configuration error: {e}")


def get_or_create_agent(session_id: str) -> StudyAgent:
    """Return the StudyAgent for this session, creating one if it doesn't exist yet.

    This means a request with an unrecognized session_id won't 404 — it just
    silently starts a fresh agent. That's intentional: if the server restarts
    and the frontend still has an old session_id cached, this avoids a hard
    crash, at the cost of silently losing that session's history.
    """
    if session_id not in sessions:
        sessions[session_id] = StudyAgent(config)
    return sessions[session_id]


# ---------- Request/response schemas ----------

class ChatRequest(BaseModel):
    session_id: str
    message: str
    topic_context: str = ""
    difficulty: str = "Intermediate"


class ChatResponse(BaseModel):
    response: str


class QuizGenerateRequest(BaseModel):
    session_id: str
    topic: str
    difficulty: str = "Intermediate"
    num_questions: int = 5


class QuizGenerateResponse(BaseModel):
    questions: str


class QuizEvaluateRequest(BaseModel):
    session_id: str
    topic: str
    questions: str
    user_answers: str


class QuizEvaluateResponse(BaseModel):
    feedback: str


class NewSessionResponse(BaseModel):
    session_id: str


# ---------- Endpoints ----------

@app.get("/")
def root():
    """Basic root endpoint, kept from the existing app."""
    return {"message": "AI Study Assistant API is running"}


@app.get("/health")
def health_check():
    """Simple status check — confirms the server is up and config loaded."""
    return {"status": "ok"}


@app.post("/session/new", response_model=NewSessionResponse)
def new_session():
    """Create a fresh session_id for a new browser tab/user.

    The frontend calls this once when the app loads, then reuses the
    returned session_id on every subsequent /chat or /quiz call.
    """
    session_id = str(uuid.uuid4())
    sessions[session_id] = StudyAgent(config)
    return NewSessionResponse(session_id=session_id)


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Send a message to the study agent and get a response.

    Mirrors StudyAgent.run() exactly — same params, same behavior.
    """
    agent = get_or_create_agent(req.session_id)

    try:
        response = agent.run(
            user_input=req.message,
            topic_context=req.topic_context,
            difficulty=req.difficulty,
        )

        return ChatResponse(response=response)

    except Exception as e:
        print("\n========== CHAT ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/quiz/generate", response_model=QuizGenerateResponse)
def quiz_generate(req: QuizGenerateRequest):
    """Generate quiz questions for a topic. Mirrors StudyAgent.generate_quiz()."""
    agent = get_or_create_agent(req.session_id)
    try:
        questions = agent.generate_quiz(
            topic=req.topic,
            difficulty=req.difficulty,
            num_questions=req.num_questions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return QuizGenerateResponse(questions=questions)


@app.post("/quiz/evaluate", response_model=QuizEvaluateResponse)
def quiz_evaluate(req: QuizEvaluateRequest):
    """Evaluate submitted quiz answers. Mirrors StudyAgent.evaluate_quiz_answers()."""
    agent = get_or_create_agent(req.session_id)
    try:
        feedback = agent.evaluate_quiz_answers(
            topic=req.topic,
            questions=req.questions,
            user_answers=req.user_answers,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return QuizEvaluateResponse(feedback=feedback)


@app.post("/session/{session_id}/clear")
def clear_session(session_id: str):
    """Clear conversation history for a session. Mirrors StudyAgent.clear_history()."""
    if session_id in sessions:
        sessions[session_id].clear_history()
    return {"status": "cleared"}


# Kept for backward compatibility with whatever was already calling /ask.
# Internally just delegates to the same logic as /chat. Safe to remove once
# nothing references it anymore.
class AskRequest(BaseModel):
    session_id: str
    message: str
    topic_context: str = ""
    difficulty: str = "Intermediate"


@app.post("/ask", response_model=ChatResponse)
def ask(req: AskRequest):
    """Legacy endpoint, preserved so anything still calling /ask keeps working."""
    return chat(req)
