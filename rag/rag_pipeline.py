from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import os

TEXTS_DIR = os.path.join(os.path.dirname(__file__), "texts")
CHROMA_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

def load_texts():
    docs = []
    for filename in os.listdir(TEXTS_DIR):
        if filename.endswith(".txt"):
            with open(os.path.join(TEXTS_DIR, filename), "r", encoding="utf-8") as f:
                text = f.read()
                docs.append(Document(page_content=text, metadata={"source": filename}))
    return docs

def build_vectorstore():
    docs = load_texts()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_DIR)
    print(f"Built vectorstore with {len(chunks)} chunks")
    return vectorstore

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    if os.path.exists(CHROMA_DIR):
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
    return build_vectorstore()

def retrieve_principles(query: str, k: int = 3) -> list:
    vectorstore = get_vectorstore()
    results = vectorstore.similarity_search(query, k=k)
    return [r.page_content for r in results]