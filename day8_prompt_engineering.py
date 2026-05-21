from day7_llm_apis import LLMClient
import json

def analyze_lead(llm, description):
    prompt = f"""Analyze this company for B2B sales potential.
Respond ONLY in valid JSON, no markdown, no explanation.
Use this exact structure:
{{"company_summary": "one line summary", "industry": "sector", "score": 1-100, "reason": "why this score"}}

Company: {description}"""
    
    response = llm.ask(prompt)
    return json.loads(response)
llm = LLMClient("llama-3.3-70b-versatile")
result = analyze_lead(llm, "Redsage is a Hyderabad startup building AI-powered CRM tools for small businesses")
print(result)
print(f"Score: {result['score']}")

def score_leads(llm,desc):
    lit=[]
    for i in desc:
        result = analyze_lead(llm, i)
        if result["score"] >= 70:
            lit.append(result)
    return lit
def generate_outreach_email(llm,lead):
    question = f"Write a short personalized B2B outreach email for a company: {lead['company_summary']} in the {lead['industry']} industry."
    respond=llm.ask_with_system("You are a B2B sales specialist",question)

    return respond
def safe_parse_json(llm_response):
    try:
        return json.loads(llm_response)
    except Exception:
        try:
            start = llm_response.find("{")
            end = llm_response.rfind("}")
            print(f"start: {start}, end: {end}")
            print(f"extracted: {llm_response[start:end+1]}")
            json_str = llm_response[start:end+1]
            return json.loads(json_str)
        except Exception:
            try:
                text=json.loads(llm_response)
                start=text.find("{")
                end=text.rfind("}")
                json_str=text[start:end+1]
                return json.loads(json_str)
            except Exception:
                return {"error": "Failed to parse", "raw": llm_response}
companies = [
    "Redsage builds AI-powered CRM tools for small businesses in India",
    "Chennai Tiffins delivers homemade breakfast in Chennai, no tech involved",
    "Deccan AI builds RAG pipelines and LLM agents for enterprise clients"
]
llm = LLMClient("llama-3.3-70b-versatile")
hot = score_leads(llm, companies)
for lead in hot:
    print(f"--- Email for {lead['company_summary']} ---")
    email = generate_outreach_email(llm, lead)
    print(email)
    print()

for lead in hot:
    print(f"{lead['company_summary']} — Score: {lead['score']}")
clean = '{"name": "Redsage", "score": 80}'
messy = 'Here is the analysis: {"name": "Redsage", "score": 80} Hope this helps!'
broken = 'Sorry, I cannot analyze this company.'

print(safe_parse_json(clean))
print(safe_parse_json(messy))
print(safe_parse_json(broken))