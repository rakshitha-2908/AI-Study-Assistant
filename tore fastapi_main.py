[1mdiff --git a/fastapi_main.py b/fastapi_main.py[m
[1mindex 61ca38b..94feebb 100644[m
[1m--- a/fastapi_main.py[m
[1m+++ b/fastapi_main.py[m
[36m@@ -1,43 +1,200 @@[m
[31m-from fastapi import FastAPI[m
[31m-from pydantic import BaseModel[m
[32m+[m[32m"""FastAPI backend for the AI Study Assistant.[m
[32m+[m
[32m+[m[32mWraps the existing StudyAgent class with HTTP endpoints so a separate[m
[32m+[m[32mfrontend (React, etc.) can talk to it. No changes were made to the[m
[32m+[m[32moriginal agent logic (study_agent.py, agent_client.py, config.py) —[m
[32m+[m[32mthis file only exposes it over HTTP.[m
[32m+[m[32m"""[m
[32m+[m
[32m+[m[32mimport uuid[m
[32m+[m[32mfrom typing import Dict[m
[32m+[m
[32m+[m[32mfrom fastapi import FastAPI, HTTPException[m
 from fastapi.middleware.cors import CORSMiddleware[m
[32m+[m[32mfrom pydantic import BaseModel[m
 [m
 from src.agent.config import load_config[m
 from src.agent.study_agent import StudyAgent[m
 [m
[31m-app = FastAPI([m
[31m-    title="AI Study Assistant API",[m
[31m-    version="1.0.0"[m
[31m-)[m
[32m+[m[32mapp = FastAPI(title="AI Study Assistant API")[m
[32m+[m
[32m+[m[32m# Allow the React frontend (running on a different port/domain) to call this API.[m
[32m+[m[32m# Vite's default dev server port is 5173; 3000 is included in case you're on CRA.[m
[32m+[m[32m# Add your deployed frontend URL here once it's live.[m
[32m+[m[32mfrom fastapi.middleware.cors import CORSMiddleware[m
[32m+[m
 app.add_middleware([m
     CORSMiddleware,[m
[31m-    allow_origins=["*"],[m
[32m+[m[32m    allow_origins=[[m
[32m+[m[32m        "http://localhost:5173",[m
[32m+[m[32m        "http://localhost:5174",[m
[32m+[m[32m        "http://127.0.0.1:5173",[m
[32m+[m[32m        "http://127.0.0.1:5174",[m
[32m+[m[32m    ],[m
     allow_credentials=True,[m
     allow_methods=["*"],[m
     allow_headers=["*"],[m
 )[m
[31m-@app.get("/health")[m
[31m-def health():[m
[31m-    return {"status": "healthy"}[m
 [m
[31m-config = load_config()[m
[31m-agent = StudyAgent(config)[m
[32m+[m[32m# In-memory store: one StudyAgent instance per session_id.[m
[32m+[m[32m# This is the FastAPI equivalent of Streamlit's st.session_state — Streamlit[m
[32m+[m[32m# gave you this for free per browser tab; here we do it manually with a dict.[m
[32m+[m[32m# NOTE: this resets if the server restarts, and doesn't scale across multiple[m
[32m+[m[32m# server processes. Fine for a portfolio project / single-instance deploy.[m
[32m+[m[32msessions: Dict[str, StudyAgent] = {}[m
[32m+[m
[32m+[m[32mtry:[m
[32m+[m[32m    config = load_config()[m
[32m+[m[32mexcept ValueError as e:[m
[32m+[m[32m    # Fail loudly at startup if GITHUB_TOKEN is missing, same as the CLI version did.[m
[32m+[m[32m    raise RuntimeError(f"Configuration error: {e}")[m
[32m+[m
[32m+[m
[32m+[m[32mdef get_or_create_agent(session_id: str) -> StudyAgent:[m
[32m+[m[32m    """Return the StudyAgent for this session, creating one if it doesn't exist yet.[m
[32m+[m
[32m+[m[32m    This means a request with an unrecognized session_id won't 404 — it just[m
[32m+[m[32m    silently starts a fresh agent. That's intentional: if the server restarts[m
[32m+[m[32m    and the frontend still has an old session_id cached, this avoids a hard[m
[32m+[m[32m    crash, at the cost of silently losing that session's history.[m
[32m+[m[32m    """[m
[32m+[m[32m    if session_id not in sessions:[m
[32m+[m[32m        sessions[session_id] = StudyAgent(config)[m
[32m+[m[32m    return sessions[session_id][m
[32m+[m
[32m+[m
[32m+[m[32m# ---------- Request/response schemas ----------[m
[32m+[m
[32m+[m[32mclass ChatRequest(BaseModel):[m
[32m+[m[32m    session_id: str[m
[32m+[m[32m    message: str[m
[32m+[m[32m    topic_context: str = ""[m
[32m+[m[32m    difficulty: str = "Intermediate"[m
[32m+[m
[32m+[m
[32m+[m[32mclass ChatResponse(BaseModel):[m
[32m+[m[32m    response: str[m
[32m+[m
[32m+[m
[32m+[m[32mclass QuizGenerateRequest(BaseModel):[m
[32m+[m[32m    session_id: str[m
[32m+[m[32m    topic: str[m
[32m+[m[32m    difficulty: str = "Intermediate"[m
[32m+[m[32m    num_questions: int = 5[m
[32m+[m
 [m
[32m+[m[32mclass QuizGenerateResponse(BaseModel):[m
[32m+[m[32m    questions: str[m
 [m
[31m-class QuestionRequest(BaseModel):[m
[31m-    question: str[m
 [m
[32m+[m[32mclass QuizEvaluateRequest(BaseModel):[m
[32m+[m[32m    session_id: str[m
[32m+[m[32m    topic: str[m
[32m+[m[32m    questions: str[m
[32m+[m[32m    user_answers: str[m
[32m+[m
[32m+[m
[32m+[m[32mclass QuizEvaluateResponse(BaseModel):[m
[32m+[m[32m    feedback: str[m
[32m+[m
[32m+[m
[32m+[m[32mclass NewSessionResponse(BaseModel):[m
[32m+[m[32m    session_id: str[m
[32m+[m
[32m+[m
[32m+[m[32m# ---------- Endpoints ----------[m
 [m
 @app.get("/")[m
 def root():[m
[32m+[m[32m    """Basic root endpoint, kept from the existing app."""[m
     return {"message": "AI Study Assistant API is running"}[m
 [m
 [m
[31m-@app.post("/ask")[m
[31m-def ask(request: QuestionRequest):[m
[31m-    response = agent.run(request.question)[m
[32m+[m[32m@app.get("/health")[m
[32m+[m[32mdef health_check():[m
[32m+[m[32m    """Simple status check — confirms the server is up and config loaded."""[m
[32m+[m[32m    return {"status": "ok"}[m
[32m+[m
[32m+[m
[32m+[m[32m@app.post("/session/new", response_model=NewSessionResponse)[m
[32m+[m[32mdef new_session():[m
[32m+[m[32m    """Create a fresh session_id for a new browser tab/user.[m
[32m+[m
[32m+[m[32m    The frontend calls this once when the app loads, then reuses the[m
[32m+[m[32m    returned session_id on every subsequent /chat or /quiz call.[m
[32m+[m[32m    """[m
[32m+[m[32m    session_id = str(uuid.uuid4())[m
[32m+[m[32m    sessions[session_id] = StudyAgent(config)[m
[32m+[m[32m    return NewSessionResponse(session_id=session_id)[m
[32m+[m
[32m+[m
[32m+[m[32m@app.post("/chat", response_model=ChatResponse)[m
[32m+[m[32mdef chat(req: ChatRequest):[m
[32m+[m[32m    """Send a message to the study agent and get a response.[m
[32m+[m
[32m+[m[32m    Mirrors StudyAgent.run() exactly — same params, same behavior.[m
[32m+[m[32m    """[m
[32m+[m[32m    agent = get_or_create_agent(req.session_id)[m
[32m+[m[32m    try:[m
[32m+[m[32m        response = agent.run([m
[32m+[m[32m            user_input=req.message,[m
[32m+[m[32m            topic_context=req.topic_context,[m
[32m+[m[32m            difficulty=req.difficulty,[m
[32m+[m[32m        )[m
[32m+[m[32m    except Exception as e:[m
[32m+[m[32m        raise HTTPException(status_code=500, detail=str(e))[m
[32m+[m[32m    return ChatResponse(response=response)[m
[32m+[m
[32m+[m
[32m+[m[32m@app.post("/quiz/generate", response_model=QuizGenerateResponse)[m
[32m+[m[32mdef quiz_generate(req: QuizGenerateRequest):[m
[32m+[m[32m    """Generate quiz questions for a topic. Mirrors StudyAgent.generate_quiz()."""[m
[32m+[m[32m    agent = get_or_create_agent(req.session_id)[m
[32m+[m[32m    try:[m
[32m+[m[32m        questions = agent.generate_quiz([m
[32m+[m[32m            topic=req.topic,[m
[32m+[m[32m            difficulty=req.difficulty,[m
[32m+[m[32m            num_questions=req.num_questions,[m
[32m+[m[32m        )[m
[32m+[m[32m    except Exception as e:[m
[32m+[m[32m        raise HTTPException(status_code=500, detail=str(e))[m
[32m+[m[32m    return QuizGenerateResponse(questions=questions)[m
[32m+[m
[32m+[m
[32m+[m[32m@app.post("/quiz/evaluate", response_model=QuizEvaluateResponse)[m
[32m+[m[32mdef quiz_evaluate(req: QuizEvaluateRequest):[m
[32m+[m[32m    """Evaluate submitted quiz answers. Mirrors StudyAgent.evaluate_quiz_answers()."""[m
[32m+[m[32m    agent = get_or_create_agent(req.session_id)[m
[32m+[m[32m    try:[m
[32m+[m[32m        feedback = agent.evaluate_quiz_answers([m
[32m+[m[32m            topic=req.topic,[m
[32m+[m[32m            questions=req.questions,[m
[32m+[m[32m            user_answers=req.user_answers,[m
[32m+[m[32m        )[m
[32m+[m[32m    except Exception as e:[m
[32m+[m[32m        raise HTTPException(status_code=500, detail=str(e))[m
[32m+[m[32m    return QuizEvaluateResponse(feedback=feedback)[m
[32m+[m
[32m+[m
[32m+[m[32m@app.post("/session/{session_id}/clear")[m
[32m+[m[32mdef clear_session(session_id: str):[m
[32m+[m[32m    """Clear conversation history for a session. Mirrors StudyAgent.clear_history()."""[m
[32m+[m[32m    if session_id in sessions:[m
[32m+[m[32m        sessions[session_id].clear_history()[m
[32m+[m[32m    return {"status": "cleared"}[m
[32m+[m
[32m+[m
[32m+[m[32m# Kept for backward compatibility with whatever was already calling /ask.[m
[32m+[m[32m# Internally just delegates to the same logic as /chat. Safe to remove once[m
[32m+[m[32m# nothing references it anymore.[m
[32m+[m[32mclass AskRequest(BaseModel):[m
[32m+[m[32m    session_id: str[m
[32m+[m[32m    message: str[m
[32m+[m[32m    topic_context: str = ""[m
[32m+[m[32m    difficulty: str = "Intermediate"[m
[32m+[m
 [m
[31m-    return {[m
[31m-        "success": True,[m
[31m-        "response": response[m
[31m-    }[m
\ No newline at end of file[m
[32m+[m[32m@app.post("/ask", response_model=ChatResponse)[m
[32m+[m[32mdef ask(req: AskRequest):[m
[32m+[m[32m    """Legacy endpoint, preserved so anything still calling /ask keeps working."""[m
[32m+[m[32m    return chat(req)[m
