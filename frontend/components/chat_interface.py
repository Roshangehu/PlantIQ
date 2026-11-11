import streamlit as st
import httpx

from frontend.state.chat_state import add_message
from frontend.components.message import render_messages
from backend.database.chat_repository import create_chat, save_message
API_URL = "http://127.0.0.1:8000/api/chat"


def render_chat_interface():

    render_messages(st.session_state.messages)

    prompt = st.chat_input(
        "Ask PlantIQ about equipment or maintenance..."
    )

    if prompt:

        history = st.session_state.messages.copy()

    # Create a new database conversation if needed
    if st.session_state.chat_id is None:
        st.session_state.chat_id = create_chat(prompt[:50])

    chat_id = st.session_state.chat_id

    # Save user message
    add_message("user", prompt)
    save_message(chat_id, "user", prompt)

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

    except httpx.TimeoutException:
        answer = "Request timed out. Please try again."

    except httpx.RequestError:
        answer = "Unable to connect to PlantIQ backend."

    except httpx.HTTPStatusError:
        answer = "Backend error. Please try again."

    except (KeyError, ValueError):
        answer = "Invalid response received from PlantIQ backend."

    # Save assistant response
    add_message("assistant", answer)
    save_message(chat_id, "assistant", answer)

    st.rerun()