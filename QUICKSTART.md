# AI Study Assistant - Quick Reference

## 🚀 Getting Started (30 seconds)

```bash
# 1. Activate environment
.\.venv\Scripts\Activate.ps1

# 2. Run the app
python src/main.py

# 3. Type a topic or question
You: Python Basics
```

## 📋 Available Commands

| Command | Effect |
|---------|--------|
| `Your topic/question` | Get AI response |
| `save` | Save conversation to file |
| `clear` | Reset conversation history |
| `exit` | Quit application |

## 🧪 Testing

```bash
# Run all tests
pytest tests/test_agent.py -v

# Run specific test
pytest tests/test_agent.py::TestStudyAgent::test_study_agent_initializes -v
```

## 📁 File Structure

```
AI-Study-Assistant/
├── src/
│   ├── main.py                    # Start here!
│   ├── agent/
│   │   ├── config.py              # GitHub token setup
│   │   ├── agent_client.py        # Conversation history
│   │   └── study_agent.py         # AI engine
│   └── utils/
│       └── helpers.py             # Formatting & saving
├── tests/
│   ├── test_agent.py              # Unit tests
│   └── conftest.py                # Test config
├── requirements.txt               # Dependencies
├── .env                           # Your config (DON'T commit!)
├── .env.example                   # Template (use this to create .env)
├── conftest.py                    # Root pytest config
├── UPGRADE.md                     # Full upgrade guide
└── CHANGELOG.md                   # What changed
```

## ⚙️ Setup Checklist

- [ ] Create `.env` file (copy from `.env.example`)
- [ ] Add `GITHUB_TOKEN=your_token_here` to `.env`
- [ ] Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
- [ ] Run tests: `pytest tests/test_agent.py -v`
- [ ] Start app: `python src/main.py`

## 🔑 Key Features

✨ **Multi-Turn Memory**
- Last 10 messages stored automatically
- Ask follow-up questions with context

🎓 **Dual Mode**
- Topics → Study plans with objectives
- Questions → Direct Q&A answers

💾 **Session Saving**
- Type `save` to export conversations
- Saved in `/transcripts` folder

🧪 **Well Tested**
- 3 unit tests included
- All passing ✅

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "ModuleNotFoundError" | Activate venv & run from project root |
| "GITHUB_TOKEN not set" | Create `.env` with your token |
| Tests fail | Run `pip install -r requirements.txt` |
| Can't save transcript | Have at least 1 conversation first |

## 📚 Learning Resources

- Full guide: See `UPGRADE.md`
- Changes list: See `CHANGELOG.md`
- Code examples: See docstrings in `src/`
- Tests: See `tests/test_agent.py`

## 🎯 Common Use Cases

### Create Study Plan
```
You: Machine Learning Fundamentals
Assistant: [Study plan with objectives, concepts, exercises]
```

### Ask Follow-up Questions
```
You: What are neural networks?
Assistant: [Response with context from previous questions]

You: How are they trained?
Assistant: [Contextual follow-up answer]
```

### Save Your Work
```
You: save
✓ Session saved to: transcripts/session_20260611_143022.txt
```

## 🔐 Security

✅ Token stored in `.env` (git-ignored)
✅ Never hardcode secrets
✅ Use `.env.example` as template
✅ GitHub PAT with minimal permissions

## 📦 What You Need

- Python 3.8+
- GitHub Personal Access Token
- That's it! (Only 3 dependencies)

## 🎓 Beginner Tips

1. Start with simple topics like "Python Basics"
2. Ask follow-up questions to explore deeper
3. Use `save` to review your learning sessions
4. Check `/transcripts` folder for saved conversations
5. Read docstrings in code (very helpful!)

## 🚀 Next Steps

1. Read `UPGRADE.md` for full details
2. Run `pytest tests/test_agent.py -v` to verify setup
3. Start `python src/main.py` and begin learning!
4. Type `save` after each session to keep records

---

**Ready to learn? Type:** `python src/main.py` 📚
