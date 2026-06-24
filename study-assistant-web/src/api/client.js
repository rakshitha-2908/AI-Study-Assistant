sion. Call this once when the app loads. */
export async function createSession() {
  const res = await fetch(`${BASE_URL}/session/new`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to create session");
  const data = await res.json();
  return data.session_id;
}

/** Send a chat message, get the assistant's response back. */
export async function sendChatMessage({ sessionId, message, topicContext, difficulty }) {
  const data = await postJSON("/chat", {
    session_id: sessionId,
    message,
    topic_context: topicContext || "",
    difficulty: difficulty || "Intermediate",
  });
  return data.response;
}

/**
 * Mirrors the backend's detect_intent() keyword logic, for display purposes
 * only (showing an "explain" / "plan" / etc. badge above assistant messages).
 * The actual intent routing happens server-side in study_agent.py — this is
 * just so the UI doesn't have to guess blindly or wait on a backend change.
 */
export function detectIntentForDisplay(message) {
  const msg = message.toLowerCase();
  const planKeywords = ["roadmap", "plan", "schedule", "days", "weeks", "curriculum", "learning path"];
  const quizKeywords = ["quiz", "test me", "interview questions", "practice questions", "give me questions"];
  const teachKeywords = ["teach me", "help me understand", "i don't get", "walk me through"];
  const debugKeywords = ["what's wrong", "why isn't", "fix this", "debug", "review my", "error in"];
  const explainKeywords = ["what is", "what are", "define", "how does", "how do", "explain"];

  if (planKeywords.some((k) => msg.includes(k))) return "plan";
  if (quizKeywords.some((k) => msg.includes(k))) return "quiz";
  if (debugKeywords.some((k) => msg.includes(k))) return "debug";
  if (teachKeywords.some((k) => msg.includes(k))) return "teach";
  if (explainKeywords.some((k) => msg.includes(k))) return "explain";
  return "general";
}

/** Generate quiz questions for a topic. */
export async function generateQuiz({ sessionId, topic, difficulty, numQuestions }) {
  const data = await postJSON("/quiz/generate", {
    session_id: sessionId,
    topic,
    difficulty: difficulty || "Intermediate",
    num_questions: numQuestions || 5,
  });
  return data.questions;
}

/** Submit answers and get evaluated feedback + score. */
export async function evaluateQuiz({ sessionId, topic, questions, userAnswers }) {
  const data = await postJSON("/quiz/evaluate", {
    session_id: sessionId,
    topic,
    questions,
    user_answers: userAnswers,
  });
  return data.feedback;
}

/** Clear conversation history for the current session. */
export async function clearSession(sessionId) {
  const res = await fetch(`${BASE_URL}/session/${sessionId}/clear`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to clear session");
  return res.json();
}/**
 * All calls to the FastAPI backend live here. Components never call fetch()
 * directly — they import functions from this file. If the backend URL or
 * an endpoint shape changes, this is the only file that needs updating.
 */

const BASE_URL = "https://ai-study-assistant-nb9m.onrender.com";

async function postJSON(path, body) {
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${path} failed: ${res.status} ${text}`);
  }
  return res.json();
}

/** Create a new ses