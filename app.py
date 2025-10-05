# main_app.py
import streamlit as st
import streamlit.components.v1 as components

def main():
    st.set_page_config(layout="wide")

    # JavaScript for device detection and redirection
    js_code = """
    <script>
        function detectDeviceAndRedirect() {
            var userAgent = navigator.userAgent || navigator.vendor || window.opera;
            var isMobile = /android|ipad|iphone|ipod|blackberry|iemobile|opera mini/i.test(userAgent);

            if (isMobile) {
                window.location.href = "/mobile_app"; // Redirect to the mobile app
            } else {
                window.location.href = "/desktop_app"; // Redirect to the desktop app
            }
        }
        detectDeviceAndRedirect();
    </script>
    """
    components.html(js_code, height=0, width=0)

    st.markdown("Redirecting to the appropriate version...")

if __name__ == "__main__":
    main()
