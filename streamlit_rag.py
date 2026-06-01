import streamlit as st
from PyPDF2 import PdfReader
from google import genai
from groq import Groq
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()
chroma_client=chromadb.Client()
collection=chroma_client.get_or_create_collection(name="trap")
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def chunk_text(data,chunk_size=500,overlap=50):
    start=0
    chunks=[]
    while start<len(data):
        text=data[start:start+chunk_size]
        chunks.append(text)
        start+=chunk_size-overlap
    return chunks
def get_embedding(chunks):
    embedding=client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunks
    )
    return embedding.embeddings[0].values
st.title("PDF RAG Chatbot")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file and "collection" not in st.session_state:
    reader=PdfReader(uploaded_file)
    pages = ""
    for page in reader.pages:
        pages += page.extract_text()
    chunk=chunk_text(pages)
    for i,docs in enumerate(chunk):
        embedding=get_embedding(docs)
        result=collection.add(
            ids=[f"ids-{i}"],
            embeddings=[embedding],
            documents=[docs]
        )
    st.session_state.collection=collection
    st.success("PDF processed! Ask questions below.")
if "collection" in st.session_state:
    question = st.chat_input("Ask a question about the PDF")
    if question:
        embd = get_embedding(question)
        result=st.session_state.collection.query(
        query_embeddings=[embd],
        n_results=2
            )
        docs = result["documents"][0]
        context = "\n".join(docs)
        response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
        {"role": "system", "content": "Answer based only on the provided context."},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]
)
        answer = response.choices[0].message.content
        st.write(answer)