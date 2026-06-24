# 📁 AI Study Assistant - Project Structure

## ✅ Current Project Layout

```
AI-Study-Assistant/
│
├── 📄 .env                             # Local environment variables (not committed)
├── 📄 .env.example                     # Environment template
├── 📄 CHANGELOG.md                     # Change history
├── 📄 COMPLETION_SUMMARY.md            # Project summary
├── 📄 LICENSE                          # Project license
├── 📄 PROJECT_STRUCTURE.md             # This file
├── 📄 QUICKSTART.md                    # Quick start guide
├── 📄 README.md                        # Root project overview
├── 📄 UPGRADE.md                       # Upgrade and migration guide
├── 📄 conftest.py                      # Pytest configuration
├── 📄 fastapi_main.py                  # FastAPI backend entrypoint
├── 📄 requirements.txt                 # Python dependencies
├── 📄 streamlit_app.py                 # Streamlit UI entrypoint
├── 📄 tore fastapi_main.py             # Duplicate / temporary file
│
├── 📁 docs/                            # Documentation resources
│   ├── 📄 architecture.md
│   └── 📁 screenshots/
│
├── 📁 src/                             # Python backend core
│   ├── 📄 main.py
│   ├── 📁 agent/
│   │   ├── 📄 __init__.py
│   │   ├── 📄 agent_client.py
│   │   ├── 📄 config.py
│   │   └── 📄 study_agent.py
│   └── 📁 utils/
│       └── 📄 helpers.py
│
├── 📁 study-assistant-web/             # React + Tailwind frontend
│   ├── 📄 README.md
│   ├── 📄 index.html
│   ├── 📄 package.json
│   ├── 📄 package-lock.json
│   ├── 📄 vite.config.js
│   ├── 📁 public/
│   ├── 📁 src/
│   │   ├── 📄 App.css
│   │   ├── 📄 App.jsx
│   │   ├── 📄 index.css
│   │   ├── 📄 main.jsx
│   │   ├── 📁 api/
│   │   │   └── 📄 client.js
│   │   ├── 📁 assets/
│   │   ├── 📁 components/
│   │   │   ├── 📄 ChatArea.jsx
│   │   │   ├── 📄 MarkdownMessage.jsx
│   │   │   ├── 📄 QuizView.jsx
│   │   │   ├── 📄 RightRail.jsx
│   │   │   └── 📄 Sidebar.jsx
│   │   └── 📁 utils/
│   │       └── 📄 exportNotes.js
│   └── 📄 eslint.config.js
└── 📁 tests/
    └── 📄 test_agent.py
```

---

## 📌 Notes

- `study-assistant-web/` contains the React frontend for the AI Study Assistant.
- `src/` contains the Python backend and core study agent logic.
- `fastapi_main.py` and `streamlit_app.py` are alternate app entrypoints.
- `tore fastapi_main.py` appears to be a duplicate or temporary file and may be removable.
- `conftest.py` at the project root configures pytest.

---

## 🔧 Highlights

- The frontend uses React, Tailwind CSS, and `react-icons`.
- The backend uses Python with a simple agent architecture under `src/agent/`.
- Notes export is implemented in `study-assistant-web/src/utils/exportNotes.js`.
- The sidebar and layout are implemented in `study-assistant-web/src/components/Sidebar.jsx`.

---

## 📍 Quick Access

- `src/main.py` — primary Python CLI entrypoint
- `study-assistant-web/src/App.jsx` — React app shell
- `study-assistant-web/src/components/Sidebar.jsx` — sidebar navigation UI
- `study-assistant-web/src/utils/exportNotes.js` — export notes helper
- `tests/test_agent.py` — test coverage for core logic
- `docs/architecture.md` — architecture documentation

---

**Start Learning**: `python src/main.py` 📚
