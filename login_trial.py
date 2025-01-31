import streamlit as st
from auth0.authentication import GetToken
from auth0.management import Auth0
import requests
import json
import os

# Configuración de Auth0
AUTH0_CLIENT_ID = st.secrets["AUTH0_CLIENT_ID"]
AUTH0_CLIENT_SECRET = st.secrets["AUTH0_CLIENT_SECRET"]
AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
AUTH0_REDIRECT_URI = "http://localhost:8501"
AUTH0_AUDIENCE = f"https://{AUTH0_DOMAIN}/userinfo"

def login_with_auth0():
    """
    Genera la URL de login con Auth0.
    """
    return (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"audience={AUTH0_AUDIENCE}&"
        f"response_type=code&"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"redirect_uri={AUTH0_REDIRECT_URI}&"
        f"scope=openid profile email"
    )

def get_auth0_token(auth_code):
    """
    Intercambia el código de autorización por un token de acceso.
    """
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    headers = {"content-type": "application/json"}
    data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": AUTH0_REDIRECT_URI
    }
    response = requests.post(token_url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()

def get_user_info(access_token):
    """
    Obtiene información del usuario usando el token de acceso.
    """
    userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    user_info = response.json()
    print("User Info:", user_info)  # Debugging line
    return response.json()

def main():
    st.title("Auth0 Login Demo")

    # Check if user is already logged in
    if "user" not in st.session_state:
        st.session_state.user = None

    # If logged in, display user info
    if st.session_state.user:
        user = st.session_state.user
        st.write(f"Welcome,  {user['name']}!")
        st.write(f"Email:  {user['name']}")
        if st.button("Logout"):
            st.session_state.user = None
            st.rerun()
    else:
        # Handle OAuth callback
        query_params = st.experimental_get_query_params()
        st.write(f"Query Params: {query_params}")  # Debugging line
        if "code" in query_params:
            auth_code = query_params["code"][0]
            token_info = get_auth0_token(auth_code)
            user_info = get_user_info(token_info["access_token"])
            st.session_state.user = user_info
            st.rerun()
        else:
            # Display login link
            login_url = login_with_auth0()
            st.write(f"Login URL: {login_url}")  # Debugging line
            st.markdown(f"[Login with Auth0]({login_url})")

if __name__ == "__main__":
    main()
