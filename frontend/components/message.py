import streamlit as st


def render_messages(messages):

    for message in messages:

        role = message["role"]
        content = message["content"]

        with st.chat_message(role):

            if role == "assistant":

                st.markdown("**⚙️ PlantIQ**")

            st.markdown(content)