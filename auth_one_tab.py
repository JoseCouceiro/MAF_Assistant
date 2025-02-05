import streamlit as st
import requests
import webbrowser
from urllib.parse import urlencode

# Auth0 Configuration

AUTH0_DOMAIN = st.secrets('AUTH0_DOMAIN')" "
CLIENT_ID = st.secrets('AUTH0_CLIENT_ID')" "
CLIENT_SECRET = st.secrets('AUTH0_CLIENT_SECRET')" "
REDIRECT_URI = "http://localhost:8501"  # Streamlit URL

AUTH_URL = f"https://{AUTH0_DOMAIN}/authorize"
TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
USER_INFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

# Generate the login URL
def get_login_url():
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email"
    }
    return f"{AUTH_URL}?{urlencode(params)}"

# Exchange authorization code for tokens
def get_tokens(auth_code):
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, data=data)
    return response.json()

# Get user info from Auth0
def get_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USER_INFO_URL, headers=headers)
    return response.json()

