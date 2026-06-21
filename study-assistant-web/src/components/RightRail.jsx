import { FiHash, FiBookOpen, FiBarChart2 } from "react-icons/fi";

const TOPIC_OPTIONS = [
  "General CS",
  "Data Structures & Algorithms",
  "Operating Systems",
  "Database Systems",
  "System Design",
  "Computer Networks",
  "OOP & Design Patterns",
];

const DIFFICULTY_OPTIONS = ["Beginner", "Intermediate", "Interview-ready"];

const PLACEHOLDER_TOPICS = ["Stacks", "Binary Search", "Sliding Window"];

function toTopicLabel(message) {
  const trimmed = message.trim();
  return trimmed.length > 32 ? trimmed.slice(0, 32) + "…" : trimmed;
}

function StatRow({ icon: Icon, label, value }) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 text-gray-500">
        <Icon size={14} />
        <span className="text-xs">{label}</span>
      </div>
      <span className="text-sm font-medium text-gray-800">{value}</span>
    </div>
  );
}

/**
 * Right rail: topic + difficulty selectors, Session Overview card,
 * Topics Covered (derived from user messages, falls back to placeholder
 * chips when chat is empty), and Quick Stats.
 */
function RightRail({ topic, setTopic, difficulty, setDifficulty, sessionId, messages, quizAttempts = 0 }) {
  const shortSessionId = sessionId ? sessionId.slice(0, 8) : "—";
  const userMessages = messages.filter((m) => m.role === "user");
  const messageCount = messages.length;

  const detectedTopics = [...new Set(userMessages.map((m) => toTopicLabel(m.content)))].slice(-6);
  const topicsToShow = detectedTopics.length > 0 ? detectedTopics : PLACEHOLDER_TOPICS;
  const isPlaceholder = detectedTopics.length === 0;

  return (
    <div className="h-full bg-white border-l border-gray-100 p-6 flex flex-col gap-7 overflow-y-auto">
      {/* Topic selector */}
      <div>
        <label className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2 block">
          Subject
        </label>
        <select
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="w-full text-sm bg-gray-50 border border-gray-200 rounded-xl px-3 py-2.5 outline-none focus:border-brand transition-colors"
        >
          {TOPIC_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>

      {/* Difficulty selector */}
      <div>
        <label className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2 block">
          Depth level
        </label>
        <div className="flex flex-col gap-1.5">
          {DIFFICULTY_OPTIONS.map((option) => {
            const isActive = difficulty === option;
            return (
              <button
                key={option}
                onClick={() => setDifficulty(option)}
                className={`text-sm text-left px-3 py-2.5 rounded-xl transition-colors ${
                  isActive
                    ? "bg-brand-light text-brand-dark font-medium"
                    : "bg-gray-50 text-gray-500 border border-gray-200 hover:border-gray-300"
                }`}
              >
                {option}
              </button>
            );
          })}
        </div>
      </div>

      {/* Session Overview */}
      <div className="bg-gray-50 rounded-2xl p-4 border border-gray-100">
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-3">
          Session Overview
        </p>
        <div className="flex flex-col gap-2.5">
          <StatRow icon={FiHash} label="Session ID" value={shortSessionId} />
          <StatRow icon={FiBookOpen} label="Topic" value={topic} />
          <StatRow icon={FiBarChart2} label="Difficulty" value={difficulty} />
          <StatRow icon={FiHash} label="Messages" value={messageCount} />
        </div>
      </div>

      {/* Topics Covered */}
      <div>
        <p className="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2.5">
          Topics Covered
        </p>
        <div className="flex flex-wrap gap-1.5">
          {topicsToShow.map((t, i) => (
            <span
              key={i}
              className={`text-xs px-2.5 py-1 rounded-full border ${
                isPlaceholder
                  ? "bg-gray-50 text-gray-400 border-gray-200 border-dashed"
                  : "bg-brand-light text-brand-dark border-brand-light"
              }`}
            >
              {t}
            </span>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="bg-gradient-to-br from-brand-light to-white rounded-2xl p-4 border border-brand-light mt-auto">
        <p className="text-xs font-semibold text-brand-dark/70 uppercase tracking-wide mb-3">
          Quick Stats
        </p>
        <div className="flex flex-col gap-2.5">
          <StatRow icon={FiHash} label="Questions Asked" value={userMessages.length} />
          <StatRow icon={FiBarChart2} label="Quiz Attempts" value={quizAttempts} />
          <div className="flex items-center justify-between">
            <span className="text-xs text-gray-500">Status</span>
            <span className="flex items-center gap-1.5 text-xs font-medium text-emerald-600">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Active
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RightRail;