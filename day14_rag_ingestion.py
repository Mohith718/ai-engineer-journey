from google import genai
import os
from dotenv import load_dotenv
import chromadb
import day13_embeddings as getword
from day7_llm_apis import LLMClient

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chroma_client=chromadb.Client()
collection=chroma_client.create_collection(name="testbase")
def load_document(filepath):
    with open(filepath,"r") as f:
        data=f.read()
        return data

def chunk_text(text, chunk_size=500, overlap=50):
    start=0
    chunks=[]
    while start < len(text):
        chunk=text[start:start+chunk_size]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks
def embed_and_store(chunks, collection):
    for i,chunk_text in enumerate(chunks):
        embd=getword.get_embedding(chunk_text)
        collection.add(
            ids=[f"chunk_{i}"], 
            embeddings=[embd],
            documents=[chunk_text]
        )   
def rag_query(question,collection,llm_client):
    embedding=getword.get_embedding(question)
    results=collection.query(
        query_embeddings=[embedding],
        n_results=3
    )
    docs = results["documents"][0]
    context = "\n".join(docs)
    response=llm_client.client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role":"system","content":"Answer questions based only on the provided context. If the answer is not in the context, say I don't have enough information."},
        {"role":"user","content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )
    return response.choices[0].message.content
llm_client=LLMClient("llama-3.3-70b-versatile")
text = load_document("ai_knowledge.txt")
chunks = chunk_text(text)
embed_and_store(chunks, collection)
print(f"Stored {collection.count()} chunks")
print(f"\nTotal chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1} ({len(chunk)} chars):")
    print(chunk[:100] + "...")
print(rag_query("What is RAG and why does it reduce hallucinations?", collection,llm_client))
print(rag_query("How do I deploy an AI application?", collection,llm_client))