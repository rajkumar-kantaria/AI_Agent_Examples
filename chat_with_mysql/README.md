# Chat with MySQL

This project demonstrates an AI-powered chat interface for interacting with MySQL databases using CrewAI. It allows you to query and analyze MySQL databases using natural language.

## Setup Instructions

### 1. Prerequisites

1. MySQL Server must be installed and running on your system
2. (Optional) Import sample database if you want to test with example data:
   ```
   mysql -u your_username -p < database/Chinook_MySql.sql
   ```

### 2. Create Required Account

1. Create a [Groq](https://console.groq.com) account to get API access for the LLM

### 3. Environment Setup

Create a `.env` file in the root folder with the following variables:

- `GROQ_API_KEY`: Your Groq API key

### 4. Install Dependencies

#### Using Conda (Recommended)

1. Create a new conda environment:
   ```
   conda create -n mysql_chat python=3.12
   ```

2. Activate conda environment:
   ```
   conda activate mysql_chat
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### 5. Run the Application

1. Start the backend API server:
   ```
   uvicorn main:app --reload
   ```

2. In a separate terminal, run the frontend application:
   ```
   streamlit run app.py
   ```