# 📚 AI Study Assistant

An AI-powered learning companion that generates personalized study plans and answers educational questions using GPT-4o Mini.

## 🚀 Live Demo

https://ai-study-assistant-lxzhwtkobdc7fsbzh5r7v9.streamlit.app

---

## ✨ Features

* 📖 Generate structured study plans for any topic
* 🎯 Personalized learning objectives and exercises
* 💬 Ask follow-up questions with conversation memory
* 🧠 AI-powered explanations for technical and academic concepts
* 🌐 Interactive Streamlit web interface
* ☁️ Cloud deployment using Streamlit Community Cloud

---

## 🛠️ Tech Stack

* Python
* Streamlit
* OpenAI SDK
* GitHub Models
* GPT-4o Mini

---

## 📂 Project Structure

```text
AI-Study-Assistant/
│
├── src/
│   ├── agent/
│   │   ├── study_agent.py
│   │   ├── agent_client.py
│   │   └── config.py
│   │
│   └── utils/
│       └── helpers.py
│
├── tests/
├── docs/
├── transcripts/
│
├── streamlit_app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 💡 Example Prompts

### Study Plan Generation

```text
Create a 30-day DSA study plan for interview preparation
```

### Educational Question

```text
What is binary search?
```

### Follow-Up Question

```text
Can you give an example?
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/rakshitha-2908/AI-Study-Assistant.git
cd AI-Study-Assistant
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

Create a `.env` file:

```env
GITHUB_TOKEN=your_github_models_token
```

### Run the Application

```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deployment

This application is deployed on Streamlit Community Cloud and automatically redeploys whenever changes are pushed to GitHub.

---

## 🔮 Future Improvements

* Sidebar controls
* Clear chat functionality
* Download study plans
* Difficulty-level customization
* Progress tracking dashboard
* Multiple AI model support

---

## 📄 License

This project is licensed under the MIT License.
