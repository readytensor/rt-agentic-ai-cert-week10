from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from pathlib import Path


# Load environment variables from root directory
root_dir = Path(__file__).parent.parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(env_path)

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant", temperature=0.7, api_key=os.getenv("GROQ_API_KEY")
)


def get_ai_response(user_message: str) -> str:
    """Generate AI response for user message

    Args:
        user_message (str): The user's input message

    Returns:
        str: The AI-generated response
    """
    messages = [
        SystemMessage(content="You are a helpful AI assistant."),
        HumanMessage(content=user_message),
    ]

    response = llm.invoke(messages)
    return response.content
