from fastapi import FastAPI, UploadFile, File
from services.pdf import extract_text_from_pdf
from services.embeddings import generate_ollama_embeddings
from services.question_answer import answer_question

app = FastAPI()

context_text = None
retriever = None

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global context_text, retriever
    contents = await file.read()
    with open("uploaded.pdf", "wb") as f:
        f.write(contents)
    
    context_text = extract_text_from_pdf("uploaded.pdf")
    retriever = generate_ollama_embeddings(context_text)
    return {"message": "PDF uploaded and processed successfully."}

@app.post("/ask-question/")
async def ask_question(question_data: dict):
    question = question_data.get("question")
    if not question:
        return {"error": "No question provided."}
    
    answer = answer_question(question, retriever)
    return {"answer": answer}
