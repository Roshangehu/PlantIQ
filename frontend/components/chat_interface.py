import streamlit as st
import httpx

from frontend.state.chat_state import add_message
from frontend.components.message import render_messages


API_URL = "http://127.0.0.1:8000/api/chat"


def render_chat_interface():

    # Display previous messages
    render_messages(st.session_state.messages)

    # Chat input
    prompt = st.chat_input(
        "Ask PlantIQ about equipment or maintenance..."
    )

    if prompt:

        # Save user question
        add_message("user", prompt)

        try:

            # Send question to FastAPI
            response = httpx.post(
                API_URL,
                json={"question": prompt},
                timeout=30
            )

            response.raise_for_status()

            # Extract answer
            answer = response.json()["answer"]

        except httpx.RequestError:

            answer = "Unable to connect to PlantIQ backend."

        except httpx.HTTPStatusError:

            answer = "PlantIQ backend returned an error."

        except (KeyError, ValueError):

            answer = "Invalid response received from PlantIQ backend."

        # Save assistant response
        add_message("assistant", answer)

        # Refresh interface
        st.rerun()