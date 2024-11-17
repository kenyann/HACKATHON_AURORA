from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()


st.title("ChatGPT-like clone")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Add file uploader
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # Process the uploaded file if needed
    st.session_state.messages.append(
        {"role": "user", "content": f"Uploaded file: {uploaded_file.name}"})
    with st.chat_message("user"):
        st.markdown(f"Uploaded file: {uploaded_file.name}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append(
        {"role": "assistant", "content": response})
