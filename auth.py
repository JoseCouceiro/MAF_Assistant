import streamlit as st
import requests
import urllib.parse

# 🔹 Auth0 Credentials (replace with your values)
AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8501"  # Streamlit URL

# 🔹 Auth0 Endpoints
AUTH_URL = f"https://{AUTH0_DOMAIN}/authorize"
TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

# Function to generate the login URL
def get_login_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
    }
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

# Function to exchange Auth0 code for an access token
def get_access_token(auth_code):
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(TOKEN_URL, data=payload)
    return response.json()

# Function to fetch user info
def get_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USERINFO_URL, headers=headers)
    return response.json()

# Function to log out the user
def get_logout_url():
    return f"https://{AUTH0_DOMAIN}/v2/logout?returnTo={REDIRECT_URI}&client_id={CLIENT_ID}"
