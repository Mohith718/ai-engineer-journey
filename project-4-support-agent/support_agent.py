from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)

class Ticketstate(TypedDict):
    ticket_text: str
    category: str
    urgency: str
    sentiment: str
    retrieved_context: str
    resolution_type: str
    response_text: str
    assigned_team: str
    final_output: str

def safe_parse_json(llm_response):
    try:
        return json.loads(llm_response)
    except Exception:
        try:
            start = llm_response.find("{")
            end = llm_response.rfind("}")
            json_str = llm_response[start:end+1]
            return json.loads(json_str)
        except Exception:
            return {"error": "Failed to parse", "raw": llm_response}
        
def classify_node(state: Ticketstate) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a support ticket classifier. Read the ticket and respond with ONLY valid JSON in this exact format, no markdown, no explanation:
{{"category": "billing" or "technical" or "security" or "account" or "feature_request", "urgency": "low" or "medium" or "high" or "critical", "sentiment": "frustrated" or "neutral" or "positive"}}"""),
        ("user", "Ticket: {ticket_text}")
    ])
    chain = prompt | llm
    response = chain.invoke({"ticket_text": state["ticket_text"]})
    parsed=safe_parse_json(response.content)
    return {
        "category": parsed.get("category", "unknown"),
        "urgency": parsed.get("urgency", "unknown"),
        "sentiment": parsed.get("sentiment", "unknown")
    }

loader = TextLoader("knowledge_base.txt")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

embeddings = GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="models/gemini-embedding-001"
)

vectorstore = Chroma.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

def retrieve_node(state: Ticketstate) -> str:
    results = retriever.invoke(state["ticket_text"])
    retrieved_context = "\n".join([doc.page_content for doc in results])
    return {"retrieved_context": retrieved_context}

def resolve_node(state: Ticketstate) -> str:
    prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a support ticket resolver. Read the ticket and the retrieved context. Decide if the context contains enough information to confidently answer this ticket automatically, or if it needs to go to a human agent.

Respond with ONLY valid JSON in this exact format, no markdown, no explanation:
{{"resolution_type": "auto_resolved" or "escalated", "response_text": "if auto_resolved, write the customer-facing answer using the context. if escalated, write a short internal note explaining why a human is needed"}}"""),
    ("user", "Ticket: {ticket_text}\nContext: {retrieved_context}")
])
    chain = prompt | llm
    response = chain.invoke({
        "ticket_text": state["ticket_text"],
        "retrieved_context": state["retrieved_context"]
    })
    parsed=safe_parse_json(response.content)
    return {
        "resolution_type": parsed.get("resolution_type", "unknown"),
        "response_text": parsed.get("response_text", "")
    }

def route_output_node(state: Ticketstate):
    team_map = {
        "billing": "Billing Team",
        "technical": "Technical Support",
        "security": "Security Team",
        "account": "Account Management",
        "feature_request": "Product Team"
    }
    
    if state["resolution_type"] == "auto_resolved":
        return {
            "assigned_team": "",
            "final_output": state["response_text"]
        }
    else:
        assigned_team = team_map.get(state["category"], "General Support")
        summary = f"[{state['urgency'].upper()} priority, customer sentiment: {state['sentiment']}] {state['response_text']}"
        return {
            "assigned_team": assigned_team,
            "final_output": summary
        }
    
graph = StateGraph(Ticketstate)
graph.add_node("classify", classify_node)
graph.add_node("retrieve", retrieve_node)
graph.add_node("resolve", resolve_node)
graph.add_node("route_output", route_output_node)

graph.set_entry_point("classify")
graph.add_edge("classify", "retrieve")
graph.add_edge("retrieve", "resolve")
graph.add_edge("resolve", "route_output")
graph.add_edge("route_output", END)
app = graph.compile()

if __name__ == "__main__":
    test_state = {
        "ticket_text": "I forgot my password, how do I reset it?",
        "category": "", "urgency": "", "sentiment": "",
        "retrieved_context": "", "resolution_type": "", "response_text": "",
        "assigned_team": "", "final_output": ""
    }
    result = app.invoke(test_state)
    print(result)
