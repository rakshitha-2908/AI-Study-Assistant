"""Streamlit web interface for the AI Study Assistant."""

import streamlit as st
import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.study_agent import StudyAgent
from agent.config import load_config

PROMPT_SUGGESTIONS = [
    "What is a stack? Explain with examples",
    "Create a 30-day DSA roadmap for beginners",
    "Teach me recursion from scratch",
    "Give me 5 binary search interview questions",
    "What's the difference between BFS and DFS?",
    "Explain dynamic programming with an example",
]


def build_export_markdown(messages: list) -> str:
    """Convert chat history into a downloadable markdown string."""
    if not messages:
        return "# Study Session\n\nNo messages yet."
    
    lines = ["# AI Study Assistant — Session Notes\n"]
    for msg in messages:
        role_label = "You" if msg["role"] == "user" else "Assistant"
        lines.append(f"## {role_label}\n")
        lines.append(f"{msg['content']}\n")
    return "\n".join(lines)

# Page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

# WHERE YOU INSERTED THIS: custom CSS for improved chat readability
st.markdown("""
<style>
    .stChatMessage {
        padding: 0.5rem 0;
    }
    .stChatMessage p {
        line-height: 1.6;
    }
    .stChatMessage code {
        font-size: 0.85em;
    }
    div[data-testid="stChatMessageContent"] table {
        font-size: 0.9em;
    }
    .stMarkdown h3, .stMarkdown h4 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar: professional app info and controls
with st.sidebar:
    st.header("📚 AI Study Assistant")
    st.markdown(
        """
        Create study plans, learn concepts,
        and prepare for interviews using AI.

        **Model:** GPT-4o Mini
        """
    )
    st.markdown("---")
    st.subheader("Try Asking")
    st.markdown(
        """
        - Create a 30-day DSA roadmap
        - Explain Binary Search
        - Teach me DBMS
        - Create a Python learning plan
        """
    )
    TOPIC_CONTEXT = {
        "General CS": "",
        "Data Structures & Algorithms": "The student is studying DSA. Always mention time complexity and space complexity. Prioritize interview patterns like sliding window, two pointers, recursion trees.",
        "Operating Systems": "The student is studying OS. Focus on process management, memory management, CPU scheduling, deadlocks, and synchronization.",
        "Database Systems": "The student is studying DBMS. Focus on normalization, SQL queries, indexing, transactions, ACID properties.",
        "System Design": "The student is preparing for system design interviews. Focus on scalability, load balancing, caching, databases, and trade-offs.",
        "Computer Networks": "The student is studying CN. Focus on OSI model, TCP/IP, HTTP, DNS, sockets, and protocols.",
        "OOP & Design Patterns": "The student is studying OOP. Focus on SOLID principles, common design patterns with real examples.",
    }

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Study Settings")

    selected_topic = st.sidebar.selectbox(
        "Subject",
        options=list(TOPIC_CONTEXT.keys()),
        index=0,
        key="selected_topic"
    )

    selected_difficulty = st.sidebar.select_slider(
        "Depth level",
        options=["Beginner", "Intermediate", "Interview-ready"],
        value="Intermediate",
        key="selected_difficulty"
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown("### Topics Covered")
    if "topics_covered" not in st.session_state:
        st.session_state.topics_covered = []

    if st.session_state.topics_covered:
        for topic in st.session_state.topics_covered[-6:]:
            st.sidebar.markdown(f"• {topic}")
    else:
        st.sidebar.caption("Topics you study will appear here.")

    # WHERE YOU INSERTED THIS: Export chat as markdown download button (appears before Clear Chat)
    if st.session_state.get("messages"):
        export_data = build_export_markdown(st.session_state.messages)
        st.sidebar.download_button(
            label="📥 Export Notes",
            data=export_data,
            file_name="study_session_notes.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quiz Mode")

    if "quiz_active" not in st.session_state:
        st.session_state.quiz_active = False
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = ""
    if "quiz_score_history" not in st.session_state:
        st.session_state.quiz_score_history = []
    if "quiz_topic" not in st.session_state:
        st.session_state.quiz_topic = ""

    quiz_topic_input = st.sidebar.text_input("Quiz topic", placeholder="e.g. Binary Search Trees")

    if st.sidebar.button("Generate Quiz", use_container_width=True):
        if quiz_topic_input.strip():
            st.session_state.quiz_active = True
            st.session_state.quiz_topic = quiz_topic_input
            st.session_state.quiz_questions = ""
            st.rerun()
        else:
            st.sidebar.warning("Enter a topic first")

    if st.session_state.quiz_score_history:
        st.sidebar.markdown("#### Past Scores")
        for entry in st.session_state.quiz_score_history[-5:]:
            st.sidebar.caption(entry)

    # persist selections to session state
    st.session_state.topic = selected_topic
    st.session_state.difficulty = selected_difficulty

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        if "agent" in st.session_state:
            st.session_state.agent.clear_history()
        st.rerun()
    st.caption("Clear the conversation and start fresh.")

# Main layout header and intro
st.title("📚 AI Study Assistant 🚀")
st.markdown("Ask me to create a study plan for any topic, or ask any learning question!")
st.markdown("---")

# Initialize agent in session state
if "agent" not in st.session_state:
    config = load_config()
    st.session_state.agent = StudyAgent(config)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Prompt suggestions when chat history is empty
if not st.session_state.messages:
    st.markdown("#### What would you like to study today?")
    cols = st.columns(2)
    for i, suggestion in enumerate(PROMPT_SUGGESTIONS):
        col = cols[i % 2]
        if col.button(suggestion, key=f"suggestion_{i}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            st.rerun()

# Display chat history with improved spacing and hierarchy
chat_container = st.container()
with chat_container:
    if st.session_state.messages:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    else:
        st.info("Start the conversation by sending a topic or question in the chat input below.")

# Quiz UI: inserted after chat messages loop and before chat input
if st.session_state.get("quiz_active", False):
    st.markdown("---")
    st.markdown(f"### Quiz: {st.session_state.get('quiz_topic', '')}")

    if not st.session_state.quiz_questions:
        with st.spinner("Generating quiz..."):
            agent = st.session_state.agent
            questions = agent.generate_quiz(
                topic=st.session_state.get("quiz_topic", ""),
                difficulty=st.session_state.get("difficulty", "Intermediate")
            )
            st.session_state.quiz_questions = questions

    st.markdown(st.session_state.quiz_questions)

    user_quiz_answers = st.text_area(
        "Your answers (number them to match the questions)",
        height=200,
        key="quiz_answer_input"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answers", use_container_width=True):
            if user_quiz_answers.strip():
                with st.spinner("Evaluating..."):
                    agent = st.session_state.agent
                    feedback = agent.evaluate_quiz_answers(
                        topic=st.session_state.get("quiz_topic", ""),
                        questions=st.session_state.quiz_questions,
                        user_answers=user_quiz_answers
                    )
                    st.markdown("#### Results")
                    st.markdown(feedback)

                    score_match = re.search(r"Score:\s*(\d+)/(\d+)", feedback)
                    if score_match:
                        score_text = f"{st.session_state.get('quiz_topic', '')}: Score: {score_match.group(1)}/{score_match.group(2)}"
                        st.session_state.quiz_score_history.append(score_text)
            else:
                st.warning("Please enter your answers first")
    with col2:
        if st.button("Exit Quiz", use_container_width=True):
            st.session_state.quiz_active = False
            st.session_state.quiz_questions = ""
            st.rerun()

st.markdown("---")

# Chat input remains unchanged to preserve behavior
if prompt := st.chat_input("Type a topic or question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # WHERE YOU INSERTED THIS: track topics covered in session
    if prompt and len(prompt) > 3:
        topic_label = prompt[:40] + "..." if len(prompt) > 40 else prompt
        if "topics_covered" not in st.session_state:
            st.session_state.topics_covered = []
        if topic_label not in st.session_state.topics_covered:
            st.session_state.topics_covered.append(topic_label)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.run(
                prompt,
                topic_context=TOPIC_CONTEXT.get(st.session_state.get("topic", "General CS"), ""),
                difficulty=st.session_state.get("difficulty", "Intermediate"),
            )
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})