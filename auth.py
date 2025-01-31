import streamlit as st
from streamlit_auth0 import login_button

# Configure Auth0
AUTH0_DOMAIN = "dev-25gut1ea7c13we7c.us.auth0.com"
AUTH0_CLIENT_ID = "o6vcbkvYS6Mw774l1UfMaPNwApL78j9X"
AUTH0_CLIENT_SECRET = "V0AE8zcNlJ_EwcKc5NyD66l9USKAykQFLD3DlO-4SvHrBf6rI_XnB6TZHNAE5BY2"

""" auth0 = Auth0(
    domain=AUTH0_DOMAIN,
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET
) """

def login():
    login_button(domain=AUTH0_DOMAIN, client_id=AUTH0_CLIENT_ID)

def logout():
    auth0.logout()
    st.session_state.pop("user", None)
