# AI Agents Repository

This repository contains various AI Agents built using different LLM models and agentic frameworks.

## Available Agents

### 1. [PDF RAG Agent](pdf_rag_example/)
A Retrieval Augmented Generation (RAG) system that allows users to:
- Upload PDF documents
- Index their content using embeddings
- Ask questions about the documents using Groq LLM
- Get accurate answers based on the document context

### 2. [Simple Chatbot](simple_chatbot/)
A conversational AI chatbot that:
- Uses Groq's Mixtral model for natural language interactions
- Maintains conversation context across multiple messages
- Provides a clean web interface for chatting
- Automatically summarizes long conversations to stay within context window

### 3. [CONFLUENCE RAG Agent](confluence_rag_example/)
A conversational AI chatbot that:
- Uses Groq's model for natural language interactions
- Provides ability to train the model on Confluence page content
- Ask questions about the page content
- Get the answer based on the context
