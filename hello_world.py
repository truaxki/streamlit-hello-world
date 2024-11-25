"""The purpose of this file is to create a simple hello world program to test the streamlit community cloud."""

import streamlit as st
from anthropic import Anthropic

# Set page config
st.set_page_config(
    page_title="Hello World",
    page_icon="👋"
)

# Access the API key securely
anthropic = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])

# Main title
st.title("Hello World! 👋")

# Add some interactive elements
name = st.text_input("What's your name?", "World")
st.write(f"Hello {name}!")

# Add a simple counter
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button('Click me!'):
    st.session_state.count += 1

st.write(f'Button clicked {st.session_state.count} times')
