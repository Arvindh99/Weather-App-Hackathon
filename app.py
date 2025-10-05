import streamlit as st
import importlib
import streamlit.components.v1 as components

st.set_page_config(page_title="Responsive Weather App", layout="wide")

# Inject JavaScript to detect screen width and store it in query params
components.html(
    """
    <script>
        const width = window.innerWidth;
        const view = width < 768 ? "mobile" : "desktop";
        const current = new URLSearchParams(window.location.search).get("view");

        if (current !== view) {
            const newUrl = new URL(window.location.href);
            newUrl.searchParams.set("view", view);
            window.location.replace(newUrl.toString());
        }
    </script>
    """,
    height=0,
)

# Get current view from query params
view = st.query_params.get("view", ["desktop"])[0]

# Dynamically import the correct view
try:
    module = importlib.import_module("mobile_app" if view == "mobile" else "desktop_app")
    if hasattr(module, "render"):
        module.render()
    else:
        st.error(f"⚠️ {view}_app.py missing render() function.")
except Exception as e:
    st.error(f"Error loading {view}_app: {e}")
