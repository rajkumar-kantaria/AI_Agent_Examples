from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import OpenAI
from langchain.schema.runnable import RunnablePassthrough
from dotenv import load_dotenv
from .embeddings import get_retriever_from_index

load_dotenv()

PROMPT_TEMPLATE = """
### [INST] 
Answer the question based on the context provided. Do not answer or make up 
information if it is not within context. Say "I do not know the answer" if unsure.

<context>
{context}
</context>

### QUESTION:
{question}

[/INST]
"""

groq_llama3_llm = ChatGroq(
    temperature=0,
    model_name="llama3-8b-8192",
)

def answer_question(question: str, retriever) -> str:
    if not retriever:
        retriever = get_retriever_from_index()

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE,
    )
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()} 
        | prompt 
        | groq_llama3_llm
    )
    result = chain.invoke(question)
    return result.content
