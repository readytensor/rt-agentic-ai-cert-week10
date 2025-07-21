from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from pathlib import Path

from database import embeddings, collection

# Load environment variables from parent directory
root_dir = Path(__file__).parent.parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(env_path)

# Initialize components
llm = ChatGroq(
    model="llama-3.1-8b-instant", temperature=0.7, api_key=os.getenv("GROQ_API_KEY")
)


def search_research_db(query: str, top_k: int = 3):
    """Search the research database for relevant chunks"""
    print(f"Searching for query: {query}")
    query_embedding = embeddings.embed_query(query)

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)

    chunks = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            chunks.append(
                {
                    "content": doc,
                    "title": (
                        results["metadatas"][0][i].get("title", "Unknown")
                        if results["metadatas"][0]
                        else "Unknown"
                    ),
                    "score": (
                        results["distances"][0][i] if results["distances"][0] else 0.0
                    ),
                }
            )
    print(f"Found {len(chunks)} relevant chunks")

    return chunks


def answer_research_question(query: str):
    """Generate an answer based on retrieved research

    Args:
        query (str): The research question

    Returns:
        tuple: (answer_string, list_of_source_chunks)
    """
    # Get relevant research chunks
    relevant_chunks = search_research_db(query, top_k=3)

    if not relevant_chunks:
        return (
            "I don't have enough information in my knowledge base to answer this question. " +
            "Please try adding some documents first.",
            [],
        )

    # Build context from research
    context = "\n\n".join(
        [f"From {chunk['title']}:\n{chunk['content']}" for chunk in relevant_chunks]
    )

    # Create research-focused prompt
    prompt_template = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Based on the following context document(s), answer the researcher's question:

Research Context:
{context}

Researcher's Question: {question}

Answer: Provide a answer based on the context above. 
If the context doesn't contain enough information to fully answer the question, say so clearly.
Only answer based on the provided context, do not make assumptions or provide additional information.
If the question is not related to the context, respond with "I don't have enough information in my 
knowledge base to answer this question. Please try adding some documents first.".
Answer clearly and concisely, without unnecessary details.
""",
    )

    # Generate answer
    prompt = prompt_template.format(context=context, question=query)
    response = llm.invoke(prompt)

    return response.content, relevant_chunks


if __name__ == "__main__":
    # Example usage
    question1 = "What is best method to handle class imbalance?"
    answer, sources = answer_research_question(question1)
    print("Answer:", answer)
    # print("Sources:", sources)
    print("\n---\n")


    question2 = "What are key components in a VAE architecture?"
    answer, sources = answer_research_question(question2)
    print("Answer:", answer)
    # print("Sources:", sources)
    print("\n---\n")


    question3 = "What is time step classification?"
    answer, sources = answer_research_question(question3)
    print("Answer:", answer)
    # print("Sources:", sources)
    print("\n---\n")


    question4 = "What are various methods of calculating distances in distance profiles?"
    answer, sources = answer_research_question(question4)
    print("Answer:", answer)
    # print("Sources:", sources)
    print("\n---\n")


    question5 = "What is the CLIP tutorial about?"
    answer, sources = answer_research_question(question5)
    print("Answer:", answer)
    # print("Sources:", sources)
    print("\n---\n")