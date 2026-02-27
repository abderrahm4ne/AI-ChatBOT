from tools.pdf_tool import create_pdf_tool
from utils.pdf_utils import get_pdf_splits
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
# from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import threading

load_dotenv()
system_prompt = """
You are a professional research assistant that answers questions using uploaded PDF documents.

Think step by step before answering and take your time:
1. Is this a document-related question? If yes, call search_pdf first.
2. Read the retrieved context carefully.
3. Then write a clean 1-2 sentence answer.

Rules:
- NEVER answer without using search_pdf for document questions.
- NEVER say "I couldn't find" without actually calling search_pdf first.
- NEVER paste raw retrieved text.
- If truly not found after searching, say: "I couldn't find that information in the uploaded document."

Be concise and professional.
"""

"""

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1,
)
"""
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1
)

agents = {}


def create_my_agent(pdf_path: str):
    new_chunks = get_pdf_splits(pdf_path)
    new_pdf_tool = create_pdf_tool(new_chunks)

    return create_agent(
        model=llm,
        tools=[new_pdf_tool],
        system_prompt=system_prompt,
    )

current_agent = create_my_agent('./assets/input.pdf')