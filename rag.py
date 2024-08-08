from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings

from lyrics import LYRICS_LIB

RAG_TEMPLATE = r"""
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

<context>
{context}
</context>

Answer the following question:

{question}"""  # noqa


def init_llm():
    llm = ChatOllama(model="llama3.1:latest")
    return llm


def init_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text")


def main(q):
    llm = init_llm()

    lyrics = [f for f in LYRICS_LIB.iterdir() if f.is_file()]
    loaders = [TextLoader(lyric) for lyric in lyrics]

    documents = []
    for loader in loaders:
        docs: list[Document] = loader.load()
        documents.extend(docs)

    embedding = init_embeddings()
    vectorstore = Chroma.from_documents(documents=documents, embedding=embedding)

    # Retrieve and generate using the relevant song lyrics.
    retriever = vectorstore.as_retriever()
    prompt = ChatPromptTemplate.from_template(RAG_TEMPLATE)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    # LCEL implementation style.
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(q)


if __name__ == "__main__":
    q = "What is the chorus of Blindside by James Arthur?"
    ans = main(q)
    print(ans)
