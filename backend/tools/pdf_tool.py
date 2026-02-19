from langchain_core.vectorstores import InMemoryVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.tools import tool


def create_pdf_tool(fullSplits):
    embiddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")
    vectoreStore = InMemoryVectorStore.from_texts(
        fullSplits, embedding=embiddings
    )
    retriever = vectoreStore.as_retriever()

    @tool
    def search_pdf(query: str) -> str:
        """Search the uploaded PDF for infos"""
        docs = retriever.invoke(query)
        return "\n\n".join([doc.page_content for doc in docs])
    
    return search_pdf