import os
import streamlit as st
from dotenv import load_dotenv

# Intentar cargar variables de entorno locales
load_dotenv()

# Detectar entorno y cargar credenciales
if "auth0_client_id" in st.secrets:
    AUTH0_CLIENT_ID = st.secrets["auth0_client_id"]
    AUTH0_CLIENT_SECRET = st.secrets["auth0_client_secret"]
    AUTH0_DOMAIN = st.secrets["auth0_domain"]
else:
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")