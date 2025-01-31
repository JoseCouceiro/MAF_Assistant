import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
import requests
import os

# Configurations (replace with your Auth0 credentials)
AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
CLIENT_ID = st.secrets["AUTH0_CLIENT_ID"]
CLIENT_SECRET = st.secrets["AUTH0_CLIENT_SECRET"]
REDIRECT_URI = "http://localhost:8501/callback"

# Configuración de Auth0
AUTH0_AUTHORIZE_URL = f"https://{st.secrets["AUTH0_DOMAIN"]}/authorize"
AUTH0_TOKEN_URL = f"https://{st.secrets["AUTH0_DOMAIN"]}/oauth/token"
AUTH0_USERINFO_URL = f"https://{st.secrets["AUTH0_DOMAIN"]}/userinfo"
AUTH0_LOGOUT_URL = f"https://{st.secrets["AUTH0_DOMAIN"]}/v2/logout"

# Initialize session state for tokens and user info
if "auth0_token" not in st.session_state:
    st.session_state["auth0_token"] = None
if "user_info" not in st.session_state:
    st.session_state["user_info"] = None

def login():
    """Redirect the user to the Auth0 login page."""
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope="openid profile email")
    authorization_url, state = oauth.create_authorization_url(AUTH0_AUTHORIZE_URL)
    st.session_state["auth_state"] = state
    st.experimental_set_query_params(redirect_url=authorization_url)

def logout():
    """Log out the user and clear session data."""
    st.session_state["auth0_token"] = None
    st.session_state["user_info"] = None
    logout_url = f"{AUTH0_LOGOUT_URL}?client_id={CLIENT_ID}&returnTo={REDIRECT_URI}"
    st.experimental_set_query_params() 
    st.write(f"[Click here to log out completely]({logout_url})")

def handle_callback():
    """Handle the OAuth2 callback from Auth0."""
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        code = query_params["code"][0]
        state = query_params.get("state", [None])[0]

        if state != st.session_state.get("auth_state"):
            st.error("Invalid state parameter!")
            return

        # Exchange the authorization code for tokens
        oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
        token = oauth.fetch_token(
            AUTH0_TOKEN_URL,
            authorization_response=st.experimental_get_query_params(),
            grant_type="authorization_code",
            client_secret=CLIENT_SECRET,
        )

        st.session_state["auth0_token"] = token

        # Fetch user information
        response = requests.get(AUTH0_USERINFO_URL, headers={"Authorization": f"Bearer {token['access_token']}"})
        if response.status_code == 200:
            st.session_state["user_info"] = response.json()
        else:
            st.error("Failed to fetch user information.")
    else:
        st.error("No code found in callback.")

def main():
    st.title("Streamlit Auth0 Login Demo")

    # Handle callback if redirected from Auth0
    if 'callback' in st.experimental_get_query_params():
        handle_callback()

    # Show login or user info
    if st.session_state["user_info"]:
        user_info = st.session_state["user_info"]
        st.success(f"Welcome, {user_info['name']}!")
        st.image(user_info["picture"], width=100)
        st.json(user_info)
        if st.button("Log out"):
            logout()
    else:
        st.info("You are not logged in.")
        if st.button("Log in"):
            login()

if __name__ == "__main__":
    main()
