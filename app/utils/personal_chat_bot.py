from langchain_qdrant import QdrantVectorStore
from qdrant_client.models import VectorParams, Distance
from langchain.text_splitter import CharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from app.config import settings
from app.services.embedding import embeddings
from app.services.qdrant_client import qdrant_client
import os
import time

def update_qdrant_with_txt_file(
    file_path: str,
    collection_name: str
):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    splitter = CharacterTextSplitter(separator="\n", chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(content)
    metadatas = [{"source": os.path.basename(file_path)} for _ in chunks]

    qdrant_client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # BGE-small = 384 dims
    )

    vectorstore = QdrantVectorStore(
        client=qdrant_client,
        collection_name=collection_name,
        embedding=embeddings
    )

    vectorstore.add_texts(texts=chunks, metadatas=metadatas)
    print(f"✅ Stored {len(chunks)} chunks into '{collection_name}'")

def ask_question_from_vectorstore(
    vectorstore,
    question: str,
    system_prompt: str,
    chat_history: list[str] = None
):
    llm = ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama3-70b-8192",
        temperature=0.3,
    )

    # Format history into readable string
    history_text = ""
    if chat_history:
        history_text = "\n".join(chat_history)

    # print('history_text', history_text)

    full_prompt = f"""{system_prompt}

Chat History:
{history_text}

Context:
{{context}}

Question:
{{input}}
"""

    prompt = ChatPromptTemplate.from_template(full_prompt)

    qa_chain = create_stuff_documents_chain(llm=llm, prompt=prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=qa_chain
    )
    # instead of create_retrieval_chain use -> as_query_engine
    llm_start = time.time()
    result = retrieval_chain.invoke({"input": question})
    llm_end = time.time()
    print("Groq LLM response time:", llm_end - llm_start)
    return result["answer"] if isinstance(result, dict) and "answer" in result else result

def get_vectorstore(collection_name: str) -> QdrantVectorStore:
    return QdrantVectorStore(
        client=qdrant_client,
        collection_name=collection_name,
        embedding=embeddings
    )
