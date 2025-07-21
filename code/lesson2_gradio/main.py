"""
AI Chatbot with Gradio - Lesson 2
Build and Share AI Demos Instantly with Gradio 🚀

A self-contained chatbot app using LangChain + Gradio.
Perfect for demos, job interviews, and portfolio projects.
"""

import gradio as gr
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize the LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.7,
    api_key=os.getenv("GROQ_API_KEY")
)

def get_ai_response(user_message: str) -> str:
    """Generate AI response for user message"""
    messages = [
        SystemMessage(
            content="You are a helpful AI assistant. Answer the user's questions."
        ),
        HumanMessage(content=user_message),
    ]
    response = llm.invoke(messages)
    return response.content

def chatbot_interface(message, history):
    """Handle chatbot conversation flow"""
    if not message.strip():
        return history, ""
    
    bot_response = get_ai_response(message)
    
    # Add to history using the new messages format
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": bot_response})
    
    return history, ""

def create_interface():
    """Create and configure the Gradio interface"""
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        # Header
        gr.Markdown("# 🤖 AI Chatbot Assistant")
        gr.Markdown("Ask me anything and I'll help you with intelligent responses!")

        # Chat components
        chatbot = gr.Chatbot(
            value=[], 
            height=400, 
            label="Chat History",
            show_copy_button=True,
            type="messages"  # Use new messages format
        )
        
        msg = gr.Textbox(
            placeholder="Type your message here...", 
            label="Your Message",
            lines=2
        )

        # Buttons
        with gr.Row():
            submit_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear Chat", variant="secondary")

        # Event handlers
        submit_btn.click(
            chatbot_interface, 
            inputs=[msg, chatbot], 
            outputs=[chatbot, msg]
        )
        
        msg.submit(
            chatbot_interface, 
            inputs=[msg, chatbot], 
            outputs=[chatbot, msg]
        )
        
        clear_btn.click(
            lambda: ([], ""), 
            inputs=[], 
            outputs=[chatbot, msg]
        )

        # Footer
        gr.Markdown("---")
        gr.Markdown("💡 Built with Gradio + LangChain + Groq")

    return demo

if __name__ == "__main__":
    # Create and launch the interface
    demo = create_interface()
    demo.launch(
        share=True,           # Creates public shareable link
        server_name="127.0.0.1",  # Use localhost instead of 0.0.0.0
        server_port=7860,
        show_error=True       # Show detailed errors for debugging
    )