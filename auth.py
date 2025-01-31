import streamlit as st
from streamlit_auth0 import login_button

# Configure Auth0
AUTH0_DOMAIN = st.secrets('AUTH0_DOMAIN')" "
AUTH0_CLIENT_ID = st.secrets('AUTH0_CLIENT_ID')" "
AUTH0_CLIENT_SECRET = st.secrets('AUTH0_CLIENT_SECRET')" "

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
