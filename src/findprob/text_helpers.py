from bs4 import BeautifulSoup

from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import RecursiveUrlLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

import re


def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()

def get_document_loader_from_url(url: str) -> RecursiveUrlLoader:
    return RecursiveUrlLoader(
        url,
        max_depth=2,
        extractor=bs4_extractor
    )

def get_document_loader_from_pdf(file_path: str) -> PyPDFLoader:
    return PyPDFLoader(file_path)

def chunk_documents(loader: RecursiveUrlLoader | PyPDFLoader, chunk_size: int, chunk_overlap: int):
    return loader.load_and_split(
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            separators=["\n\n", "\n", " "], # separate by paragraph, sentence, then word
            chunk_overlap=chunk_overlap
        )
    )

def save_vectorstore(chunks: list, out_dir: str):
    embeddings = OpenAIEmbeddings() # default model='text-embedding-ada-002'
    store = FAISS.from_documents(chunks, embeddings)
    store.save_local(out_dir)
