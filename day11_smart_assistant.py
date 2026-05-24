import os
import json
from dotenv import load_dotenv
from day7_llm_apis import LLMClient
from groq import Groq

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluates a math expression. Use this when the user asks for calculations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate, e.g. '25 * 4'"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_lead_score",
            "description": "Looks up a company's lead score from the CRM database. Use this when asked about a company's score.",
            "parameters": {
                "type": "object",
                "properties": {
                    "company_name": {
                        "type": "string",
                        "description": "The name of the company to look up"
                    }
                },
                "required": ["company_name"]
            }
        }
    }
]

def calculate(expression):
    try:
        result= eval(expression)
        return str(result)
    except:
        return "Error: got error"
def get_lead_score(company_name):
    scores = {
        "Deccon": 70,
        "infosys": 96,
        "IBM": 65,
        "Wipro": 85
    }
    return str(scores.get(company_name, "Company not found"))
class SmartAssistant:
    def __init__(self,system_prompt):
        load_dotenv()
        api_key=os.getenv("GROQ_API_KEY")
        self.client=Groq(api_key=api_key)
        self.tools=tools
        self.system_prompt=system_prompt
        self.available_tools={
            "calculate": calculate,
            "get_lead_score": get_lead_score
        }
        self.history=[{"role": "system", "content": system_prompt}]
        
    def send(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        # answer=self.llm.chat(self.history)
        response=self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=self.history,
            tools=self.tools,
            tool_choice="auto"
        )
        answer=response.choices[0].message
        if answer.tool_calls:
            tool_call = answer.tool_calls[0]
            function_name = tool_call.function.name          # "calculate"
            arguments = json.loads(tool_call.function.arguments)
            func = self.available_tools[function_name]    # gets the actual function
            result = func(**arguments)
            follow_up = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": user_message},
                answer,
                {"role": "tool", "content": result, "tool_call_id": tool_call.id}
            ]
        )
            answer= follow_up.choices[0].message.content
            self.history.append({"role": "assistant", "content": answer})
            return answer
        else:
            final_answer = answer.content
            self.history.append({"role": "assistant", "content": final_answer})
            return final_answer
    def show_history(self):
        for i in self.history:
            print(i)
    def reset(self):
        self.history = [{"role": "system", "content": self.system_prompt}]

bot=SmartAssistant("You are a smart AI assistant. You can answer questions, do math calculations, and look up company lead scores. Be concise and helpful.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    elif user_input.lower() == "history":
        bot.show_history()
    elif user_input.lower() == "reset":
        bot.reset()
        print("Chat reset.\n")
    else:
        response = bot.send(user_input)
        print(f"AI: {response}\n")