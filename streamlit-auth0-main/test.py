from auth0_component import login_button
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

clientId = st.secrets('AUTH0_CLIENT_ID')" "
domain = st.secrets('AUTH0_DOMAIN')" "

st.title('Welcome to Auth0-Streamlit')

with st.echo():
    user_info = login_button(clientId = clientId, domain = domain, key=clientId)
    if user_info:
        st.write(f'Hi {user_info["nickname"]}')
        # st.write(user_info) # some private information here
        
if not user_info:
    st.write("Please login to continue")
