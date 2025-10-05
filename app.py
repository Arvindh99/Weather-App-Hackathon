import streamlit as st
from streamlit_javascript import st_javascript
from user_agents import parse
import importlib

st.set_page_config(page_title="Responsive Weather App", layout="wide")

def detect_device():
    """Detect if the user is using a mobile or tablet device."""
    user_agent_string = st_javascript("window.navigator.userAgent;")
    if user_agent_string:
        ua = parse(user_agent_string)
        return ua.is_mobile or ua.is_tablet
    return False

def main():
    # Cache the result so we don't re-run detection unnecessarily
    if "is_mobile" not in st.session_state:
        st.session_state.is_mobile = detect_device()

    if st.session_state.is_mobile:
        st.session_state.device_type = "mobile"
    else:
        st.session_state.device_type = "desktop"

    # Dynamically import the correct view
    try:
        module_name = (
            "mobile_app" if st.session_state.device_type == "mobile" else "desktop_app"
        )
        module = importlib.import_module(module_name)

        if hasattr(module, "render"):
            module.render()
        else:
            st.error(f"⚠️ {module_name}.py is missing a render() function.")
    except Exception as e:
        st.error(f"Error loading view: {e}")

if __name__ == "__main__":
    main()
