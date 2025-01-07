import streamlit as st
import requests
import uuid

BACKEND_URL = "http://localhost:8000"

# Generate a unique user ID for this session
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())

st.title("Context aware Chatbot")
st.markdown("""
This chatbot uses Groq's powerful Mixtral model to have natural conversations while maintaining context across messages. 
Ask any question and get detailed, helpful responses!
""")

# Initialize chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("What is your question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get streaming response from backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Make streaming request
        with requests.post(
            f"{BACKEND_URL}/ask-question",
            json={"question": prompt},
            params={"session_id": st.session_state["user_id"]},
            stream=True
        ) as response:
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
                    if chunk:
                        full_response += chunk
                        message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error("Failed to get response from the chatbot.")
