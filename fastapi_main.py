from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from src.agent.config import load_config
from src.agent.study_agent import StudyAgent

app = FastAPI(
    title="AI Study Assistant API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    return {"status": "healthy"}

config = load_config()
agent = StudyAgent(config)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "AI Study Assistant API is running"}


@app.post("/ask")
def ask(request: QuestionRequest):
    response = agent.run(request.question)

    return {
        "success": True,
        "response": response
    }