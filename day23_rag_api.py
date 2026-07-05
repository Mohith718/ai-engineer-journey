from fastapi import FastAPI, UploadFile, File
from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import BaseModel
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv()

app=FastAPI()

# def reader(data):
#     load=PyPDFLoader()
#     doc=load.load(data)
#     return doc

def splitter(doc,chunk_size=500,chunk_overlap=50):
    split=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunk=split.split_text(doc)
    return chunk

def embed(chunk):
    embeddings=GoogleGenerativeAIEmbeddings(
        google_api_key=os.getenv("GEMINI_API_KEY"),
        model="models/gemini-embedding-001"
    )
    vs=Chroma.from_texts(chunk,embeddings)
    ret=vs.as_retriever(search_kwargs={"k":3})
    return ret

def ask_llm(question,context):
    llm=ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile"
    )
    prompt=ChatPromptTemplate.from_messages([
        ("system","Answer the question based only on the provided context. Be direct and concise. Do not format as JSON, just answer in plain text."),
        ("user","question {question}\n\n context {context}")
    ])
    chain=prompt|llm
    response=chain.invoke({"question":question,"context":context})
    return response.content

@app.get("/")
def home():
    return {"messsage":"Welcome to chat_with_me"}

class upload(BaseModel):
    filename: str

retriever = None
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    "Processing PDF file"
    global retriever
    contents=await file.read()
    pdf_read=PdfReader(BytesIO(contents))
    text=""
    for page in pdf_read.pages:
        text+=page.extract_text()
    chunk=splitter(text)
    retriever=embed(chunk)
    return {"filename": file.filename, "chunks": len(chunk), "status": "processed"}

class query(BaseModel):
    question: str
@app.post("/ask")
def ask(data: query):
    if retriever is None:
        return {"error": "No PDF uploaded yet. Upload a PDF first."}
    docs = retriever.invoke(data.question)
    context = "\n\n".join(doc.page_content for doc in docs) if hasattr(docs[0], 'page_content') else "\n\n".join(docs)
    answer=ask_llm(data.question,context)
    return {"question": data.question, "answer": answer}
