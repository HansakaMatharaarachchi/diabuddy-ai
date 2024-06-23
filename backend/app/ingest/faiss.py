from app.constants import KNOWLEDGE_BASE_PATH, RAW_DATA_PATH
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_or_create_index():
    """Load or create a FAISS index.

    Returns:
        FAISS: The FAISS index.
    """
    # Embeddings used for the index.
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    if KNOWLEDGE_BASE_PATH.exists():
        # Index file already exists, load it.
        vector_db = FAISS.load_local(
            KNOWLEDGE_BASE_PATH, embeddings, allow_dangerous_deserialization=True
        )
    else:
        # Index file doesn't exist, create a new one
        # Define the document loader.
        document_loader = DirectoryLoader(
            path=RAW_DATA_PATH,
            glob="**/*.pdf",
            use_multithreading=True,
            show_progress=True,
            loader_cls=UnstructuredPDFLoader,
            loader_kwargs={"infer_table_structure": True, "strategy": "hi_res"},
        )
        # Load the documents.
        loaded_documents = document_loader.load()

        # Split the documents.
        splitted_documents = RecursiveCharacterTextSplitter().split_documents(
            loaded_documents
        )

        # Create and save the FAISS index.
        vector_db = FAISS.from_documents(splitted_documents, embeddings)
        vector_db.save_local(KNOWLEDGE_BASE_PATH)

    return vector_db
