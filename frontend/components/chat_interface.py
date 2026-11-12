import streamlit as st
import httpx

from frontend.state.chat_state import add_message
from frontend.components.message import render_messages
from backend.database.chat_repository import create_chat, save_message

API_URL = "http://127.0.0.1:8000/api/chat"


def render_chat_interface():

    render_messages(st.session_state.messages)

    prompt = st.chat_input("Ask PlantIQ anything...")

    if prompt is not None and prompt.strip():

        prompt = prompt.strip()

        history = st.session_state.messages.copy()

        if st.session_state.chat_id is None:
            st.session_state.chat_id = create_chat(prompt[:50])

        # Save user message
        add_message("user", prompt)

        save_message(
            st.session_state.chat_id,
            "user",
            prompt
        )

        try:
            with st.spinner("PlantIQ is thinking..."):

                response = httpx.post(
                    API_URL,
                    json={
                        "question": prompt,
                        "history": history
                    },
                    timeout=30
                )

                response.raise_for_status()

                answer = response.json()["answer"]

            # Save assistant response
            add_message("assistant", answer)

            save_message(
                st.session_state.chat_id,
                "assistant",
                answer
            )

        except httpx.TimeoutException:
            st.error("Request timed out. Please try again.")

        except httpx.RequestError:
            st.error("Unable to connect to PlantIQ API.")

        except (httpx.HTTPStatusError, KeyError, ValueError):
            st.error("Something went wrong while processing your question.")

        st.rerun()