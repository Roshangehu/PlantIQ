import streamlit as st

from backend.database.chat_repository import (
    get_all_chats,
    get_chat_messages
)


def render_sidebar():

    with st.sidebar:

        st.title("⚙️ PlantIQ")
        st.caption("Industrial Maintenance AI")
        st.divider()

        # New Chat button
        if st.button("＋ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.chat_id = None
            st.rerun()

        st.subheader("Recent Chats")

        # Fetch saved conversations
        chats = get_all_chats()

        if not chats:
            st.caption("No conversations yet.")

        for chat in chats:

            chat_id = chat["chat_id"]
            title = chat["title"]

            if st.button(
                title,
                key=f"chat_{chat_id}",
                use_container_width=True
            ):

                # Load selected conversation
                st.session_state.chat_id = chat_id

                st.session_state.messages = get_chat_messages(
                    chat_id
                )

                st.rerun()

        st.divider()
        st.caption("PlantIQ | AI Maintenance Assistant")