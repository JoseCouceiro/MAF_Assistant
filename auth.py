import streamlit as st
from streamlit_auth0 import login_button

# Auth0 Configuration
AUTH0_DOMAIN = "dev-25gut1ea7c13we7c.us.auth0.com"
AUTH0_CLIENT_ID = "o6vcbkvYS6Mw774l1UfMaPNwApL78j9X"

def login():
    """
    Displays the Auth0 login button and handles authentication.
    """
    user_info = login_button(domain=AUTH0_DOMAIN,
                             client_id=AUTH0_CLIENT_ID)

    if user_info:
        st.session_state["user"] = user_info  # Store user in session state
        st.success(f"✅ Logged in as {user_info.get('name', 'Unknown')}")
        return user_info
    else:
        st.warning("🔹 Please log in to continue.")
        return None

def logout():
    """
    Logs the user out by clearing session state.
    """
    if "user" in st.session_state:
        del st.session_state["user"]
    st.success("✅ Logged out successfully! Refresh the page.")

