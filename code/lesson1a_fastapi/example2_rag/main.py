from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from rag_service import answer_research_question
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Research Assistant API",
    description="AI-powered research assistant using RAG technology",
    version="1.0.0",
)


# Request model
class ResearchRequest(BaseModel):
    question: str


# Response models
class Source(BaseModel):
    title: str
    content: str
    score: float


class ResearchResponse(BaseModel):
    answer: str
    sources: List[Source]


@app.post("/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    """Ask a research question and get an AI-powered answer with sources"""
    try:
        answer, sources = answer_research_question(request.question)

        formatted_sources = [
            Source(
                title=source["title"],
                content=(
                    source["content"][:200] + "..."
                    if len(source["content"]) > 200
                    else source["content"]
                ),
                score=source["score"],
            )
            for source in sources
        ]

        return ResearchResponse(answer=answer, sources=formatted_sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {
        "message": "Research Assistant API is running! Visit /docs for API documentation"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
