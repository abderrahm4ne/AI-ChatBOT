from tools.pdf_tool import create_pdf_tool
from utils.pdf_utils import get_pdf_splits
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_groq import ChatGroq

load_dotenv()

system_prompt = """
### ROLE
You are an expert Research Assistant. Your goal is to provide accurate information based on the documents provided to you,
answer questions using the information retrieved from the search_pdf tool. If the answer is not in the document, say: "I'm sorry, I couldn't find information about that in the uploaded document.

### TOOLS:
## You have access to this tool:
    - pdf_tool : Always use the 'search_pdf' tool when a user asks a question about the PDF content. Do not rely on your internal training data for facts that should be in the PDF.

### RESPONSE STRUCTURE
    - Direct Answer:** Start with a clear, direct answer to the user's question.
    - Context/Details:** Provide supporting details from the PDF.
    - Source Reference:** Mention that the information was found in the provided document.
"""


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.6
)

chunks = get_pdf_splits('./assets/input.pdf')
pdf_tool = create_pdf_tool(chunks)

agent = create_agent(
    model= llm,
    tools= [pdf_tool],
    system_prompt=system_prompt
)

response = agent.invoke(
    {"messages": [{"role": "user", "content": "How does hydroponic farming compare to traditional soil-based agriculture? send exactly what has been writing inside the pdf"}]},
)

print(response['messages'][-1].content)
