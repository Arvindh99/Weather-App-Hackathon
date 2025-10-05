import streamlit as st
import importlib
from st_screen_stats import WindowQueryHelper

st.set_page_config(page_title="Responsive App", layout="wide")

# --- Setup Helper ---
helper = WindowQueryHelper()

# Detect screen size in real-time
is_mobile = helper.maximum_window_size(max_width=768, key="window_mobile")

# Optional: for debugging
# st.write("Mobile:", is_mobile)

# --- Switch Between Views ---
if is_mobile["status"]:
    module_name = "mobile_app"
else:
    module_name = "desktop_app"

try:
    app = importlib.import_module(module_name)
    if hasattr(app, "render"):
        app.render()
    else:
        st.error(f"⚠️ '{module_name}' does not have a render() function.")
except Exception as e:
    st.error(f"Error loading {module_name}: {e}")
    st.exception(e)
