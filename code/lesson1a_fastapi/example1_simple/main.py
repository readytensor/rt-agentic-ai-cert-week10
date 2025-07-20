from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from service import get_ai_response
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI Chatbot API",
    description="A simple AI chatbot powered by Groq and LangChain",
    version="1.0.0"
)

# Request model
class ChatRequest(BaseModel):
    message: str

# Response model  
class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat with the AI assistant"""
    try:
        ai_response = get_ai_response(request.message)
        return ChatResponse(response=ai_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "AI Chatbot API is running! Visit /docs for API documentation"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)