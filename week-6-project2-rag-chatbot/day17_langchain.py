from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

loader = PyPDFLoader("LLM Interview Questions.pdf")
documents = loader.load()
print(f"Pages loaded: {len(documents)}")
print(f"First page preview: {documents[0].page_content[:200]}")
print(f"Metadata: {documents[0].metadata}")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)
print(f"\nTotal chunks: {len(chunks)}")
print(f"First chunk: {chunks[0].page_content[:200]}")

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

response = llm.invoke("What is RAG in AI? Answer in 2 sentences.")
print(response.content)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI engineering tutor. Be concise."),
    ("user", "Explain {topic} in {num_sentences} sentences.")
])

chain = prompt | llm

response = chain.invoke({"topic": "embeddings", "num_sentences": "3"})
print(response.content)

response = chain.invoke({"topic": "vector databases", "num_sentences": "2"})
print(response.content)

embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="models/gemini-embedding-001"
)
vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
results = retriever.invoke("What is tokenization?")
for doc in results:
    print(f"Page {doc.metadata['page']}: {doc.page_content[:100]}...")
    print()

rag_prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer questions based only on the provided context. If the answer is not in the context, say you don't have enough information."),
    ("user", "Context:\n{context}\n\nQuestion: {question}")
])

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | rag_prompt
    | llm
    | StrOutputParser()
)

answer = rag_chain.invoke("What is tokenization and why is it important?")
print(answer)
