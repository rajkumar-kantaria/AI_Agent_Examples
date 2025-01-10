from fastapi import FastAPI, UploadFile, File
from services.confluence import extract_text_from_confluence
from services.embeddings import generate_ollama_embeddings
from services.question_answer import answer_question

app = FastAPI()

context_text = None
retriever = None

@app.post("/upload-confluence-doc/")
async def upload_confluence_doc(pageid: str):
    global context_text, retriever
    context_text = extract_text_from_confluence(pageid)
    retriever = generate_ollama_embeddings(context_text)
    return {"message": "Confluence document uploaded and processed successfully."}

@app.post("/ask-question/")
async def ask_question(question_data: dict):
    question = question_data.get("question")
    if not question:
        return {"error": "No question provided."}
    
    answer = answer_question(question, retriever)
    return {"answer": answer}
