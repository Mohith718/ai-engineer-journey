from langgraph.graph import StateGraph, END
from typing import TypedDict

class AState(TypedDict):
    target: int
    guess: int
    attempts: int
    result: str

def guess_node(state: AState):
    guesses = [10, 25, 47, 50]
    current_attempt = state["attempts"]
    guess = guesses[current_attempt]
    return {"guess": guess, "attempts": current_attempt + 1}

def check_node(state: AState):
    if state["guess"]==state["target"]:
        return {"result":"Found it!"}
    elif state["attempts"]>=4:
        return {"result":"Gave up after 4 tries."}
    else:
        return {"result":""}    
    
def route_check(state: AState):
    if state["result"] != "":
        return "done"
    else:
        return "retry"
    
graph=StateGraph(AState)
graph.add_node("guess_node",guess_node)
graph.add_node("check",check_node)  

graph.set_entry_point("guess_node")
graph.add_edge("guess_node","check")

graph.add_conditional_edges(
    "check",
    route_check,
    {
        "done":END,
        "retry":"guess_node"    
    }
)

graph.add_edge("check",END)
app=graph.compile()
result1 = app.invoke({"target": 47, "guess": 0, "attempts": 0, "result": ""})
print(result1)

result2 = app.invoke({"target": 99, "guess": 0, "attempts": 0, "result": ""})
print(result2)