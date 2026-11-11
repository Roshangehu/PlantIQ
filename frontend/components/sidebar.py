import streamlit as st


def render_sidebar():

    with st.sidebar:

        st.title("⚙️ PlantIQ")
        st.caption("Industrial Maintenance AI")

        st.divider()

        if st.button("＋ New Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        st.subheader("Recent Chats")

        st.button(
            "Pump troubleshooting",
            use_container_width=True
        )

        st.button(
            "Motor maintenance",
            use_container_width=True
        )

        st.button(
            "Equipment inspection",
            use_container_width=True
        )

        st.divider()

        st.caption("PlantIQ | AI Maintenance Assistant")