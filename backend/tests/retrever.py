import os

import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas import evaluate
from ragas.metrics import (
    context_precision,
    context_recall,
)
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.embeddings.huggingface import HuggingFaceInferenceAPIEmbeddings
from datasets import Dataset
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.chat_models.ollama import ChatOllama

load_dotenv("../.env")

test_embeddings = HuggingFaceInferenceAPIEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    api_key=os.getenv("HF_TOKEN"),
)

DATA_PATH = "../data/raw_data"
FAISS_INDEX_PATH = "../vectorstores/faiss"
TESTSET = "../data/test_data/retrieval_qna.csv"

# Load or create the FAISS index.
if os.path.exists(FAISS_INDEX_PATH):
    # Index file exists, load it
    print("Loading existing FAISS index from:", FAISS_INDEX_PATH)
    vector_db = FAISS.load_local(
        FAISS_INDEX_PATH, test_embeddings, allow_dangerous_deserialization=True
    )
    print("Loaded FAISS index.")
else:
    # Index file doesn't exist, create a new one
    # Define the document loader.
    documentLoader = DirectoryLoader(
        path=DATA_PATH,
        glob="**/*.pdf",
        use_multithreading=True,
        show_progress=True,
        loader_cls=UnstructuredPDFLoader,
        # loader_kwargs={"infer_table_structure": True, "strategy": "hi_res"},
    )
    # Load the documents.
    loaded_documents = documentLoader.load()

    # Split the documents.
    splitted_documents = RecursiveCharacterTextSplitter().split_documents(
        loaded_documents
    )

    # Create the FAISS index.
    print("Creating new FAISS index and saving to:", FAISS_INDEX_PATH)
    vector_db = FAISS.from_documents(splitted_documents, test_embeddings)
    vector_db.save_local(FAISS_INDEX_PATH)
    print("Created and saved FAISS index.")

langchain_llm = ChatOllama(model="llama3")
langchain_embeddings = OllamaEmbeddings(model="llama3")
retriever = vector_db.as_retriever()

# retriever = MultiQueryRetriever.from_llm(
#     retriever=vector_db.as_retriever(), llm=langchain_llm
# )

retriever.invoke("What is the capital of Germany?")

# load test set csv
df = pd.read_csv(TESTSET)


eval_questions = df["question"].tolist()
eval_answers = df["answer"].tolist()


data = {
    "question": [],
    # "answer": [],
    "contexts": [],
    "ground_truth": eval_answers,
}

for q in eval_questions:
    data["question"].append(q)
    data["contexts"].append([doc.page_content for doc in retriever.invoke(q)])

dataset = Dataset.from_dict(data)

results = evaluate(
    dataset,
    [context_precision, context_recall],
    is_async=False,
    llm=langchain_llm,
    embeddings=langchain_embeddings,
)

results
