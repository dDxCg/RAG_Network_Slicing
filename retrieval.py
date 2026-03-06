from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

rerank_model="BAAI/bge-reranker-base"
reranker = HuggingFaceCrossEncoder(
    model_name = rerank_model
)

embed_model="BAAI/bge-small-en-v1.5"
embed = HuggingFaceEmbeddings(
    model_name = embed_model
)

vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embed
)
