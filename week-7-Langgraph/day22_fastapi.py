from fastapi import FastAPI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello from FastAPI!"}

@app.get("/score/{company_name}")
def get_score(company_name: str):
    scores = {
        "Redsage": 85,
        "Fractal": 45,
        "Deccan AI": 92,
        "TCS": 60
    }
    score = scores.get(company_name, "Not found")
    return {"company": company_name, "score": score}
from pydantic import BaseModel
class CompanyInput(BaseModel):
    description: str

@app.post("/analyze")
def analyze_company(data: CompanyInput):
    count=len(data.description.split())
    exist="AI" in data.description
    return {
        "description":data.description,
        "word_count": count,
        "has_ai": exist
        }
class QuestionInput(BaseModel):
    question: str
@app.post("/ask")
def ask(data: QuestionInput):
    llm=ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model="llama-3.3-70b-versatile"
    )
    prompt=ChatPromptTemplate.from_messages([
        ("system","you are a helpful bot that could answer to every question user asks only in JSON format..."),
        ("user","question {question}\n\n")
    ])
    chain=prompt|llm
    response=chain.invoke({"question":data.question})
    return {"question": data.question, "answer": response.content}