const API_BASE = "http://127.0.0.1:8000";

export async function createSession() {
  const response = await fetch(`${API_BASE}/session/new`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error("Failed to create session");
  }

  const data = await response.json();
  return data.session_id;
}