from langchain_huggingface import HuggingFaceEmbeddings

# Load once — reuse everywhere
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
