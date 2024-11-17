import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from flow import extract_pdf, summarize

import os
from dotenv import load_dotenv
load_dotenv()

# Chat UI title
st.header("Upload your own files and ask questions like ChatGPT")
st.subheader('File type supported: PDF/DOCX/TXT :city_sunrise:')


llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))


with st.sidebar:
    uploaded_files = st.file_uploader(
        "Please upload your files", accept_multiple_files=True, type=None)

# Check if files are uploaded
if uploaded_files:
    # Print the number of files to console
    print(f"Number of files uploaded: {len(uploaded_files)}")

    # Load the data and perform preprocessing only if it hasn't been loaded before

    # Load the data from uploaded PDF files
    documents = []
    for uploaded_file in uploaded_files:
        # Get the full file path of the uploaded file
        # file_path = os.path.join(os.getcwd(), uploaded_file.name)
        file_path = os.path.join('upload', uploaded_file.name)

        # Save the uploaded file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        # Use UnstructuredFileLoader to load the PDF file
        loaded_documents = extract_pdf(file_path)

        documents.append(loaded_documents)

    # Store the processed data in session state for reuse
    st.session_state.processed_data = {
        "documents": documents
    }

    documents = st.session_state.processed_data["documents"]
    # print(documents)
    # Initialize Langchain's QA Chain with the vectorstore

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if not documents:
        summary = summarize(documents)
        st.session_state.messages.append(
            {"role": "assistant", "content": summary.content})
        st.markdown(summary.content)

    # Accept user input
    if prompt := st.chat_input("Upload your files or your requirements"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query the assistant using the latest chat history
        result = llm.query(prompt, messages=st.session_state.messages)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            full_response = result.content
            message_placeholder.markdown(full_response + "|")
        message_placeholder.markdown(full_response)
        print(full_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response})

else:
    st.write("Please upload your files.")
