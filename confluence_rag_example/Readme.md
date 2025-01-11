# CONFLUENCE RAG Example

This project demonstrates a RAG (Retrieval Augmented Generation) system using Confluence store. It allows you to specify confluence page number, index their content, and ask questions about them.

## Setup Instructions

### 1. Create Required Accounts

1. Create a [Groq](https://console.groq.com) account to get API access for the LLM
2. Create a [Pinecone](https://www.pinecone.io/) account to use as the vector database store

### 2. Environment Setup

Create a `.env` file in the root folder with the following variables:

- `PINECONE_API_KEY`: Your Pinecone API key
- `GROQ_API_KEY`: Your Groq API key
- `CONFLUENCE_URL`: Base URL of the confluence server
- `CONFLUENCE_TOKEN`: Confluence API token

### 3. Install Dependencies

#### Using Conda (Recommended)

1. Create a new conda environment:
   ```
   conda create -n <env name>
   ```

2. Activate conda environment:
   ```
   conda activate <env name>
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### 4. Run the Application

1. Start the backend API server:
   ```
   uvicorn main:app --reload
   ```

2. In a separate terminal, run the frontend application:
   ```
   streamlit run app.py
   ```



