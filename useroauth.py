import streamlit as st
from auth0.authentication import GetToken
from auth0.management import Auth0
import requests

class Login:
    
    AUTH0_CLIENT_ID = st.secrets["AUTH0_CLIENT_ID"]
    AUTH0_CLIENT_SECRET = st.secrets["AUTH0_CLIENT_SECRET"]
    AUTH0_DOMAIN = st.secrets["AUTH0_DOMAIN"]
    AUTH0_REDIRECT_URI = "http://localhost:8501"
    AUTH0_AUDIENCE = f"https://{AUTH0_DOMAIN}/userinfo"

    def login_with_auth0(self):
        """
        Generates login URL with Auth0.
        """
        return (
            f"https://{self.AUTH0_DOMAIN}/authorize?"
            f"audience={self.AUTH0_AUDIENCE}&"
            f"response_type=code&"
            f"client_id={self.AUTH0_CLIENT_ID}&"
            f"redirect_uri={self.AUTH0_REDIRECT_URI}&"
            f"scope=openid profile email"
        )

    def get_auth0_token(self, auth_code):
        """
        Swaps access code for an access token.
        """
        token_url = f"https://{self.AUTH0_DOMAIN}/oauth/token"
        headers = {"content-type": "application/json"}
        data = {
            "grant_type": "authorization_code",
            "client_id": self.AUTH0_CLIENT_ID,
            "client_secret": self.AUTH0_CLIENT_SECRET,
            "code": auth_code,
            "redirect_uri": self.AUTH0_REDIRECT_URI,
        }
        response = requests.post(token_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    def get_user_info(self, access_token):
        """
        Retrieves user information using an access token.
        """
        userinfo_url = f"https://{self.AUTH0_DOMAIN}/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(userinfo_url, headers=headers)
        response.raise_for_status()
        return response.json()

    def show_login_page(self):

        # Check if user is already logged in
        if "user" not in st.session_state:
            st.session_state.user = None

        # If logged in, display user info
        if st.session_state.user:
            user = st.session_state.user
            st.write(f"Welcome, {user['name']}!")
            st.write(f"Email: {user['email']}")
            if st.button("Logout"):
                st.session_state.user = None
                st.experimental_rerun()
        else:
            # Handle OAuth callback
            query_params = st.experimental_get_query_params()
            if "code" in query_params:
                auth_code = query_params["code"][0]
                token_info = self.get_auth0_token(auth_code)
                user_info = self.get_user_info(token_info["access_token"])
                st.session_state.user = user_info
                st.experimental_rerun()
            else:
                # Display login link
                login_url = self.login_with_auth0()
                st.markdown(f"[Login with Auth0]({login_url})")
