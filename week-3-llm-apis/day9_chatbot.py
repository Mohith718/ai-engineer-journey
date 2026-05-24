from day7_llm_apis import LLMClient
import json

class Chatbot:
    def __init__(self,system_prompt):
        self.system_prompt = system_prompt
        self.llm=LLMClient("llama-3.3-70b-versatile")
        self.history = [{"role": "system", "content": system_prompt}]
    def send(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        answer=self.llm.chat(self.history)
        self.history.append({"role": "assistant", "content": answer})
        return answer
    def show_history(self):
        for i in self.history:
            print(i)
    def reset(self):
        self.history = [{"role": "system", "content": self.system_prompt}]
bot = Chatbot("You are an AI engineering tutor who gives concise answers")

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
