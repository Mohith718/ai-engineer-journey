from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
import os

load_dotenv()
llm=ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

prompt=ChatPromptTemplate.from_messages([
    ("system","you are bot that answer every question that user asks.."),
    ("user","Explain\n\n {context} \n\n query {question}")
])

chain=prompt|llm

loader=TextLoader("ai_knowledge.txt")
doc=loader.load()

split=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
splitter=split.split_documents(doc)

embd=GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="models/gemini-embedding-001"
)
vector=Chroma.from_documents(splitter,embd)
ves=vector.as_retriever(search_kwargs={"k": 3})

result=ves.invoke("what is AI?")
for doc in result:
    print(f"Page {doc.metadata['source']}: {doc.page_content[:100]}...")
    print()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": ves | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnablePassthrough
import os

load_dotenv()
llm=ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

prompt=ChatPromptTemplate.from_messages([
    ("system","you are bot that answer every question that user asks.."),
    ("user","Explain\n\n {context} \n\n query {question}")
])

loader=TextLoader("ai_knowledge.txt")
doc=loader.load()

split=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
splitter=split.split_documents(doc)

embd=GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="models/gemini-embedding-001"
)
vector=Chroma.from_documents(splitter,embd)
ves=vector.as_retriever(search_kwargs={"k": 3})

result=ves.invoke("what is AI?")
for doc in result:
    print(f"Page {doc.metadata['source']}: {doc.page_content[:100]}...")
    print()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": ves | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
print(rag_chain.invoke("What is RAG?"))
print(rag_chain.invoke("How does FastAPI help AI engineers?"))
print(rag_chain.invoke("What are embeddings?"))