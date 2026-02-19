from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_pdf_splits(input):
    all_chunks = []
    reader = PdfReader(input)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", " ", ""]
    )

    for page in reader.pages:
        fullText = page.extract_text() + "\n"
        if fullText:
            page_chunks = text_splitter.split_text(fullText)
            all_chunks.extend(page_chunks)

    return all_chunks