import os
import json

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is not set in the .env file")


# Initialize the Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    groq_api_key=GROQ_API_KEY
)


def analyze_clause(
    clause_name: str,
    clause_text: str,
    retrieved_context: str = ""
) -> dict:
    """
    Analyze one legal contract clause using the Groq LLM.

    retrieved_context is optional for now.
    Later, it will contain relevant legal knowledge retrieved
    from the project's RAG/vector database.
    """

    # If RAG context is available, include it in the prompt.
    if retrieved_context and retrieved_context.strip():
        knowledge_section = f"""
Relevant legal knowledge retrieved from the project's knowledge base:

{retrieved_context}
"""
    else:
        knowledge_section = """
No additional knowledge-base context is available yet.
Analyze the clause based on the clause text itself.
"""

    prompt = f"""
You are a legal contract analysis assistant.

Analyze the following contract clause.

Clause name:
{clause_name}

Clause text:
{clause_text}

{knowledge_section}

Use the retrieved legal knowledge when it is provided.
Do not invent facts that are not supported by the clause or
the retrieved knowledge.

Return ONLY valid JSON with these fields:

{{
    "clause_name": "...",
    "summary": "...",
    "risk_level": "Low | Medium | High",
    "risk_reason": "...",
    "recommendation": "..."
}}
"""

    # Send the clause and available knowledge to the LLM
    response = llm.invoke(prompt)

    # Get the model response
    content = response.content.strip()

    # Remove Markdown code fences if the model returns JSON inside them
    if content.startswith("```"):
        content = content.replace("```json", "", 1)
        content = content.replace("```", "", 1)
        content = content.strip()

    # Convert the response from JSON text into a Python dictionary
    try:
        return json.loads(content)

    # Fallback if the model does not return valid JSON
    except json.JSONDecodeError:
        return {
            "clause_name": clause_name,
            "summary": content,
            "risk_level": "Unknown",
            "risk_reason": "",
            "recommendation": ""
        }