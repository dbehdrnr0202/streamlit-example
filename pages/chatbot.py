import openai
import streamlit as st
from streamlit_chat import message
import os
import time


def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


def run_chat_bot():
    st.title("💬 Chatbot")
    st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "How can I help you?"}
        ]
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if query := st.chat_input():
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        st.chat_message("user").write(query)
        st.session_state.messages.append({"role": "user", "content": query})
        responsed_msg = response.choices[0].message.content
        st.session_state.messages.append(
            {"role": "assistant", "content": responsed_msg}
        )
        st.chat_message("assistant").write(responsed_msg)