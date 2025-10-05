import streamlit as st
from streamlit.components.v1 import html

# --- Step 1: Initialize session state for screen width ---
if "screen_width" not in st.session_state:
    st.session_state.screen_width = 1024  # default value

# --- Step 2: Inject JS to detect user screen width ---
html(
    """
    <script>
    const width = window.innerWidth;
    window.parent.postMessage({isStreamlitMessage: true, type: 'setWidth', width: width}, '*')
    </script>
    """,
    height=0,
)

# --- Step 3: Listen for screen width message ---
def handle_msg(msg):
    if msg.type == "setWidth":
        st.session_state.screen_width = msg.width

st.query_params()  # triggers rerun when session_state changes

# --- Step 4: Decide which app to render ---
if st.session_state.screen_width < 768:
    import mobile_app as app  # make sure mobile_app.py has a render() function
else:
    import desktop_app as app  # make sure desktop_app.py has a render() function

# --- Step 5: Render the appropriate app ---
app.render()
