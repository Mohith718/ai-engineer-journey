from dotenv import load_dotenv
import os
from groq import Groq



# api_key = os.getenv("GROQ_API_KEY")

# client = Groq(api_key=api_key)

# response = client.chat.completions.create(
#     model="llama-3.3-70b-versatile",
#     messages=[
#         {"role": "user", "content": "Give me 3 business ideas for a small shop in Hyderabad"}
#     ]
# )

# result = response.choices[0].message.content

# print(result)

class LLMClient:
    def __init__(self,model):
        load_dotenv()
        api_key=os.getenv("GROQ_API_KEY")
        self.client=Groq(api_key=api_key)
        self.model=model
        
    def ask(self,question):
        response=self.client.chat.completions.create(
        model=self.model,
        messages=[{
            "role":"user",
            "content":question
            }]
        )
        return response.choices[0].message.content
    def ask_with_system(self,system,prompt):
        response=self.client.chat.completions.create(
        model=self.model,
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":prompt}
            ]
        )
        return response.choices[0].message.content
    def chat(self,message):
        response=self.client.chat.completions.create(
        model=self.model,
        messages=message
        )
        return response.choices[0].message.content
llm = LLMClient("llama-3.3-70b-versatile")
print(llm.ask("What is RAG in 2 lines?"))
print(llm.ask_with_system("You are an AI engineering tutor", "What is RAG in 2 sentences?"))
conversation = [
    {"role": "system", "content": "You are an AI engineering tutor"},
    {"role": "user", "content": "What is RAG?"},
    {"role": "assistant", "content": "RAG stands for Retrieval-Augmented Generation..."},
    {"role": "user", "content": "What vector databases can I use for it?"}
]
print(llm.chat(conversation))
