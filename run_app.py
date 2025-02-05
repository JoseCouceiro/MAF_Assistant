import streamlit as st
import auth
from display_info import Display
from main import main

# Handle authentication callback (Auth0 redirects here after login)
query_params = st.query_params
if "code" in query_params:
    auth_code = query_params["code"]
    token_data = auth.get_access_token(auth_code)
    
    if "access_token" in token_data:
        access_token = token_data["access_token"]
        user_info = auth.get_user_info(access_token)
        st.session_state["user"] = user_info
        st.session_state["access_token"] = access_token
        # Clear the URL parameters after successful login
        st.query_params.clear()

# Display Login or Logout button
__displayer = Display()

if "user" not in st.session_state:
    st.title("Welcome to MAF Assistant")
    login_url = auth.get_login_url()
    __displayer.display_title()
    st.markdown(f"🔑[**Login with Auth0**]({login_url})", unsafe_allow_html=True)
else:
    __displayer.display_title()
    user = st.session_state["user"]
    st.sidebar.write(f"✅ Logged in as: {user.get('name', 'Unknown')}")
    logout_url = auth.get_logout_url()
    st.sidebar.markdown(f"[:blue[**Logout**]]({logout_url})", unsafe_allow_html=True)

# Run app
    main(user['name'])