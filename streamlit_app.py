"""Streamlit web interface for the AI Study Assistant."""

import streamlit as st
import sys
import os

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

# Page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="wide"
)

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
    st.markdown("---")
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

st.markdown("---")

# Chat input remains unchanged to preserve behavior
if prompt := st.chat_input("Type a topic or question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.run(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})