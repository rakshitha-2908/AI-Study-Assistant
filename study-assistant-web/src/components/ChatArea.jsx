import { useEffect, useRef, useState } from "react";
import { FiArrowUp, FiCode, FiMap, FiEdit2, FiTool } from "react-icons/fi";
import { sendChatMessage, detectIntentForDisplay } from "../api/client";

const QUICK_ACTIONS = [
  {
    label: "Explain a Concept",
    prompt: "What is a stack? Explain with examples",
    icon: FiCode,
    bg: "bg-brand-light",
    text: "text-brand-dark",
  },
  {
    label: "Create Study Plan",
    prompt: "Create a 30-day DSA roadmap for beginners",
    icon: FiMap,
    bg: "bg-peach-light",
    text: "text-peach-dark",
  },
  {
    label: "Generate Quiz",
    prompt: "Give me 5 binary search interview questions",
    icon: FiEdit2,
    bg: "bg-mint-light",
    text: "text-mint-dark",
  },
  {
    label: "Debug Code",
    prompt: "What's wrong with my recursive function?",
    icon: FiTool,
    bg: "bg-pink-light",
    text: "text-pink-dark",
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

/**
 * Center chat panel: quick-action cards (shown when empty), scrollable
 * message list, and a fixed input box at the bottom.
 *
 * Props:
 *   sessionId, topic, difficulty — passed straight through to /chat
 *   messages, setMessages — lifted up to App so other views can read history later
 */
function ChatArea({ sessionId, topic, difficulty, messages, setMessages }) {
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const scrollRef = useRef(null);

  // Auto-scroll to the latest message whenever the list changes.
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
    <div className="flex flex-col h-full">
      {/* Header + quick actions, only shown when chat is empty */}
      {messages.length === 0 && (
        <div className="px-6 pt-6 pb-2">
          <h1 className="text-xl font-semibold text-gray-900">What would you like to study?</h1>
          <p className="text-sm text-gray-500 mt-1 mb-4">
            Ask a question, request a plan, or quiz yourself on anything.
          </p>
          <div className="grid grid-cols-2 gap-2">
            {QUICK_ACTIONS.map(({ label, prompt, icon: Icon, bg, text }) => (
              <button
                key={label}
                onClick={() => handleSend(prompt)}
                className={`${bg} rounded-xl p-3.5 text-left transition-transform hover:-translate-y-0.5`}
              >
                <Icon className={text} size={18} />
                <p className={`${text} text-sm font-medium mt-2`}>{label}</p>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Scrollable message list */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-4 flex flex-col gap-3">
        {messages.map((msg, i) =>
          msg.role === "user" ? (
            <div
              key={i}
              className="self-end max-w-[75%] bg-brand text-brand-light px-4 py-2.5 rounded-2xl rounded-br-md text-sm"
            >
              {msg.content}
            </div>
          ) : (
            <div
              key={i}
              className="self-start max-w-[85%] bg-gray-100 px-4 py-3 rounded-2xl rounded-bl-md text-sm leading-relaxed text-gray-800"
            >
              {msg.intent && (
                <span
                  className={`inline-block text-[11px] font-medium px-2.5 py-0.5 rounded-full mb-2 ${
                    INTENT_STYLES[msg.intent] || INTENT_STYLES.general
                  }`}
                >
                  {msg.intent}
                </span>
              )}
              <div className="whitespace-pre-wrap">{msg.content}</div>
            </div>
          )
        )}

        {isLoading && (
          <div className="self-start max-w-[85%] bg-gray-100 px-4 py-3 rounded-2xl rounded-bl-md text-sm text-gray-400">
            <span className="inline-flex gap-1 items-center">
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
              <span className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" />
            </span>
          </div>
        )}

        {error && (
          <div className="self-start max-w-[85%] bg-red-50 text-red-600 px-4 py-2.5 rounded-xl text-sm">
            {error}
          </div>
        )}
      </div>

      {/* Fixed input box */}
      <div className="px-6 pb-6 pt-2">
        <div className="flex items-center gap-2 bg-gray-50 border border-gray-200 rounded-full px-4 py-1.5">
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
            className="w-8 h-8 flex items-center justify-center rounded-full bg-brand text-white disabled:opacity-40 transition-opacity"
          >
            <FiArrowUp size={15} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatArea;