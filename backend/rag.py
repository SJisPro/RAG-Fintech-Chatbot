from backend.vector_store import search
from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(query, role, docs, sources):
    prompt = f"Answer the question based on the following documents:\n\n"
    for idx, context in enumerate(docs):
        prompt += f"Document {idx+1}:\n{context}\n\n"
    prompt += f"Question: {query}\nAnswer:" 

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return {"answer": response.choices[0].message.content.strip(), "sources": sources}

