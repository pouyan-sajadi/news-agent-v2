import os
from dotenv import load_dotenv

try:
    import streamlit as st
    USE_STREAMLIT_SECRETS = True
except ImportError:
    USE_STREAMLIT_SECRETS = False

if not USE_STREAMLIT_SECRETS:
    load_dotenv()

def get_secret(key, default=None):
    if USE_STREAMLIT_SECRETS and key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)

# Usage
SERPAPI_KEY = get_secret("SERPAPI_KEY")
OPENAI_API_KEY = get_secret("OPENAI_API_KEY")
MODEL = "gpt-4.1-nano-2025-04-14"
#MODEL = "gpt-4.1-mini-2025-04-14"
NUM_SOURCES = 10