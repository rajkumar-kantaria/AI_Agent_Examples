# Simple Chatbot

This project demonstrates a conversational AI chatbot powered by Groq's Mixtral model. It provides a clean web interface for having natural conversations with an AI assistant that maintains context across multiple messages.

## Setup Instructions

### 1. Create Required Accounts

1. Create a [Groq](https://console.groq.com) account to get API access for the LLM
2. Create a [Pinecone](https://www.pinecone.io/) account to use as the vector database store

### 2. Environment Setup

Create a `.env` file in the root folder with the following variables:

- `PINECONE_API_KEY`: Your Pinecone API key
- `GROQ_API_KEY`: Your Groq API key

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
   uvicorn backend:app --port 8000 --reload
   ```

2. In a separate terminal, run the frontend application:
   ```
   streamlit run app.py
   ```