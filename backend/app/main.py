import os
from operator import itemgetter
from typing import TypedDict

from app.dependencies.database import get_mongo
from app.utils.chat_message import MongoDBUserChatMessageHistory
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables.utils import ConfigurableFieldSpec
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load environment variables.
load_dotenv("../.env")

# Define constants.
DATA_PATH = "../data"
FAISS_INDEX_PATH = "../vectorstores/faiss"

# Define the embeddings.
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Load or create the FAISS index.
if os.path.exists(FAISS_INDEX_PATH):
    # Index file exists, load it
    print("Loading existing FAISS index from:", FAISS_INDEX_PATH)
    vector_db = FAISS.load_local(
        FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
    )
else:
    # Index file doesn't exist, create a new one
    # Define the document loader.
    # TODO eval loaders
    documentLoader = DirectoryLoader(
        path=DATA_PATH,
        glob="**/*.pdf",
        use_multithreading=True,
        show_progress=True,
        loader_cls=UnstructuredPDFLoader,
    )
    # Load the documents.
    loaded_documents = documentLoader.load()

    # Split the documents.
    splitted_documents = SemanticChunker(
        embeddings=embeddings,
    ).split_documents(loaded_documents)

    # Create the FAISS index.
    print("Creating new FAISS index and saving to:", FAISS_INDEX_PATH)
    vector_db = FAISS.from_documents(splitted_documents, embeddings)
    vector_db.save_local(FAISS_INDEX_PATH)

# Create a retriever.
retriever = vector_db.as_retriever()


class User:
    def __init__(self, name, age, gender, diabetes_type, preferred_language):
        self.name = name
        self.age = age
        self.gender = gender
        self.diabetes_type = diabetes_type
        self.preferred_language = preferred_language


user = User("Hansaka", 23, "Male", "Type 1", "English")

# Define the chat prompts.

prompt_rag = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"""You are a helpful and informative medical assistant called DiaBuddy,
            who specializes diabetes management. Your goal is to provide
            accessible information and support for patients with diabetes while
            prioritizing patient-centered care.

            Answer only using this Knowledge: {{context}}

            Patient Profile:
            Name: {user.name}
            Age: {user.age}
            Gender: {user.gender}
            Diabetes Type: {user.diabetes_type}
            Preferred Language: {user.preferred_language}

            Offer personalized conversation whenever possible, considering {user.name}'s background.
            Provide clear, concise explanations of diabetes-related concepts.
            Offer practical tips for managing their diabetes.
            Use empathetic language that reassures {user.name} and acknowledges their experiences.
            Avoid sounding overly clinical or robotic.
            Refer {user.name} to consult a healthcare professional if a question
            requires medical diagnosis, complex treatment recommendations, or
            changes to an existing care plan.

            Important: It's crucial to understand your capabilities and
            limitations to avoid providing incorrect or potentially harmful advice.
            """,
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)


# Load the LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
llm.invoke("Hello")


class ChatInput(TypedDict):
    input: str


_template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:
{chat_history}
Follow Up Input: {input}
Standalone question:"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)

standalone_question = RunnableParallel(
    input=RunnableParallel(
        input=RunnablePassthrough(),
        chat_history=lambda x: get_buffer_string(x["chat_history"]),
    )
    | CONDENSE_QUESTION_PROMPT
    | llm
    | StrOutputParser(),
)

rag_chat_chain = (
    RunnableParallel(
        context=(itemgetter("input") | retriever), input=itemgetter("input")
    )
    | RunnableParallel(output=(prompt_rag | llm), docs=itemgetter("context"))
).with_types(input_type=ChatInput)

history_retriever = lambda user_id: MongoDBUserChatMessageHistory(
    user_id=user_id, chat_history_service=get_mongo()
)

chat_with_history = RunnableWithMessageHistory(
    runnable=standalone_question | rag_chat_chain,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
    get_session_history=history_retriever,
    history_factory_config=[
        ConfigurableFieldSpec(
            id="user_id",
            annotation=str,
            name="User ID",
            description="Unique identifier of the user.",
        )
    ],
)
