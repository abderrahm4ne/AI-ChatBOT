from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

def clean_text(text:str):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s([?.!,])', r'\1', text)

    return text.strip()


def get_pdf_splits(input):
    all_chunks = []
    reader = PdfReader(input)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size= 300,
        chunk_overlap=50,
        length_function=len,
        is_separator_regex=False,
        separators=["\n\n", "\n", ".", " " ,""]
    )

    for page in reader.pages:
        fullText = page.extract_text() + "\n"
        #print('page content : ', fullText)
        if fullText:
            cleanedText = clean_text(fullText)
            page_chunks = text_splitter.split_text(cleanedText)
            all_chunks.extend(page_chunks)

    return all_chunks