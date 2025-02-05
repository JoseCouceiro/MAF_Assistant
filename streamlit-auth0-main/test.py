from auth0_component import login_button
import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()

clientId = "o6vcbkvYS6Mw774l1UfMaPNwApL78j9X"
domain = "dev-25gut1ea7c13we7c.us.auth0.com"

st.title('Welcome to Auth0-Streamlit')

with st.echo():
    user_info = login_button(clientId = clientId, domain = domain, key=clientId)
    if user_info:
        st.write(f'Hi {user_info["nickname"]}')
        # st.write(user_info) # some private information here
        
if not user_info:
    st.write("Please login to continue")
