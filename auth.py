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
    """
    Generate the Auth0 login URL with required parameters.
    This function constructs a URL for initiating the OAuth2 authorization flow
    with Auth0. It encodes the necessary parameters and returns the full login URL.
    Returns:
        str: The fully constructed Auth0 authorization URL.
    """
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
    }
    return f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

# Function to exchange Auth0 code for an access token
def get_access_token(auth_code):
    """
    Exchange an authorization code for an access token.
    This function sends a POST request to the Auth0 token endpoint to exchange
    the provided authorization code for an access token. The access token can be 
    used to authenticate API requests.
    Args:
        auth_code (str): The authorization code received from Auth0 after user login.
    Returns:
        dict: A JSON response containing the access token, ID token, and other metadata.
    """
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
    """
    Fetch user information from Auth0 using the provided access token.
    This function sends a GET request to the Auth0 `/userinfo` endpoint with the
    provided access token. It returns the user's profile information as a JSON
    response.
    Args:
        access_token (str): The access token obtained during the OAuth2 authorization
                             process. This token is used to authenticate the request to
                             the Auth0 API.
    Returns:
        dict: A JSON response containing the user's profile information, such as
              name, email, and picture.
    """
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(USERINFO_URL, headers=headers)
    return response.json()

# Function to log out the user
def get_logout_url():
    """
    Generate the URL to log out the user from Auth0.
    This function constructs the Auth0 logout URL, including the client ID and
    the return URL where the user should be redirected after logout.
    Returns:
        str: The fully constructed Auth0 logout URL.
    """
    return f"https://{AUTH0_DOMAIN}/v2/logout?returnTo={REDIRECT_URI}&client_id={CLIENT_ID}"
