import openai
import streamlit as st
import os

def create_chat_gpt():
    st.title("💬 Chatbot")
    st.caption("🚀 A streamlit chatbot powered by OpenAI LLM")
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if query := st.chat_input():
        messages = [{"role":"system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query}]
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
        responsed_msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": responsed_msg})
        st.chat_message("assistant").write(responsed_msg)