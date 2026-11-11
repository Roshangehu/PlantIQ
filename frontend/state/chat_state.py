import streamlit as st


def initialize_chat():

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_id" not in st.session_state:
        st.session_state.chat_id = None


def add_message(role, content):

    st.session_state.messages.append({
        "role": role,
        "content": content
    })