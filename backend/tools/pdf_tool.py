from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool


def create_pdf_tool(fullSplits):
    embiddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    vectoreStore = FAISS.from_texts(
        fullSplits,
        embedding=embiddings
    )
    retriever = vectoreStore.as_retriever(search_kwargs={"k": 5})

    @tool
    def search_pdf(query: str) -> str:
        """Search the uploaded PDF document for a specific answer.
        Returns only the most relevant passage, not the full document."""
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
    
    return search_pdf