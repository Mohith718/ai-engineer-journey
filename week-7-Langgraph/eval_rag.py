from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma

load_dotenv()
llm=ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama-3.3-70b-versatile"
)
prompt=ChatPromptTemplate.from_messages([
    ("system", "Answer questions based only on the provided context. Be concise and accurate."),
    ("user","Context:\n{context}\n\nQuestion: {question}")
])
chain=prompt|llm

doc=PyPDFLoader("LLM Interview Questions.pdf")
load=doc.load()
#    return load


spliter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
chunk=spliter.split_documents(load)
    # return chunk

chunks=GoogleGenerativeAIEmbeddings(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model="models/gemini-embedding-001"
)

vs=Chroma.from_documents(chunk,chunks)
ret=vs.as_retriever(search_kwargs={"k": 3})

eval_dataset = [
    {
        "question": "What is tokenization, and why is it important in LLMs?",
        "answer": "Tokenization is the process of splitting text into smaller units called tokens, such as words, subwords, or characters. It allows LLMs to process text efficiently, handle unknown words, and represent text numerically."
    },
    {
        "question": "What is the context window in an LLM?",
        "answer": "The context window is the maximum number of tokens an LLM can process at one time. A larger context window enables the model to understand longer documents and maintain better context, but requires more computation."
    },
    {
        "question": "What are the three main steps in Retrieval-Augmented Generation (RAG)?",
        "answer": "The three main steps are retrieval of relevant documents, ranking the retrieved documents by relevance, and generating a response using the retrieved context."
    },
    {
        "question": "How does LoRA differ from QLoRA?",
        "answer": "LoRA fine-tunes a model by adding low-rank adaptation matrices. QLoRA extends LoRA by quantizing the base model, typically to 4-bit precision, which significantly reduces memory usage while maintaining similar performance."
    },
    {
        "question": "What challenges do LLMs face during deployment?",
        "answer": "LLMs face challenges such as high computational requirements, bias inherited from training data, limited interpretability, and privacy or data security concerns."
    }
]

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)





def judge_faithfulness(question,context,generated_answer):
    judge_prompt=ChatPromptTemplate.from_messages([
        ("system","You are an evaluation judge. Given a question, the retrieved context, and the generated answer, score how faithful the answer is to the context. A score of 5 means every claim in the answer is directly supported by the context. A score of 1 means the answer contains information not found in the context. Respond with ONLY a number from 1 to 5."),
        ("user","question {question}\n\n context {context}\n\n generated_answer {generated_answer}")
    ])
    chain=judge_prompt|llm
    response = chain.invoke({
    "question": question,
    "context": context,
    "generated_answer": generated_answer
})
    result = int(response.content.strip())
    return result

rag_chain=(
    {"context": ret | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
results = []
scores = []
for item in eval_dataset:
    docs = ret.invoke(item["question"])
    context = format_docs(docs)
    answer = rag_chain.invoke(item["question"])
    score = judge_faithfulness(item["question"], context, answer)
    
    results.append({
        "question": item["question"],
        "ground_truth": item["answer"],
        "generated_answer": answer,
        "faithfulness_score": score
    })
    scores.append(score)
    print(f"Q: {item['question']}")
    print(f"A: {answer}")
    print(f"Faithfulness: {score}/5\n")
avg = sum(scores) / len(scores)
print(f"Average Faithfulness Score: {avg}/5")