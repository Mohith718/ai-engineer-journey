from groq import Groq
from dotenv import load_dotenv
import os


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Explain RAG in AI engineering in 5 sentences"}],
    stream=True
)

# for chunk in response:
#     content = chunk.choices[0].delta.content
#     if content:
#         print(content, end="", flush=True)
# print()

system_prompt = """You are a lead qualification assistant for an AI consulting company.

RULES:
- Always respond in valid JSON format
- Never use markdown
- Score leads from 1-100
- If the company has no tech focus, score below 30
- If asked about anything other than lead qualification, respond with: {"error": "I only handle lead qualification"}

RESPONSE FORMAT:
{"company": "name", "score": number, "qualified": true/false, "reason": "one line"}
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What is the weather today?"}
    ]
)
# print(response.choices[0].message.content)
def count_tokens_approx(messages):
    total = 0
    for msg in messages:
        total += len(msg["content"].split())
    return total

# Test
history = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is RAG in AI?"},
    {"role": "assistant", "content": "RAG stands for Retrieval-Augmented Generation. It combines retrieval and generation to produce accurate responses grounded in external knowledge."}
]
# print(f"Approximate tokens: {count_tokens_approx(history)}")

def trim_history(history, max_tokens=500):
    """Keep system message + most recent messages that fit within max_tokens"""
    if count_tokens_approx(history) <= max_tokens:
        return history
    
    system_msg = history[0]
    trimmed = [system_msg]
    
    # Start from the most recent messages and work backwards
    recent = history[1:]
    recent.reverse()
    
    kept = []
    token_count = count_tokens_approx([system_msg])
    
    for msg in recent:
        msg_tokens = len(msg["content"].split())
        if token_count + msg_tokens <= max_tokens:
            kept.append(msg)
            token_count += msg_tokens
        else:
            break
    
    kept.reverse()
    return [system_msg] + kept

# Build a long history
long_history = [{"role": "system", "content": "You are helpful"}]
for i in range(20):
    long_history.append({"role": "user", "content": f"This is message number {i} with some extra words to fill space"})
    long_history.append({"role": "assistant", "content": f"Response to message {i} with additional context and detail"})

print(f"Before trim: {len(long_history)} messages, ~{count_tokens_approx(long_history)} tokens")
trimmed = trim_history(long_history, max_tokens=100)
print(f"After trim: {len(trimmed)} messages, ~{count_tokens_approx(trimmed)} tokens")