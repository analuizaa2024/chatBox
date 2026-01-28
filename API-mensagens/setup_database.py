import os
import sys
import shutil
import csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.app.config import get_embedding_function



DOC_DIR = "data"
DB_DIR = "db"
# if os.path.exists(DB_DIR):
# shutil.rmtree(DB_DIR)


# ---------------- CARREGAMENTO DOS DOCUMENTOS ----------------


data = []


for file_name in os.listdir(DOC_DIR):
    file_path = os.path.join(DOC_DIR, file_name)


    if file_name.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        data.extend(loader.load())


    elif file_name.endswith(".txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        data.extend(loader.load())


    elif file_name.endswith(".csv"):
        with open(file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
        for row in reader:
            text = row.get("Problema", "")
            metadata = {"URL": row.get("URL", "")}
            data.append(Document(page_content=text, metadata=metadata))


    else:
        print(f"Arquivo ignorado: {file_name}")


# ---------------- SPLIT EM CHUNKS (MUITO IMPORTANTE) ----------------


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100
)


docs = text_splitter.split_documents(data)


print(f"Total de documentos carregados: {len(data)}")
print(f"Total de chunks criados: {len(docs)}")


# ---------------- EMBEDDINGS ----------------


print(f"Criando embeddings com a função configurada...")
embedding_function = get_embedding_function()


# ---------------- BANCO VETORIAL ----------------


print("Armazenando no banco de dados vetorial...")
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_function,
    persist_directory=DB_DIR
)


print("Banco de dados vetorial criado com sucesso.")