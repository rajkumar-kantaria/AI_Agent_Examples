import streamlit as st
import requests
import json

# Set page config
st.set_page_config(page_title="Chat with MySQL", layout="wide")

# Initialize session state for connection status
if 'connected' not in st.session_state:
    st.session_state.connected = False

# Sidebar for database connection
with st.sidebar:
    st.header("Database Connection")
    hostname = st.text_input("Hostname")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    database = st.text_input("Database")
    
    if st.button("Connect"):
        try:
            response = requests.post(
                "http://localhost:8000/connect",
                json={
                    "hostname": hostname,
                    "username": username,
                    "password": password,
                    "database": database
                }
            )
            if response.status_code == 200:
                st.success("Successfully connected to database!")
                st.session_state.connected = True
            else:
                st.error(f"Failed to connect: {response.json()['detail']}")
                st.session_state.connected = False
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.connected = False

# Main chat interface
st.title("Chat with MySQL")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your database"):
    if not st.session_state.connected:
        st.error("Please connect to a database first!")
    else:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get AI response
        try:
            response = requests.get(
                "http://localhost:8000/query",
                params={"question": prompt}
            )
            
            if response.status_code == 200:
                ai_response = response.json()
                # Add AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                with st.chat_message("assistant"):
                    st.markdown(ai_response)
            else:
                st.error(f"Error: {response.json()['detail']}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
