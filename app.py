import streamlit as st
from streamlit.components.v1 import html
import importlib

MOBILE_BREAKPOINT = 768  # px cutoff between mobile & desktop

# --- 1. Check for ?width= param in query params ---
params = st.query_params
width_str = params.get("width", None)

# --- 2. If not present, inject JS to detect width and reload the app ---
if width_str is None:
    html(
        """
        <script>
        const width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
        const url = new URL(window.location.href);
        url.searchParams.set("width", width);
        window.location.replace(url);  // reloads the page once with ?width=<value>
        </script>
        """,
        height=0,
    )
    st.stop()  # stop execution until reload happens

# --- 3. Convert to int safely ---
try:
    width = int(width_str[0] if isinstance(width_str, list) else width_str)
except Exception:
    width = 1024  # fallback if conversion fails

# --- 4. Dynamically import the right app ---
if width < MOBILE_BREAKPOINT:
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
