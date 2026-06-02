from google import genai
from groq import Groq
import os
from dotenv import load_dotenv
import chromadb

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chroma_client=chromadb.Client()
collection=chroma_client.create_collection(name="test")
def load_pdf(filepath):
    with open(filepath,"r") as f:
        data=f.read()
    return data
def chunk_text(pagetext,chunk_size=500,overlap=50):
    start=0
    chunks=[]
    while start<len(pagetext):
        chunk=pagetext[start:start+chunk_size]
        chunks.append(chunk)
        start+=chunk_size-overlap
    return chunks
def get_embeddings(chunks):
    result=client.models.embed_content(
        model="gemini-embedding-001",
        contents=chunks
    )
    return result.embeddings[0].values
def storeembed(filepath):
    text=load_pdf(filepath)
    chunks=chunk_text(text)
    for i,chunk in enumerate(chunks):
        embeding=get_embeddings(chunk)
        collection.add(
            ids=[f"ids-{i}"],
            embeddings=[embeding],
            documents=[chunk]
        )
    return collection
def search(query, collection):
    embd=get_embeddings(query)
    result=collection.query(
        query_embeddings=[embd],
        n_results=3
    )
    doc= result["documents"][0]
    context = "\n".join(doc)
    return context
class bot:
    def __init__(self,system_prompt):
        api_key=os.getenv("GROQ_API_KEY")
        self.client=Groq(api_key=api_key)
        self.system_prompt = system_prompt
        self.history = [{"role": "system", "content": self.system_prompt}]
    def rag_answer(self,question, collection):
        chunktext=search(question,collection)
        self.history.append({"role": "user", "content": question})
        response=self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.history + [
            {"role": "user", "content": f"Context:\n{chunktext}\n\nQuestion: {question}"}
        ]
        )
        answer = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": answer})
        return answer
    def show_history(self):
        for i in self.history:
            print(i)
    def reset(self):
        self.history = [{"role": "system", "content": self.system_prompt}]

chatbot=bot("You are a helpful AI assistant that answers questions based only on the provided context. If the answer is not found in the context, say 'I don't have enough information in the document to answer this.' Be concise and accurate. Always ground your answers in the context provided.")
filepath="LLM_Interview_Questions.pdf"
collection = storeembed("ai_knowledge.txt")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    elif user_input.lower() == "history":
        chatbot.show_history()
    elif user_input.lower() == "reset":
        chatbot.reset()
        print("Chat reset.\n")
    else:
        response = chatbot.rag_answer(user_input,collection)
        print(f"AI: {response}\n")
