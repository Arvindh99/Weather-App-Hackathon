import streamlit as st
from streamlit.components.v1 import html
import importlib

# --- Step 1: Initialize session state for screen width ---
if "screen_width" not in st.session_state:
    st.session_state.screen_width = 1024  # default fallback

# --- Step 2: Inject JavaScript to detect user screen width ---
html(
    """
    <script>
    const width = window.innerWidth;
    window.parent.postMessage({isStreamlitMessage: true, type: 'setWidth', width: width}, '*');
    </script>
    """,
    height=0,
)

# --- Step 3: Set up Streamlit query params (replaces deprecated experimental API) ---
params = st.query_params

# --- Step 4: Handle incoming message (simulated reload when width detected) ---
if "width" in params:
    try:
        st.session_state.screen_width = int(params["width"])
    except ValueError:
        pass

# --- Step 5: Auto-select app based on screen width ---
if st.session_state.screen_width < 768:
    app_module = importlib.import_module("mobile_app")
else:
    app_module = importlib.import_module("desktop_app")

# --- Step 6: Run the app ---
app_module.render()
