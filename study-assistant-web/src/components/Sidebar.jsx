import {
  FiMessageSquare,
  FiEdit3,
  FiClock,
  FiDownload,
  FiMenu,
  FiChevronRight,
} from "react-icons/fi";

const NAV_ITEMS = [
  { key: "chat", label: "Chat", icon: FiMessageSquare },
  { key: "quiz", label: "Quiz Mode", icon: FiEdit3 },
  { key: "topics", label: "Topics Covered", icon: FiClock },
  { key: "export", label: "Export Notes", icon: FiDownload },
];

function Sidebar({ activeView, onNavigate, onExportNotes, collapsed, onToggleCollapse }) {
  return (
    <div className="bg-violet-800 h-full flex flex-col gap-8 p-5 transition-all duration-300 ease-in-out">
      <div className="flex items-center justify-between gap-2 px-1">
        <div className={`flex items-center gap-2 ${collapsed ? "justify-center w-full" : ""}`}>
          <span className="text-lg">📚</span>
          <span
            className={`text-white font-semibold text-sm transition-all duration-200 ${
              collapsed ? "opacity-0 w-0 overflow-hidden" : "opacity-100"
            }`}
          >
            AI Study Assistant
          </span>
        </div>

        <button
          type="button"
          onClick={onToggleCollapse}
          className="inline-flex items-center justify-center rounded-lg bg-white/10 p-2 text-white transition hover:bg-white/20"
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {collapsed ? <FiChevronRight size={18} /> : <FiMenu size={18} />}
        </button>
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
              className={`flex items-center gap-3 px-3 py-3 rounded-xl text-sm transition-all duration-200 ${
                collapsed ? "justify-center" : "justify-start"
              } ${
                isActive
                  ? "bg-violet-100 text-violet-800 font-semibold"
                  : "text-white/80 hover:bg-white/10 hover:text-white"
              }`}
            >
              <Icon size={18} />
              <span className={`${collapsed ? "hidden" : "block"}`}>{label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}

export default Sidebar;