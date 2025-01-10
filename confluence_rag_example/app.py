import streamlit as st
import requests

# Backend API URL
API_BASE_URL = "http://127.0.0.1:8000"

st.title("AI Document Assistant")
st.write("Enter a Confluence page ID to ask questions about its content.")

# Sidebar for document input
st.sidebar.header("Document Input")

# Store the upload status in session state
if "doc_uploaded" not in st.session_state:
    st.session_state.doc_uploaded = False

page_id = st.sidebar.text_input("Enter Confluence Page ID")

# Only upload if page ID is entered and not already uploaded
if page_id and not st.session_state.doc_uploaded:
    st.sidebar.write("Processing...")
    response = requests.post(f"{API_BASE_URL}/upload-confluence-doc/", params={"pageid": page_id})
    
    if response.status_code == 200:
        st.session_state.doc_uploaded = True
        st.sidebar.success("Confluence page processed successfully!")
    else:
        st.sidebar.error("Failed to process Confluence page.")

# Main Interface for Question Answering
st.header("Ask a Question")
question = st.text_input("Enter your question")

if st.button("Get Answer"):
    if question.strip():
        processing_msg = st.empty()
        processing_msg.write("Processing...")

        payload = {"question": question}
        response = requests.post(f"{API_BASE_URL}/ask-question/", json=payload)
        
        processing_msg.empty()

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer found.")
            st.write(f"**Answer:** {answer}")
        else:
            st.error("Failed to fetch the answer.")
        
    else:
        st.warning("Please enter a question.")
