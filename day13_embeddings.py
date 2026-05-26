from google import genai
from dotenv import load_dotenv
import os
import chromadb

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="knowledge_base")
def get_embedding(text):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return response.embeddings[0].values

documents = [
    "RAG combines retrieval and generation to produce grounded AI responses",
    "LangChain is a framework for building LLM-powered applications",
    "Vector databases store embeddings for fast similarity search",
    "FastAPI is a Python web framework for building REST APIs",
    "Docker containers package applications for consistent deployment"
]

# Embed and store each document
for i, doc in enumerate(documents):
    embedding = get_embedding(doc)
    collection.add(
        ids=[f"doc_{i}"],
        embeddings=[embedding],
        documents=[doc]
    )

print(f"Stored {collection.count()} documents")

query = "How do I build apps with LLMs?"
query_embedding = get_embedding(query)

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

print(f"Query: {query}\n")
for i, doc in enumerate(results["documents"][0]):
    print(f"Result {i+1}: {doc}")

def cosine_similarity(vec1, vec2):
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a * a for a in vec1) ** 0.5
    magnitude2 = sum(b * b for b in vec2) ** 0.5
    return dot_product / (magnitude1 * magnitude2)

# Three sentences
emb1 = get_embedding("What is artificial intelligence?")
emb2 = get_embedding("Explain AI and machine learning")
emb3 = get_embedding("How to make butter chicken")

# Compare
print(f"AI vs AI (similar): {cosine_similarity(emb1, emb2):.4f}")
print(f"AI vs cooking (different): {cosine_similarity(emb1, emb3):.4f}")

embedding = get_embedding("What is artificial intelligence?")
print(f"Embedding length: {len(embedding)}")
print(f"First 5 numbers: {embedding[:5]}")

def search_knowledge(query,collection):
    embd=get_embedding(query)
    result=collection.query(
        query_embeddings=[embd],
        n_results=3
    )
    doc=[]
    for i,d in enumerate(result["documents"][0]):
        print(f"{i+1} - {d}")
        doc.append(d)
    return doc
search_knowledge("What is retrieval augmented generation?", collection)
search_knowledge("How do I deploy my Python app?", collection)
search_knowledge("What tools help me build AI agents?", collection)
    
    