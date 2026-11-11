import streamlit as st

from frontend.components.sidebar import render_sidebar
from frontend.components.chat_interface import render_chat_interface
from frontend.state.chat_state import initialize_chat
from frontend.components.blueprint_view import render_blueprint_view

# Page configuration
st.set_page_config(
    page_title="PlantIQ | Maintenance Assistant",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Load CSS
def load_css():
    with open("frontend/styles/style.css", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


# Initialize application
load_css()
initialize_chat()

# Render components
render_sidebar()

st.title("⚙️ PlantIQ")
st.caption("Your AI-powered Industrial Maintenance Assistant")
tab1, tab2 = st.tabs([
    "P&ID Asset Explorer",
    "AI Maintenance Assistant"
])

with tab1:
    render_blueprint_view()

with tab2:
    render_chat_interface()