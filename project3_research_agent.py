from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import TypedDict
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os

load_dotenv()
llm=ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile",
    )
search_tool = TavilySearch(max_results=3, tavily_api_key=os.getenv("TAVILY_API_KEY"))

def format_search_results(results):
    formatted = []
    for r in results["results"]:
        formatted.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {r['content']}")
    return "\n\n".join(formatted)

class ResearchState(TypedDict):
    topic: str
    search_results: str
    attempts: int
    report: str
    grade: str

def search_node(state: ResearchState):
    current_attempt=state["attempts"]
    results=search_tool.invoke({"query": state["topic"]})
    search_results=format_search_results(results)
    return {"search_results":search_results,"attempts": current_attempt+1}

def grade_node(state: ResearchState):
    prompt=ChatPromptTemplate.from_messages([
    ("system","you are bot that checks wether Is this enough information to write a good report on the topic? and answers in one word like"
    "'Sufficient' or 'Not Sufficient'"),
    ("user", "Topic: {topic}\n\nSearch Results:\n{search_results}")
    ])
    chain=prompt|llm
    response=chain.invoke({
        "topic":state["topic"],
        "search_results":state["search_results"]
    })
    return {"grade":response.content.strip().lower()}

def generate_node(state: ResearchState):
    prompt=ChatPromptTemplate.from_messages([
    ("system", """You are a research report writer. Based on the search results provided, write a structured report with EXACTLY these four sections:

1. Executive Summary - 2-3 sentences summarizing the key takeaway
2. Key Findings - the main discoveries and information found
3. Analysis - what these findings mean and why they matter
4. References - list all source URLs from the search results

Do not add any other sections. Follow this structure exactly."""),
    ("user", "Topic: {topic}\n\nSearch Results:\n{search_results}")
    ])
    chain=prompt|llm
    response=chain.invoke({
        "topic":state["topic"],
        "search_results":state["search_results"]
    })
    return {"report":response.content}

def route_after_grade(state: ResearchState):
    if state["grade"]=="sufficient" or state["attempts"]>=3:
        return "generate"
    else:
        return "retry"
    
graph=StateGraph(ResearchState)
graph.add_node("search",search_node)
graph.add_node("grade",grade_node)
graph.add_node("generate",generate_node)

graph.set_entry_point("search")
graph.add_edge("search","grade")
graph.add_conditional_edges(
    "grade",
    route_after_grade,
    {
        "generate":"generate",
        "retry":"search"
    }
)

graph.add_edge("generate",END)
app=graph.compile()
result = app.invoke({
    "topic": "How LangGraph is used to build AI agents",
    "search_results": "",
    "attempts": 0,
    "grade": "",
    "report": ""
})
result2 = app.invoke({
    "topic": "quantum computing breakthroughs this week",
    "search_results": "",
    "attempts": 0,
    "grade": "",
    "report": ""
})
print(f"Attempts: {result2['attempts']}")
print(f"Grade: {result2['grade']}")
print(result2["report"])
print(result["report"])