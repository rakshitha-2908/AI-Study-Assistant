# AI Study Assistant

An AI-powered study companion that helps students learn computer science topics through interactive conversations, personalized explanations, study roadmaps, quizzes, and answer evaluation.

## Live Demo

* Frontend: https://ai-study-assistant-beryl.vercel.app
* Backend API: https://ai-study-assistant-nb9m.onrender.com

---

## Features

### Intelligent Study Assistant

* Ask questions about Computer Science topics.
* Receive concise explanations, detailed lessons, or structured study plans.
* Multi-turn conversations with context retention.

### Intent-Aware Responses

The assistant automatically detects user intent and adapts its responses:

* Explain Mode

  * Direct explanations with examples.
* Teach Mode

  * Lesson-style teaching with intuition and examples.
* Plan Mode

  * Generates structured learning roadmaps.
* Quiz Mode

  * Creates practice questions and interview-style quizzes.
* Debug Mode

  * Reviews code and identifies issues.

### Quiz System

* Generate quizzes for any topic.
* Adjustable difficulty levels.
* Evaluate submitted answers.
* Receive feedback and scoring.

### Study Tools

* Topic selection.
* Difficulty selection.
* Session management.
* Export study notes.
* Conversation history tracking.

---

## Tech Stack

### Frontend

* React
* Vite
* Tailwind CSS
* React Markdown

### Backend

* FastAPI
* Python
* Pydantic

### AI

* GitHub Models
* GPT-4o Mini
* OpenAI SDK

### Deployment

* Vercel (Frontend)
* Render (Backend)

---

## Architecture

Frontend (React + Vite)
↓
FastAPI Backend
↓
StudyAgent
↓
GitHub Models (GPT-4o Mini)

The frontend communicates with the FastAPI backend, which manages sessions, conversation history, quiz generation, answer evaluation, and AI interactions through GitHub Models.

---

## Project Structure

```text
AI-Study-Assistant/
│
├── fastapi_main.py
├── requirements.txt
│
├── src/
│   └── agent/
│       ├── study_agent.py
│       ├── agent_client.py
│       └── config.py
│
└── study-assistant-web/
    ├── src/
    │   ├── components/
    │   ├── api/
    │   ├── utils/
    │   └── App.jsx
    │
    └── package.json
```

---

## Installation

### Backend

```bash
git clone https://github.com/rakshitha-2908/AI-Study-Assistant.git

cd AI-Study-Assistant

python -m venv .venv

source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
GITHUB_TOKEN=your_github_models_token
```

Run the backend:

```bash
uvicorn fastapi_main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

---

### Frontend

```bash
cd study-assistant-web

npm install

npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## API Endpoints

### Create Session

```http
POST /session/new
```

### Chat

```http
POST /chat
```

### Generate Quiz

```http
POST /quiz/generate
```

### Evaluate Quiz

```http
POST /quiz/evaluate
```

### Clear Session

```http
POST /session/{session_id}/clear
```

### Health Check

```http
GET /health
```

---

## Key Highlights

* Full-stack AI application.
* Session-based conversation memory.
* Intent-aware tutoring system.
* Dynamic quiz generation and evaluation.
* Production deployment with Vercel and Render.
* Responsive user interface.
* Exportable study notes.

---

## Future Improvements

* User authentication.
* Persistent database storage.
* PDF study guide generation.
* Progress tracking dashboard.
* Flashcard generation.
* Learning analytics.

---

## Author

Rakshitha Badugu

Built as a full-stack AI learning platform combining modern web development, FastAPI APIs, and Large Language Models to create an interactive study experience.
