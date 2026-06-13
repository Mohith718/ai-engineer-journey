import os
import groq
import truststore
truststore.inject_into_ssl()

from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def calculate(expression: str) -> str:
    """Evaluates a math expression. Use this for any calculation."""
    try:
        return str(eval(expression))
    except:
        return "Error: invalid expression"

@tool
def get_lead_score(company_name:str) -> str:
    "Looks up a company's lead score from the CRM database. Use this when asked about a company's score."
    scores = {
        "Deccon": 70,
        "infosys": 96,
        "IBM": 65,
        "Wipro": 85,
        "Deccan AI": 92
    }
    return str(scores.get(company_name, "Company not found"))

loader=TextLoader("ai_knowledge.txt")
doc=loader.load()
split=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunk=split.split_documents(doc)
embd=GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="models/gemini-embedding-001"
)
vector=Chroma.from_documents(chunk,embd)
ret=vector.as_retriever(search_kwargs={"k":3})
@tool
def search_knowledge(query:str) -> str:
    """Searches the knowledge base for information. Use this when asked about AI topics."""
    result=ret.invoke(query)
    docs_text = "\n\n".join(doc.page_content[:200] for doc in result)
    return docs_text
llm=ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile",
    temperature=0,
    disable_streaming=True
)
from langchain_core.messages import HumanMessage, ToolMessage
tools = [calculate, get_lead_score, search_knowledge]
llm_with_tools = llm.bind_tools(tools)
llm_with_tools = llm.bind_tools(tools)

def run_agent(question):
    print(f"\n> Question: {question}")
    messages = [HumanMessage(content=question)]
    response = llm_with_tools.invoke(messages)
    
    if response.tool_calls:
        tool_map = {
            "calculate": calculate,
            "get_lead_score": get_lead_score,
            "search_knowledge": search_knowledge
        }
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            result = tool_map[tool_name].invoke(tool_args)
            print(f"Tool used: {tool_name} with args: {tool_args}")
            messages.append(response)
            messages.append(ToolMessage(content=str(result), tool_call_id=tool_call["id"]))
        
        final = llm_with_tools.invoke(messages)
        print(f"Answer: {final.content}")
    else:
        print(f"Answer: {response.content}")

run_agent("What is 999 * 77?")
run_agent("What is Deccan AI's lead score?")
run_agent("What does the document say about FastAPI?")
run_agent("What is 50 * 30 and also tell me about RAG from the document?")