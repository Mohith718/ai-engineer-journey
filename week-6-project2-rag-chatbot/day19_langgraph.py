from langgraph.graph import StateGraph, END
from typing import TypedDict

# ------------- 1 -----------
class AgentState(TypedDict):
    messages: list
    result: str

def greet_node(state: AgentState):
    return {"result": f"Hello! You have {len(state['messages'])} messages."}

def farewell_node(state: AgentState):
    return {"result": state["result"] + " Goodbye!"}

graph = StateGraph(AgentState)
graph.add_node("greet", greet_node)
graph.add_node("farewell", farewell_node)

graph.set_entry_point("greet")
graph.add_edge("greet", "farewell")
graph.add_edge("farewell", END)

app = graph.compile()
result = app.invoke({"messages": ["hi", "how are you"], "result": ""})
print(result)

# ------------- 2 -----------

class AState(TypedDict):
    company_name: str
    scores: int
    decision: str

def score_node(state: AState):
    scores = {
        "Redsage": 85,
        "Fractal": 45,
        "Deccan AI": 92,
        "TCS": 60
    }
    return {"scores":scores.get(state["company_name"], 0)}

def decide_node(state: AState):
    return {"decision":"hot_lead" if state["scores"]>=70 else "cold_lead"}

graph=StateGraph(AState)
graph.add_node("score",score_node)
graph.add_node("decision",decide_node)

graph.set_entry_point("score")
graph.add_edge("score","decision")
graph.add_edge("decision",END)

app=graph.compile()
result=app.invoke({"company_name":"Deccan AI","scores":"","decision":""})
print(result)