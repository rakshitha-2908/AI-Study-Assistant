# AI Study Assistant - Upgrade Documentation

## ✨ What's New

Your AI Study Assistant has been upgraded to be a polished, production-ready application. Here's what changed:

### 🎯 Major Features

#### 1. **Interactive CLI with Welcome Message**
- Beautiful welcome banner on startup
- Interactive input loop for asking multiple questions
- Clean, formatted output with visual separators
- Special commands: `exit`, `save`, `clear`

#### 2. **Multi-Turn Conversation Memory**
- Maintains last 10 messages in history
- Context-aware responses to follow-up questions
- Ask related questions and the AI remembers previous context
- `clear` command to start fresh conversation

#### 3. **Dual-Mode Intelligence**
- **Study Plans**: Ask about topics like "Python Basics" or "Machine Learning"
- **Q&A Mode**: Ask questions like "What is supervised learning?" or "How does a for loop work?"
- Auto-detection between study plan and question modes

#### 4. **Session Transcripts**
- `save` command exports your conversation to a timestamped text file
- Transcripts saved in `/transcripts` folder
- Perfect for reviewing or sharing your learning session

#### 5. **Comprehensive Unit Tests**
- 3 unit tests included:
  - ✓ StudyAgent initialization test
  - ✓ Prompt creation test (topics & questions)
  - ✓ Conversation history management test
- Run with: `pytest tests/test_agent.py -v`

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- GitHub Personal Access Token (with `read` access to at least one GitHub resource)

### Installation

1. **Clone/Navigate to project**
```bash
cd d:\IIIT\AI-Study-Assistant
```

2. **Create `.env` file** (copy from `.env.example`)
```bash
GITHUB_TOKEN=your_github_pat_here
```

3. **Create virtual environment** (if not already done)
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run the application**
```bash
python src/main.py
```

---

## 📝 Usage Examples

### Example 1: Create a Study Plan
```
You: Machine Learning Fundamentals
Assistant: [Generates comprehensive study plan with objectives, concepts, exercises]
```

### Example 2: Follow-up Questions
```
You: What are supervised learning algorithms?
Assistant: [Contextual answer based on previous conversation]

You: Can you give me an example?
Assistant: [References your previous questions in this session]
```

### Example 3: Save Your Session
```
You: save
✓ Session saved to: transcripts/session_20260611_143022.txt
```

### Example 4: Start Fresh
```
You: clear
✓ Conversation history cleared. Starting fresh!
```

---

## 🔧 Project Structure

```
src/
├── main.py                 # Interactive CLI entry point
├── agent/
│   ├── __init__.py
│   ├── config.py          # GitHub token configuration
│   ├── agent_client.py    # ConversationHistory class
│   └── study_agent.py     # Main StudyAgent with multi-turn support
└── utils/
    └── helpers.py         # Formatting & transcript utilities

tests/
├── test_agent.py          # 3 unit tests
└── conftest.py            # Test configuration

requirements.txt           # Python dependencies
.env.example              # Configuration template
conftest.py               # Root pytest configuration
```

---

## 🧪 Running Tests

```bash
# Run all tests with verbose output
pytest tests/test_agent.py -v

# Run a specific test
pytest tests/test_agent.py::TestStudyAgent::test_study_agent_initializes -v

# Run tests with coverage (if installed)
pytest tests/test_agent.py --cov=src --cov-report=term-missing
```

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `openai>=1.0.0` | GitHub Models API via OpenAI SDK |
| `python-dotenv>=1.0.0` | Environment variable management |
| `pytest>=7.0.0` | Unit testing framework |

---

## 🔐 Security Notes

- ✅ No Azure SDK packages (removed bloat)
- ✅ Uses GitHub Models via OpenAI SDK only
- ✅ Token stored in `.env` (never hardcoded)
- ✅ `.env` should NOT be committed to git
- ✅ Use `.env.example` as template for new developers

---

## 🎓 Code Quality

- ✓ Type hints on all functions
- ✓ Comprehensive docstrings (Google style)
- ✓ Clear, beginner-friendly code
- ✓ Modular design with separation of concerns
- ✓ Proper error handling with meaningful messages

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'agent'"
**Solution**: Make sure your `.venv` is activated and run from project root
```bash
.\.venv\Scripts\Activate.ps1
cd d:\IIIT\AI-Study-Assistant
python src/main.py
```

### Issue: "ValueError: GITHUB_TOKEN environment variable must be set"
**Solution**: Create `.env` file with your GitHub PAT
```bash
cp .env.example .env
# Edit .env and add your GitHub token
```

### Issue: "No conversations to save yet"
**Solution**: Have at least one conversation before saving
```bash
You: Python Fundamentals
[Wait for response]
You: save
```

---

## 📚 API Reference

### StudyAgent
```python
from agent.config import load_config
from agent.study_agent import StudyAgent

config = load_config()
agent = StudyAgent(config)

# Single query
response = agent.run("What is Python?")

# Multi-turn (history maintained automatically)
response = agent.run("Follow-up question")

# Clear history
agent.clear_history()
```

### ConversationHistory
```python
from agent.agent_client import ConversationHistory

history = ConversationHistory(max_messages=10)
history.add_message("user", "Hello")
history.add_message("assistant", "Hi there!")

messages = history.get_messages()  # Returns list of messages
history.clear()  # Clear all messages
```

### Helpers
```python
from utils.helpers import format_response, save_session_transcript

# Format response for terminal
formatted = format_response(raw_response)
print(formatted)

# Save transcript
messages = agent._conversation_history.get_messages()
filepath = save_session_transcript(messages)
```

---

## 🚀 Future Enhancements

Potential features to add:
- [ ] Web UI with Gradio/Streamlit
- [ ] Database for persistent session storage
- [ ] Export to PDF/Markdown formats
- [ ] Multi-language support
- [ ] Custom system prompts per session
- [ ] Rate limiting & API usage tracking

---

## 📄 License

See LICENSE file for details.

---

## 💬 Support

If you encounter issues:
1. Check `.env` is properly configured
2. Verify virtual environment is activated
3. Run `pip install -r requirements.txt`
4. Check GitHub token has necessary permissions
5. Run tests: `pytest tests/test_agent.py -v`

Happy learning! 📚
