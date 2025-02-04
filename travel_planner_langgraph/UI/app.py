import streamlit as st
import requests
import time
import pdfkit

st.title("VoyageAI - AI-powered seamless travel planning")

if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.thread_id = None
    st.session_state.final_itinerary = None

def call_chat_api(message):
    url = "http://localhost:8000/chat"
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "message": message
    }
    
    if st.session_state.thread_id:
        payload["thread_id"] = st.session_state.thread_id
        
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    print("data:", data)
    
    if not st.session_state.thread_id and "thread_id" in data:
        st.session_state.thread_id = data["thread_id"]
    elif "thread_id" not in data:
        print(data["message"])
        st.session_state.final_itinerary = data["message"]
        st.rerun()
        
    return data["message"]

def export_to_pdf():
    if st.session_state.thread_id:
        try:
            response = requests.get(
                f"http://localhost:8000/download-pdf/{st.session_state.thread_id}",
                stream=True
            )
            if response.status_code == 200:
                return response.content
            else:
                st.error("Failed to generate PDF. Please try again.")
                return None
        except requests.RequestException as e:
            st.error(f"Error downloading PDF: {str(e)}")
            return None
    else:
        st.error("No thread ID available. Cannot generate PDF.")
        return None

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if st.session_state.final_itinerary:
    with st.chat_message("assistant"):
        st.write(st.session_state.final_itinerary)
else:
    if prompt := st.chat_input("Provide your details to get started"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            dots = ""
            for _ in range(3):
                dots += "."
                message_placeholder.write(f"Processing{dots}")
                time.sleep(0.3)
                
            ai_response = call_chat_api(prompt)
            message_placeholder.write(ai_response)

        st.session_state.messages.append({"role": "assistant", "content": ai_response})