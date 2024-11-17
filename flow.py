from dotenv import load_dotenv
import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))


def extract_pdf(file_path):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    return " ".join([doc.page_content for doc in docs])


def summarize(user_input):

    predefined_sections = {
        "Introduction": "",
        "Objectives": "",
        "Methodology": "",
        "Results": "",
        "Conclusion": ""
    }

    system_prompt = (
        f"You are an assistant for document summarize tasks. Summarize the content and categorize it into these sections: {list(predefined_sections.keys())}"
        "If a section lacks sufficient information, leave it empty and indicate that more input is needed."
        "answer concise."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    chain = prompt | llm
    response = chain.invoke({"input": user_input})

    return response
