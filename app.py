# main.py
import streamlit as st
from streamlit.components.v1 import html
import importlib

# Default fallback width (used if something goes wrong)
DEFAULT_WIDTH = 1024
MOBILE_BREAKPOINT = 768  # px - change if you want

# 1) Read existing query params
params = st.query_params

# 2) If width param not present or differs from current window width, inject JS to set it and reload
if "width" not in params:
    # JS computes the viewport width and reloads the page with ?width=<value>
    js = """
    <script>
    (function() {
      try {
        const width = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
        const params = new URLSearchParams(window.location.search);
        if (params.get('width') != String(width)) {
          params.set('width', width);
          const newUrl = window.location.pathname + '?' + params.toString();
          // Replace location so history doesn't blow up on repeated reruns
          window.location.replace(newUrl);
        }
      } catch (e) {
        console.log('width-js-error', e);
      }
    })();
    </script>
    """
    # Inject JS and stop execution until reload happens (so we don't render both)
    html(js, height=0)
    st.stop()

# 3) If width param exists, parse it
try:
    width_param = int(params.get("width", [DEFAULT_WIDTH])[0])
except Exception:
    width_param = DEFAULT_WIDTH

# Optional: allow override via a dev/test toggle (comment out if you don't want it)
# view_override = st.sidebar.selectbox("Force view (dev only)", ["Auto", "Desktop", "Mobile"])
# if view_override == "Desktop": width_param = DEFAULT_WIDTH
# if view_override == "Mobile": width_param = MOBILE_BREAKPOINT - 1

# 4) Choose module based on breakpoint
if width_param < MOBILE_BREAKPOINT:
    app_name = "mobile_app"
else:
    app_name = "desktop_app"

# 5) Import & render chosen app (expect render() defined)
try:
    app_module = importlib.import_module(app_name)
    if hasattr(app_module, "render"):
        app_module.render()
    else:
        st.error(f"Module '{app_name}' does not expose a render() function.")
except Exception as e:
    st.error(f"Error loading {app_name}: {e}")
    st.exception(e)
