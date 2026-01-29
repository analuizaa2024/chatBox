from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser


class RAGModel:
    def __init__(self, db_path, embedding_function, max_chunks=3, max_context_chars=2000):
        # Banco vetorial
        self.vectorstore = Chroma(
            persist_directory=db_path,
            embedding_function=embedding_function
        )

        # Modelo de linguagem (Ollama)
        self.llm = ChatOllama(
            model="qwen2:1.5b",
            temperature=0.1,
            num_ctx=1024
        )

        self.max_context_chars = max_context_chars
        self.max_chunks = max_chunks

    def get_rag_response(self, question):
        # 1 Busca com score
        docs_with_scores = self.vectorstore.similarity_search_with_score(
            question,
            k=self.max_chunks
        )

        # 2 Não descartar documentos relevantes
        # (quanto menor o score, mais relevante)
        docs_filtrados = [doc for doc, score in docs_with_scores]

        if not docs_filtrados:
            return "Essa informação não está nos documentos."

        # 3 Monta contexto com limite de caracteres
        context_parts = []
        total_chars = 0

        for doc in docs_filtrados:
            if total_chars + len(doc.page_content) > self.max_context_chars:
                break
            context_parts.append(doc.page_content)
            total_chars += len(doc.page_content)

        context = "\n\n".join(context_parts)

        if not context.strip():
            return "Essa informação não está nos documentos."

        # 4 Prompt
        template = """
Você é um professor de língua portuguesa.
Use EXCLUSIVAMENTE as informações presentes no TEXTO.
Não use conhecimento externo.
Não complete lacunas.
Não faça suposições.

Se a resposta NÃO estiver claramente no texto, responda exatamente:
"Essa informação não está nos documentos."

TEXTO:
{context}

PERGUNTA:
{question}

RESPOSTA:
"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | self.llm | StrOutputParser()

        return chain.invoke({
            "context": context,
            "question": question
        })