import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI
from flow import extract_pdf, summarize
import uuid
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

# Function to summarize PDF content


def summarize_pdf(file):
    file_path = os.path.join('upload', uploaded_file.name)
    # Save the uploaded file to disk
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue())
    content = extract_pdf(file_path)
    # Placeholder for actual summarization logic
    summary = summarize(content)
    return summary.content

# Function to check if summary has enough information


def has_enough_information(summary):
    required_sections = ["Introduction", "Scope", "Requirements"]
    for section in required_sections:
        if section not in summary:
            return False
    return True

# Function to create requirement analysis


def create_requirement_analysis(summary):
    # Placeholder for actual requirement analysis logic
    analysis = f"Requirement Analysis based on the summary: {summary}"
    return analysis


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "more_info_needed" not in st.session_state:
    st.session_state.more_info_needed = False

# File upload
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")
if uploaded_file:
    summary = summarize_pdf(uploaded_file)
    st.session_state.messages.append({"role": "assistant", "content": summary})
    st.markdown(summary)

    # Check if summary has enough information
    if not has_enough_information(summary):
        st.session_state.more_info_needed = True
        st.session_state.summary = summary

if st.session_state.more_info_needed:
    with st.chat_message("assistant"):
        st.markdown("Please provide more information:")
    prompt = st.chat_input(
        "Please provide more information:", key=str(uuid.uuid4()))
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        # Update summary with additional information
        st.session_state.summary += " " + prompt
        summary = st.session_state.summary
        st.session_state.messages.append(
            {"role": "assistant", "content": summary})
        st.markdown(summary)
        # Check again if enough information is provided
        if has_enough_information(summary):
            st.session_state["more_info_needed"] = False
            # Create requirement analysis
            analysis = create_requirement_analysis(summary)
            st.session_state.messages.append(
                {"role": "assistant", "content": analysis})
            st.markdown(analysis)

else:
    # Accept user input
    if prompt := st.chat_input("Upload your files or your requirements"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Query the assistant using the latest chat history
        chain = prompt | llm
        result = chain.invoke(prompt, messages=st.session_state.messages)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
