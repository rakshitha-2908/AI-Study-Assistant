import { useEffect, useState } from "react";
import { createSession } from "./api/client";
import Sidebar from "./components/Sidebar";
import ChatArea from "./components/ChatArea";
import RightRail from "./components/RightRail";

function App() {
  const [sessionId, setSessionId] = useState(null);
  const [sessionError, setSessionError] = useState(null);
  const [messages, setMessages] = useState([]);
  const [topic, setTopic] = useState("General CS");
  const [difficulty, setDifficulty] = useState("Intermediate");
  const [activeView, setActiveView] = useState("chat");
  // Tracked here (not yet wired to a quiz UI) so RightRail's Quick Stats
  // has a real field to read once quiz mode is built. Stays 0 until then.
  const [quizAttempts, setQuizAttempts] = useState(0);

  useEffect(() => {
    createSession()
      .then(setSessionId)
      .catch((err) => setSessionError(err.message));
  }, []);

  if (sessionError) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-gray-50">
        <div className="text-center max-w-sm">
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
      <div className="h-screen w-screen flex items-center justify-center bg-gray-50">
        <p className="text-gray-500 text-sm">Connecting...</p>
      </div>
    );
  }

  return (
    <div className="h-screen w-screen flex bg-white overflow-hidden">
      {/* Sidebar — fixed width, full height */}
      <div className="w-[260px] flex-shrink-0 h-full">
        <Sidebar activeView={activeView} onNavigate={setActiveView} />
      </div>

      {/* Chat area — fills remaining space */}
      <div className="flex-1 h-full min-w-0">
        <ChatArea
          sessionId={sessionId}
          topic={topic}
          difficulty={difficulty}
          messages={messages}
          setMessages={setMessages}
        />
      </div>

      {/* Right rail — fixed width, hidden below lg breakpoint */}
      <div className="w-[320px] flex-shrink-0 h-full hidden lg:block">
        <RightRail
          topic={topic}
          setTopic={setTopic}
          difficulty={difficulty}
          setDifficulty={setDifficulty}
          sessionId={sessionId}
          messages={messages}
          quizAttempts={quizAttempts}
        />
      </div>
    </div>
  );
}

export default App;