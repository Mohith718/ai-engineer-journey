# from day7_llm_apis import LLMClient
# import os
# from groq import Groq
# from dotenv import load_dotenv
# import json

# load_dotenv()
# def calculate(expression):
#     """Evaluates a math expression"""
#     try:
#         result = eval(expression)
#         return str(result)
#     except:
#         return "Error: invalid expression"

# def get_lead_score(company_name):
#     """Looks up a company's lead score"""
#     scores = {
#         "Redsage": 85,
#         "Fractal": 45,
#         "Deccan AI": 92,
#         "TCS": 60
#     }
#     return str(scores.get(company_name, "Company not found"))
# tools = [
#     {
#         "type": "function",
#         "function": {
#             "name": "calculate",
#             "description": "Evaluates a math expression. Use this when the user asks for calculations.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "expression": {
#                         "type": "string",
#                         "description": "The math expression to evaluate, e.g. '25 * 4'"
#                     }
#                 },
#                 "required": ["expression"]
#             }
#         }
#     },
#     {
#         "type": "function",
#         "function": {
#             "name": "get_lead_score",
#             "description": "Looks up a company's lead score from the CRM database. Use this when asked about a company's score.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "company_name": {
#                         "type": "string",
#                         "description": "The name of the company to look up"
#                     }
#                 },
#                 "required": ["company_name"]
#             }
#         }
#     }
# ]

# client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[{"role": "user", "content": "What is Deccan AI's lead score?"}],
#     tools=tools,
#     tool_choice="auto"
# )

# message = response.choices[0].message

# if message.tool_calls:
#     tool_call = message.tool_calls[0]
#     function_name = tool_call.function.name
#     arguments = json.loads(tool_call.function.arguments)
    
#     print(f"LLM wants to call: {function_name}")
#     print(f"With arguments: {arguments}")
    
#     # Execute the function
#     if function_name == "calculate":
#         result = calculate(arguments["expression"])
#     elif function_name == "get_lead_score":
#         result = get_lead_score(arguments["company_name"])
    
#     print(f"Function returned: {result}")

# # Send the result back to the LLM
#     follow_up = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",
#         messages=[
#             {"role": "user", "content": "What is Deccan AI's lead score?"},
#             message,
#             {"role": "tool", "content": result, "tool_call_id": tool_call.id}
#         ]
#     )
    
#     print(f"Final answer: {follow_up.choices[0].message.content}")

from day7_llm_apis import LLMClient
from groq import Groq
from dotenv import load_dotenv
import os
import json

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
class ToolAgent:
    def __init__(self):
        load_dotenv()
        api_key=os.getenv("GROQ_API_KEY")
        self.client=Groq(api_key=api_key)
        self.model="llama-3.3-70b-versatile"
        self.tools=tools
        self.available_functions = {
                "calculate": calculate,
                "get_lead_score": get_lead_score
            } 
    def ask(self, question):

    # STEP 1: Ask LLM, give it the tools list
        response = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": question}],
        tools=self.tools,
        tool_choice="auto"
        )
        message = response.choices[0].message
    # STEP 2: Check — did LLM ask for a tool?
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name          # "calculate"
            arguments = json.loads(tool_call.function.arguments)
            func = self.available_functions[function_name]    # gets the actual function
            result = func(**arguments)
            follow_up = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": question},
                message,
                {"role": "tool", "content": result, "tool_call_id": tool_call.id}
            ]
        )
            return follow_up.choices[0].message.content
        else:
        # NO tool — LLM answered directly
            return message.content
agent = ToolAgent()
print(agent.ask("What is 999 * 77?"))
print(agent.ask("What is IBM's lead score?"))
print(agent.ask("What is the capital of India?"))
