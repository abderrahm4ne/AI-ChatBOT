from tools.pdf_tool import create_pdf_tool
from utils.pdf_utils import get_pdf_splits
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.agents.structured_output import ToolStrategy
# from pydantic import BaseModel

load_dotenv()


system_prompt = """
You are a research assistant helping answer questions about uploaded PDF documents.

Follow these rules:

1. You must use the search_pdf tool if:
   - The user asks about document content
   - The answer is likely inside the PDF so use the tool and get the infos

2. If user asks general questions, answer normally.

3. If you cannot find information in document:
   Say:
   "I couldn't find that information in the uploaded document."

"""

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.1
)

chunks = get_pdf_splits('./assets/input.pdf')
pdf_tool = create_pdf_tool(chunks)

def create_my_agent(pdf_path: str):
    new_chunks = get_pdf_splits(pdf_path)
    new_pdf_tool = create_pdf_tool(new_chunks)

    return create_agent(
        model=llm,
        tools=[new_pdf_tool],
        system_prompt=system_prompt,
    )

current_agent = create_my_agent('./assets/input.pdf')
