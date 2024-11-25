"""The purpose of this file is to create a simple hello world program to test the streamlit community cloud."""

import streamlit as st
from anthropic import Anthropic

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == st.secrets["PASSWORD"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        return False
    return st.session_state["password_correct"]

def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_system_prompt():
    return """You are Admiral Ackbar, a Mon Calamari naval officer known for your leadership and expertise in navigating complex administrative tasks. 
    Your communication style should:
    - Use nautical phrases and exclamations ("Arrgh!", "Batten down the hatches!", "Set a course!")
    - Maintain a gruff but friendly tone, befitting a veteran officer
    - Address users as "sailor" or by their rank
    - Reference proper naval terminology and protocols
    - React dramatically to bureaucratic challenges with phrases like "It's a trap!"
    - Stay in character while being helpful and informative
    - Pepper responses with Star Wars naval references when appropriate
    
    While maintaining this persona, your primary goal is to be helpful and clear in your responses. Never break character, but ensure the information you provide is accurate and useful."""

def main():
    st.title("Admiral Ackbar's Administrative Assistant")
    st.markdown("*'It's not a trap, it's just paperwork!'*")
    
    with st.sidebar:
        temperature = st.slider(
            "Creativity Level",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher values make the Admiral more creative but less predictable"
        )
    
    init_chat_history()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    if prompt := st.chat_input("Request assistance from Admiral Ackbar..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Create a streaming response
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=temperature,
                system=get_system_prompt(),
                messages=[
                    {"role": m["role"], "content": m["content"]} 
                    for m in st.session_state.messages
                ],
                stream=True
            )
            
            # Process the stream
            for chunk in message:
                # Skip non-content events
                if hasattr(chunk, 'type') and chunk.type == 'content_block_start':
                    continue
                
                if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                    full_response += chunk.delta.text
                    message_placeholder.markdown(full_response + "▌")
            
            # Final update without the cursor
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if check_password():
    main()
else:
    st.stop()
