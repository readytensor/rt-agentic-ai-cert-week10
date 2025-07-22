"""
Streamlit AI Chatbot App
Built with LangChain + Groq + Streamlit

This app demonstrates how to build a professional AI chatbot interface
using Streamlit's powerful UI components and session state management.
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

# Load environment variables from .env in current directory
load_dotenv()

    
# Initialize the LLM with caching for performance
@st.cache_resource
def load_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found in environment variables!")
        st.error("Please make sure you have a .env file with your Groq API key.")
        st.stop()
    return ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")
    )

def get_ai_response(user_message: str, llm) -> str:
    messages = [
        SystemMessage(content="You are a helpful AI assistant. Answer the user's questions clearly and concisely."),
        HumanMessage(content=user_message),
    ]
    response = llm.invoke(messages)
    return response.content

def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Chatbot Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Main title and description
    st.title("🤖 AI Chatbot Assistant")
    st.markdown("Ask me anything and I'll help you with intelligent responses!")

    # Load the LLM
    llm = load_llm()

    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What would you like to know?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_ai_response(prompt, llm)
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

    # Sidebar for additional features
    with st.sidebar:
        st.markdown("### About This App")
        st.markdown("This AI chatbot is powered by:")
        st.markdown("- **Groq** for fast LLM inference")
        st.markdown("- **LangChain** for AI orchestration")
        st.markdown("- **Streamlit** for the beautiful UI")

        st.markdown("---")
        st.markdown("### Chat Controls")

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.markdown("---")
        st.markdown("### Stats")
        st.metric("Messages in Chat", len(st.session_state.messages))

        if st.session_state.messages:
            user_messages = len([msg for msg in st.session_state.messages if msg["role"] == "user"])
            st.metric("Questions Asked", user_messages)

if __name__ == "__main__":
    main()