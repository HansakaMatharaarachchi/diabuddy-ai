import os
from operator import itemgetter
from typing import Dict, TypedDict

from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings, ChatOpenAI

# Load environment variables.
load_dotenv()

# Define constants.
DATA_PATH = "data"
FAISS_INDEX_PATH = "vectorstores/faiss"
# Define the embeddings.
# TODO eval embeddings
openAIEmbeddings = OpenAIEmbeddings()
# Load or create the FAISS index.
# TODO eval indexes
if len(os.listdir(FAISS_INDEX_PATH)):
    # Index file exists, load it
    print("Loading existing FAISS index from:", FAISS_INDEX_PATH)
    vector_db = FAISS.load_local(FAISS_INDEX_PATH, openAIEmbeddings, allow_dangerous_deserialization=True)
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

    # Add metadata.
    # for document in loaded_documents:
    #     document.metadata['file_name'] = document.metadata['source']

    # Split the documents.
    splitted_documents = SemanticChunker(
        embeddings=openAIEmbeddings,
    ).split_documents(loaded_documents)

    # Create the FAISS index.
    print("Creating new FAISS index and saving to:", FAISS_INDEX_PATH)
    vector_db = FAISS.from_documents(splitted_documents, openAIEmbeddings)
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
prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                """You are a helpful and informative medical assistant called DiaBuddy,
              who specializes diabetes management. Your goal is to provide
              accessible information and support for patients with diabetes while
              prioritizing patient-centered care.

              Provide clear, concise explanations of diabetes-related concepts.
              Offer practical tips for managing their diabetes.
              Use empathetic language that reassures the patient and acknowledges their experiences.
              Avoid sounding overly clinical or robotic.
              Refer users to consult a healthcare professional if a question
              requires medical diagnosis, complex treatment recommendations, or
              changes to an existing care plan.

              Important: It's crucial to understand your capabilities and
              limitations to avoid providing incorrect or potentially harmful advice.
              """)
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

prompt_personalised = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=(
                f"""You are a helpful and informative medical assistant called DiaBuddy,
                who specializes diabetes management. Your goal is to provide
                accessible information and support for patients with diabetes while
                prioritizing patient-centered care.

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
                """)
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

prompt_personalised_context = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"""You are a helpful and informative medical assistant called DiaBuddy,
            who specializes diabetes management. Your goal is to provide
            accessible information and support for patients with diabetes while
            prioritizing patient-centered care.

            Additional Knowledge: {{context}}

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
            """
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

prompt_personalised_context_memory = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            f"""You are a helpful and informative medical assistant called DiaBuddy,
            who specializes diabetes management. Your goal is to provide
            accessible information and support for patients with diabetes while
            prioritizing patient-centered care.

            Additional Knowledge: {{context}}

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
            """
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

message = "Can i eat some ice cream?"

# Load the LLM
llm = ChatOpenAI(streaming=True)

# # Response without any modifications
# llm.invoke(message)
#
# # Response with the guided prompt template
# chain = prompt | llm | StrOutputParser()
# chain.invoke({"input": message})
#
# # Response with the guided prompt template and user profile
# chain = prompt_personalised | llm | StrOutputParser()
# chain.invoke({"input": message})

# Response with the guided prompt template, user profile and context memory
# Create message history.# Create message history.
chat_history = ChatMessageHistory()

INITIAL_MESSAGE = "Hello, I'm DiaBuddy, your personal diabetes assistant. How can I help you today?"

# Function to build the knowledge retrieval and processing chain.
document_chain = create_stuff_documents_chain(llm, prompt_personalised_context_memory)


# Helper function to extract the most recent user message for retrieval.
def parse_retriever_input(params: Dict):
    return params["messages"][-1].content


# Chain for information retrieval - fetches relevant information based on user input.
retrieval_chain = (
        RunnablePassthrough.assign(
            context=parse_retriever_input | retriever
        )
        | document_chain
)


# Main function to handle a single query/response cycle.
def executeQuery(user_input, chat_history):
    chat_history.add_user_message(user_input)

    # Process the input through the retrieval chain.
    response = retrieval_chain.invoke({
        "messages": chat_history.messages
    })

    chat_history.add_ai_message(response)
    return response


if __name__ == "__main__":
    # Conversation loop.
    while True:
        if len(chat_history.messages) == 0:
            # Add initial message.
            chat_history.add_ai_message(INITIAL_MESSAGE)
            print("DiaBuddy: ", INITIAL_MESSAGE)

        try:
            user_input = input(f"{user.name} : ")
            if user_input.lower() == 'exit':
                break

            chat_history.add_user_message(user_input)
            response = executeQuery(user_input, chat_history)
            chat_history.add_ai_message(response)
            print("DiaBuddy: ", response)
        except KeyboardInterrupt:
            print("Goodbye!!!!")
            break


class ChatInput(TypedDict):
    input: str


# Chain for information retrieval - fetches relevant information based on user input.
# TODO used for testing purposes
chat_chain = (
        RunnableParallel(
            context=(itemgetter("input") | retriever), input=itemgetter("input")
        )
        | RunnableParallel(
    input=(prompt_personalised_context | llm),
    docs=itemgetter("context")
)).with_types(input_type=ChatInput)
