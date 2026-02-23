from tools.pdf_tool import create_pdf_tool
from utils.pdf_utils import get_pdf_splits
from dotenv import load_dotenv
from langchain.agents import create_agent
# from langchain_groq import ChatGroq
# from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
import os


load_dotenv()


system_prompt = """
You are a professional research assistant that answers questions using uploaded PDF documents.

Rules:
1. Only use the search_pdf tool when the user asks a clear, specific question about document content.
   Never use it for: greetings, single words, vague inputs, or general knowledge questions.

2. For greetings, conversational messages, or general questions: answer directly without any tools.

3. After using search_pdf:
   - Summarize the answer in 1-3 sentences using the retrieved context.
   - NEVER paste the raw retrieved text directly.
   - Answer only based on retrieved information.

4. Be concise and professional. Never repeat the user's question.
"""

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def create_my_agent(pdf_path: str):
    new_chunks = get_pdf_splits(pdf_path)
    new_pdf_tool = create_pdf_tool(new_chunks)

    return create_agent(
        model=llm,
        tools=[new_pdf_tool],
        system_prompt=system_prompt,
    )

current_agent = create_my_agent('./assets/input.pdf')