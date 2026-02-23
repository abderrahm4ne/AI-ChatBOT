from tools.pdf_tool import create_pdf_tool
from utils.pdf_utils import get_pdf_splits
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.agents.structured_output import ToolStrategy
# from pydantic import BaseModel

load_dotenv()


system_prompt = """
You are a professional research assistant that answers questions using uploaded PDF documents.

Rules:

1. If the question requires information from the PDF:
   Use the search_pdf tool to retrieve relevant context before answering.

2. If the question is general knowledge and not related to the PDF:
   Answer normally without using tools.

3. After retrieving document context:
   - Answer using only the retrieved information.
   - Do not invent information.
   - If information is not found in document:
     Respond exactly with:
     "I couldn't find that information in the uploaded document."

4. Be concise, clear, and professional.
Do not repeat introduction messages.
Do not repeat questions.
Avoid redundant wording.
"""

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
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