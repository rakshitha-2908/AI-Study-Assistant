import { FiMessageSquare, FiEdit3, FiClock, FiDownload } from "react-icons/fi";

const NAV_ITEMS = [
  { key: "chat", label: "Chat", icon: FiMessageSquare },
  { key: "quiz", label: "Quiz Mode", icon: FiEdit3 },
  { key: "topics", label: "Topics Covered", icon: FiClock },
  { key: "export", label: "Export Notes", icon: FiDownload },
];

function Sidebar({ activeView, onNavigate, onExportNotes }) {
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
          const handleClick = () => {
            if (key === "export") {
              onExportNotes?.();
              return;
            }
            if (key === "topics") {
              return;
            }
            onNavigate(key);
          };

          return (
            <button
              key={key}
              type="button"
              onClick={handleClick}
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