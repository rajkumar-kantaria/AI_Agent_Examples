from langchain_groq import ChatGroq
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

load_dotenv()

app = FastAPI()

llm = ChatGroq(
    temperature=0,
    model_name="mixtral-8x7b-32768"
)

store = {}

def get_chat_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    history = store[session_id]
    
    # Keep only a summary of the conversation
    if len(history.messages) > 4:
        # Create a summary prompt
        summary_prompt = "\n".join([f"{msg.type}: {msg.content}" for msg in history.messages])
        summary_request = f"Summarize this conversation briefly:\n{summary_prompt}"
        
        # Get summary from LLM
        summary = llm.invoke(summary_request).content
        
        # Reset history with just the summary
        history.clear()
        history.add_ai_message(f"Previous conversation summary: {summary}")
    
    return history

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_chat_history,
    input_messages_key="input",
    history_messages_key="history"
)

async def generate(question: str, session_id: str):
        async for chunk in chain_with_history.astream(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        ):
            yield chunk.content

@app.post("/ask-question")
async def ask_question(question_data: dict, session_id: str):
    question = question_data.get("question")
    if not question:
        return {"error": "No question provided."}
    
    return StreamingResponse(generate(question, session_id), media_type="text/event-stream")
