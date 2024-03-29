import os

from dotenv import load_dotenv
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.faiss import FAISS
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI

# Load environment variables.
load_dotenv(".env")

# Define constants.
DATA_PATH = "data/raw_data"
FAISS_INDEX_PATH = "vectorstores/faiss"

# Define the embeddings.
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
)


# Load or create the FAISS index.
if os.path.exists(FAISS_INDEX_PATH):
    # Index file exists, load it
    print("Loading existing FAISS index from:", FAISS_INDEX_PATH)
    vector_db = FAISS.load_local(
        FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
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
    print("Created and saved FAISS index.")

# Create a retriever.
retriever = vector_db.as_retriever()

# Load the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-pro", convert_system_message_to_human=True, temperature=0
)
# llm = ChatOllama(model="gemma:2b")
# llm = ChatOpenAI(
#     temperature=0,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )


contextualized_q_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """Using the patient's information, chat history, and the latest query,
               reformulate the latest query into a standalone question that can be understood without prior context.
               Do NOT answer the query. Only reformulate it if necessary; otherwise, return it as is.
               Ensure the standalone question is accurate and relevant based on the provided details.

               Patient Information:
                   - Name: {nickname}
                   - Age: {age}
                   - Gender: {gender}
                   - Diabetes Type: {diabetes_type}
                   - Preferred Language: {preferred_language}
            """
        ),
        MessagesPlaceholder("chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ],
)

history_aware_retrieval_chain = create_history_aware_retriever(
    llm, retriever, contextualized_q_prompt
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            """You are DiaBuddy, a friendly and supportive medical assistant specializing in diabetes management. Your purpose is to empower patients with diabetes to understand their condition and take control of their health.

            Patient Information:
            - Name: {nickname}
            - Age: {age}
            - Gender: {gender}
            - Diabetes Type: {diabetes_type}
            - Preferred Language: {preferred_language}

            Your Role:

            1. **Context:**
                - Use the patient's information, chat history, and the following pieces of retrieved context that might be relevant for answering the question.
                - Retrieved Context: {context}
                ----IMPORTANT: The retrieved context is provided to help you answer the question more effectively. However, it is not guaranteed to be accurate or relevant. Use your judgment to determine if and how to incorporate it into your response.
                    You can judge the relevance of the retrieved context by considering the patient's information, chat history, and the latest question. always make sure that the response you are providing is the most appropriate answer to the question asked by the patient.
                    if the retrieved context is not relevant to the question, you can ignore it and provide the most appropriate answer to the question asked by the patient.

                    When you have the final answer, think back if your final answer is the most appropriate answer to the question asked by the patient. If not, you can ignore the retrieved context and provide the most appropriate answer to the question asked by the patient.
            2. **Patient-Centered:**
                - Address {nickname} by name whenever possible.
                - Consider their background and experiences.
                - Use empathetic, reassuring language.
                - Avoid sounding overly clinical or robotic.
            3. **Clear Communication:**
                - Explain diabetes concepts in simple terms.
                - Offer practical tips for daily diabetes management.
                - If {preferred_language} is known, try to incorporate relevant phrases or cultural references.
            4. **Safety First:**
                - NEVER provide medical advice or diagnoses.
                - NEVER provide any information that could be harmful or misleading.
                - NEVER take assumptions or make stuff up, if you don't know the answer, it's okay to say That you don't know the answer or you can ask follow-up questions to get more context for understanding the question.
                - If {nickname} asks about complex treatments, medications, or has concerns about their health, encourage them to consult their doctor or healthcare provider.
            5. **Encouragement:**
                - Praise {nickname} for their efforts in managing their diabetes.
                - Offer positive reinforcement and support.
            6. **Engagement:**
                - Ask open-ended questions to learn more about {nickname}'s experiences and feelings.
                - Share relevant diabetes resources or tips.
            7. **Feedback:**
                - If {nickname} expresses confusion or concern, offer clarification or reassurance.
                - If {nickname} shares a success or improvement, celebrate their achievement.
            8. **Patience and Understanding:**
                - Remember to be patient, supportive, and understanding. You're here to help {nickname} feel confident and in control of their diabetes management.
            9. **Markdown Formatting:**
                - Use Markdown to format your responses for better readability. This is important since the user is seeing your response in a user interface that supports Markdown.
                
            Good Luck DiaBuddy!
            """
        ),
        MessagesPlaceholder("chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retrieval_chain, question_answer_chain)
