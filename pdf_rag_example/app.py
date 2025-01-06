import streamlit as st
import requests

# Backend API URL
API_BASE_URL = "http://127.0.0.1:8000"

st.title("AI Document Assistant")
st.write("Upload a PDF document to ask questions about its content.")

# Sidebar for document input
st.sidebar.header("Document Input")

# Store the upload status in session state
if "doc_uploaded" not in st.session_state:
    st.session_state.doc_uploaded = False

uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf", key="pdf_uploader")

# Only upload if file is selected and not already uploaded
if uploaded_file and not st.session_state.doc_uploaded:
    st.sidebar.write("Uploading...")
    files = {"file": uploaded_file}
    response = requests.post(f"{API_BASE_URL}/upload-pdf/", files=files)
    
    if response.status_code == 200:
        st.session_state.doc_uploaded = True
        st.sidebar.success("PDF uploaded successfully!")
    else:
        st.sidebar.error("Failed to upload PDF.")

# Main Interface for Question Answering
# if st.session_state.doc_uploaded:
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
