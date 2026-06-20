import { FiMessageSquare, FiEdit3, FiClock, FiDownload } from "react-icons/fi";

const NAV_ITEMS = [
  { key: "chat", label: "Chat", icon: FiMessageSquare },
  { key: "quiz", label: "Quiz Mode", icon: FiEdit3 },
  { key: "topics", label: "Topics Covered", icon: FiClock },
  { key: "export", label: "Export Notes", icon: FiDownload },
];

function Sidebar({ activeView, onNavigate }) {
  return (
    <div className="bg-violet-800 h-full flex flex-col gap-8 p-5">
      <div className="flex items-center gap-2 px-1">
        <span className="text-lg">📚</span>
        <span className="text-white font-semibold text-sm">
          AI Study Assistant
        </span>
      </div>

      <nav className="flex flex-col gap-2">
        {NAV_ITEMS.map(({ key, label, icon: Icon }) => {
          const isActive = activeView === key;

          return (
            <button
              key={key}
              onClick={() => onNavigate(key)}
              className={`flex items-center gap-3 px-3 py-3 rounded-xl text-sm transition-all text-left
                ${
                  isActive
                    ? "bg-violet-100 text-violet-800 font-semibold"
                    : "text-white/80 hover:bg-white/10 hover:text-white"
                }`}
            >
              <Icon size={18} />
              {label}
            </button>
          );
        })}
      </nav>
    </div>
  );
}

export default Sidebar;