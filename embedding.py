from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

embed_model="BAAI/bge-small-en-v1.5"

embed = HuggingFaceEmbeddings(
    model_name = embed_model
)

import json
texts = []
with open("sample_kb.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)
        text = f"<ENV> {obj['slice']}. {obj['ue_pattern']}. {obj['ue_number']}\n<ANALYZE> {obj['analyze']}\n<ACTION> {obj['action']}\n<REWARD> {obj['reward']}"
        texts.append(text)

docs = [
    Document(
        page_content=t,
        metadata={"source": "sample_kb.jsonl"}
    )
    for t in texts
]

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embed,
    persist_directory="./chroma_db"
)

