import { useEffect, useState } from "react";
import { createSession } from "./api/client";
import Sidebar from "./components/Sidebar";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [sessionError, setSessionError] = useState(null);
  const [messages, setMessages] = useState([]);
  const [topic, setTopic] = useState("General CS");
  const [difficulty, setDifficulty] = useState("Intermediate");
  const [activeView, setActiveView] = useState("chat");

  // Create a session once when the app first loads.
  useEffect(() => {
    createSession()
      .then(setSessionId)
      .catch((err) => setSessionError(err.message));
  }, []);

  if (sessionError) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 font-medium mb-2">Couldn't connect to the backend.</p>
          <p className="text-sm text-gray-500">{sessionError}</p>
          <p className="text-sm text-gray-500 mt-2">
            Make sure FastAPI is running on http://localhost:8000
          </p>
        </div>
      </div>
    );
  }

  if (!sessionId) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-500">Connecting...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6 flex justify-center">
      <div className="w-full max-w-7xl rounded-3xl overflow-hidden grid grid-cols-[220px_1fr_260px] shadow-sm border border-gray-200 bg-white min-h-[640px]">
        {/* Sidebar */}
        <Sidebar activeView={activeView} onNavigate={setActiveView} />

        {/* Main chat area placeholder */}
        <div className="p-6">
          <p className="text-gray-400 text-sm">
            Session connected: <span className="font-mono text-xs">{sessionId}</span>
          </p>
          <p className="text-gray-400 text-sm mt-2">Chat area goes here</p>
        </div>

        {/* Right rail placeholder */}
        <div className="bg-gray-50 border-l border-gray-200 p-5">
          <p className="text-gray-400 text-sm">Right rail goes here</p>
        </div>
      </div>
    </div>
  );
}

export default App;