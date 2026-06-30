from langgraph.graph import StateGraph,END
from typing import TypedDict

class AState(TypedDict):
    company_name: str
    score: int
    decision: str
    action: str

def score_node(state: AState):
    score={
        "Redsage": 85,
        "Fractal": 45,
        "Deccan AI": 92,
        "TCS": 60
    }
    return {"score":score.get(state["company_name"],0)}

def decision_node(state: AState):
    return {"decision":"hot_lead" if state["score"]>=70 else "cold_lead"}

def alert_sales_node(state: AState):
    return {"action":f"need action {state['company_name']}" }

def archive_node(state: AState):
    return {"action": f"{state['company_name']} is archived as it's cold lead"}

def route_decision(state: AState):
    if state["decision"] == "hot_lead":
        return "alert_sales"
    else:
        return "archive"
graph=StateGraph(AState)
graph.add_node("score",score_node)
graph.add_node("decision",decision_node)
graph.add_node("alert",alert_sales_node)
graph.add_node("archive",archive_node)

graph.set_entry_point("score")
graph.add_edge("score", "decision") 
graph.add_conditional_edges(
    "decision",
    route_decision,
    {
        "alert_sales": "alert",
        "archive": "archive"
    }
)
graph.add_edge("alert",END)
graph.add_edge("archive", END)

app=graph.compile()
result=app.invoke({"company_name": "Deccan AI", "score": 0, "decision": "", "action": ""})
print(result)

result2 = app.invoke({"company_name": "Fractal", "score": 0, "decision": "", "action": ""})
print(result2)
