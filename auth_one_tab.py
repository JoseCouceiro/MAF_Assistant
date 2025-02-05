import streamlit as st
import requests
import webbrowser
from urllib.parse import urlencode

# Auth0 Configuration

AUTH0_DOMAIN = "dev-25gut1ea7c13we7c.us.auth0.com"
CLIENT_ID = "o6vcbkvYS6Mw774l1UfMaPNwApL78j9X"
CLIENT_SECRET = "V0AE8zcNlJ_EwcKc5NyD66l9USKAykQFLD3DlO-4SvHrBf6rI_XnB6TZHNAE5BY2"
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

