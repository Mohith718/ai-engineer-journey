from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from support_agent import app as graph_app, Ticketstate

api = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
class TicketInput(BaseModel):
    ticket_text: str

@api.post("/ticket")

# ... your existing api = FastAPI() and CORS middleware stay exactly as they are


def process_ticket(data: TicketInput):
    initial_state = {
        "ticket_text": data.ticket_text,
        "category": "", "urgency": "", "sentiment": "",
        "retrieved_context": "", "resolution_type": "", "response_text": "",
        "assigned_team": "", "final_output": ""
    }
    result = graph_app.invoke(initial_state)
    return result

api.mount("/", StaticFiles(directory=".", html=True), name="static")