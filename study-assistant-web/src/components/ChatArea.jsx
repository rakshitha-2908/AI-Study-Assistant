import { useEffect, useRef, useState } from "react";
import { FiArrowUp, FiCode, FiMap, FiEdit2, FiTool, FiUser } from "react-icons/fi";
import { sendChatMessage, detectIntentForDisplay } from "../api/client";
import MarkdownMessage from "./MarkdownMessage";

const QUICK_ACTIONS = [
  {
    label: "Explain a Concept",
    desc: "Get a clear, direct answer",
    prompt: "What is a stack? Explain with examples",
    icon: FiTool,
    bg: "bg-brand-light",
    text: "text-brand-dark",
    iconBg: "bg-brand/10",
  },
  {
    label: "Create Study Plan",
    desc: "Structured day-by-day roadmap",
    prompt: "Create a 30-day DSA roadmap for beginners",
    icon: FiMap,
    bg: "bg-peach-light",
    text: "text-peach-dark",
    iconBg: "bg-[#d85a30]/10",
  },
  {
    label: "Generate Quiz",
    desc: "Test yourself on a topic",
    prompt: "Give me 5 binary search interview questions",
    icon: FiEdit2,
    bg: "bg-mint-light",
    text: "text-mint-dark",
    iconBg: "bg-[#0f6e56]/10",
  },
  {
    label: "Debug Code",
    desc: "Find and fix the issue",
    prompt: "What's wrong with my recursive function?",
    icon: FiTool,
    bg: "bg-pink-light",
    text: "text-pink-dark",
    iconBg: "bg-[#993556]/10",
  },
];

const INTENT_STYLES = {
  explain: "bg-brand-light text-brand-dark",
  plan: "bg-peach-light text-peach-dark",
  quiz: "bg-mint-light text-mint-dark",
  teach: "bg-pink-light text-pink-dark",
  debug: "bg-pink-light text-pink-dark",
  general: "bg-gray-100 text-gray-500",
};

function AssistantAvatar() {
  return (
    <div className="w-8 h-8 rounded-full bg-brand flex items-center justify-center flex-shrink-0 text-sm shadow-sm">
      🧠
    </div>
  );
}

function UserAvatar() {
  return (
    <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center flex-shrink-0">
      <FiUser size={14} className="text-gray-500" />
    </div>
  );
}

/**
 * Center chat panel. Fills all space given to it by the parent flex layout
 * in App.jsx — no fixed widths or centering here, just height: 100% behavior.
 */
function ChatArea({ sessionId, topic, difficulty, messages, setMessages }) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, isLoading]);

  async function handleSend(text) {
    const messageText = (text ?? input).trim();
    if (!messageText || isLoading) return;

    setError(null);
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: messageText }]);
    setIsLoading(true);

    try {
      const response = await sendChatMessage({
        sessionId,
        message: messageText,
        topicContext: topic,
        difficulty,
      });
      const intent = detectIntentForDisplay(messageText);
      setMessages((prev) => [...prev, { role: "assistant", content: response, intent }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex flex-col h-full bg-gray-50/50">
      {messages.length === 0 ? (
        // Welcome state
        <div className="flex-1 flex flex-col items-center justify-center px-8">
          <div className="w-16 h-16 rounded-2xl bg-brand-light flex items-center justify-center text-3xl mb-5 shadow-sm">
            🧠
          </div>
          <h1 className="text-2xl font-semibold text-gray-900">What would you like to study?</h1>
          <p className="text-sm text-gray-500 mt-2 mb-8 text-center max-w-md">
            Ask a question, request a plan, or quiz yourself on anything — CS fundamentals to interview prep.
          </p>
          <div className="grid grid-cols-2 gap-3 w-full max-w-xl">
            {QUICK_ACTIONS.map(({ label, desc, prompt, icon: Icon, bg, text, iconBg }) => (
              <button
                key={label}
                onClick={() => handleSend(prompt)}
                className={`${bg} rounded-2xl p-5 text-left transition-all hover:-translate-y-0.5 hover:shadow-lg shadow-sm`}
              >
                <div className={`${iconBg} w-9 h-9 rounded-xl flex items-center justify-center mb-3`}>
                  <Icon className={text} size={17} />
                </div>
                <p className={`${text} text-sm font-semibold`}>{label}</p>
                <p className={`${text} text-xs opacity-70 mt-1`}>{desc}</p>
              </button>
            ))}
          </div>
        </div>
      ) : (
        // Message list
        <div ref={scrollRef} className="flex-1 overflow-y-auto">
          <div className="max-w-3xl mx-auto px-8 py-8 flex flex-col gap-7">
            {messages.map((msg, i) =>
              msg.role === "user" ? (
                <div key={i} className="flex items-start gap-3 justify-end">
                  <div className="max-w-[70%] bg-gradient-to-br from-brand to-brand-dark text-white px-5 py-3 rounded-2xl rounded-tr-md text-sm shadow-md">
                    {msg.content}
                  </div>
                  <UserAvatar />
                </div>
              ) : (
                <div key={i} className="flex items-start gap-3">
                  <AssistantAvatar />
                  <div className="max-w-[80%] bg-white px-5 py-4 rounded-2xl rounded-tl-md shadow-sm border border-gray-100">
                    {msg.intent && (
                      <span
                        className={`inline-block text-[11px] font-medium px-2.5 py-0.5 rounded-full mb-2.5 ${
                          INTENT_STYLES[msg.intent] || INTENT_STYLES.general
                        }`}
                      >
                        {msg.intent}
                      </span>
                    )}
                    <MarkdownMessage content={msg.content} />
                  </div>
                </div>
              )
            )}

            {isLoading && (
              <div className="flex items-start gap-3">
                <AssistantAvatar />
                <div className="bg-white px-5 py-4 rounded-2xl rounded-tl-md shadow-sm border border-gray-100">
                  <div className="flex items-center gap-2 text-xs text-gray-400">
                    <span className="inline-flex gap-1 items-center">
                      <span className="w-1.5 h-1.5 bg-brand/40 rounded-full animate-bounce [animation-delay:-0.3s]" />
                      <span className="w-1.5 h-1.5 bg-brand/40 rounded-full animate-bounce [animation-delay:-0.15s]" />
                      <span className="w-1.5 h-1.5 bg-brand/40 rounded-full animate-bounce" />
                    </span>
                    Thinking...
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="flex items-start gap-3">
                <AssistantAvatar />
                <div className="bg-red-50 text-red-600 px-5 py-3 rounded-2xl rounded-tl-md text-sm border border-red-100">
                  {error}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Fixed input box */}
      <div className="px-8 py-5 border-t border-gray-100 bg-white/60">
        <div className="max-w-3xl mx-auto flex items-center gap-2 bg-white border border-gray-200 rounded-full px-5 py-2 shadow-sm focus-within:border-brand/40 focus-within:shadow-md transition-all">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask anything..."
            className="flex-1 bg-transparent outline-none text-sm py-2"
            disabled={isLoading}
          />
          <button
            onClick={() => handleSend()}
            disabled={isLoading || !input.trim()}
            className="w-9 h-9 flex items-center justify-center rounded-full bg-brand text-white disabled:opacity-30 transition-opacity hover:bg-brand-dark"
          >
            <FiArrowUp size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatArea;