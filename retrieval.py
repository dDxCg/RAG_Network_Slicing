from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# rerank_model="BAAI/bge-reranker-base"
# reranker = HuggingFaceCrossEncoder(
#     model_name = rerank_model
# )

# embed_model="BAAI/bge-small-en-v1.5"
# embed = HuggingFaceEmbeddings(
#     model_name = embed_model
# )

# vectorstore = Chroma(
#     persist_directory="./chroma_db",
#     embedding_function=embed
# )


#query sampling
import random
def sample_prob(n):
    vals = [random.random() for _ in range(n)]
    s = sum(vals)

    return [v/s for v in vals]

sample_slice_prob = sample_prob(3)
sample_pattern_prob = sample_prob(3)
sample_arrival = random.randrange(-5, 5, 1)
numeric_data = [*sample_slice_prob, *sample_pattern_prob, sample_arrival]

# sample_query = f"Probability of user using embb, urllc and mmtc is: {sample_slice_prob[0]}, {sample_slice_prob[1]}, {sample_slice_prob[2]}. Probability of user walking, using vehicle and stationary is: {sample_pattern_prob[0]}, {sample_pattern_prob[1]}, {sample_pattern_prob[2]}. The rate of the change in number of users is: {sample_arrival}. Suggest reward weights for QoS, Energy, Fairness."

# #similarity search
# docs = vectorstore.max_marginal_relevance_search(
#     sample_query,
#     k=10,       
#     fetch_k=30,  
#     lambda_mult=0.7
# )

# pairs = [(sample_query, doc.page_content) for doc in docs]
# scores = reranker.score(pairs)
# reranked = sorted(
#     zip(docs, scores),
#     key=lambda x: x[1],
#     reverse=True
# )
# top_docs = [doc for doc, score in reranked[:3]]

# for rank, (doc, score) in enumerate(reranked[:3], 1):
#     print(f"Rank {rank} | score={score:.4f}")
#     print(doc.page_content)


#sql lite:
import sqlite3

conn = sqlite3.connect("experiment_memory.db")
cursor = conn.cursor()
