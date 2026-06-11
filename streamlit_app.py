"""Streamlit web interface for the AI Study Assistant."""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agent.study_agent import StudyAgent
from agent.config import load_config

# Page config
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

# Title and description
st.title("📚 AI Study Assistant 🚀")
st.markdown("Ask me to create a study plan for any topic, or ask any learning question!")

# Initialize agent in session state
if "agent" not in st.session_state:
    config = load_config()
    st.session_state.agent = StudyAgent(config)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type a topic or question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.agent.run(prompt)
            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})