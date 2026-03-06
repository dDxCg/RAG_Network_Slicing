from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma

embed_model="BAAI/bge-small-en-v1.5"

embed = HuggingFaceEmbeddings(
    model_name = embed_model
)

import json
docs = []
with open("sample_kb.jsonl", "r") as f:
    for line in f:
        obj = json.loads(line)
        text = f"<ENV> {obj['slice']}. {obj['ue_pattern']}. {obj['ue_number']}\n<ANALYZE> {obj['analyze']}\n<ACTION> {obj['action']}\n<REWARD> {obj['reward']}"
        docs.append(
            Document(
                page_content=text,
                metadata={
                    "source": "sample_kb.jsonl",
                    "numeric_data": obj["numeric_data"]   
                }
            )
        )

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embed,
    persist_directory="./chroma_db"
)

