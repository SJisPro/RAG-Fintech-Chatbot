# backend/main.py
from fastapi import FastAPI, HTTPException, Request
from backend.auth import authenticate_user
from backend.rag import generate_response
from backend.rbac import is_authorized
from backend.vector_store import search

app = FastAPI()
sessions = {}

@app.post("/login")
async def login(request: Request):
    body = await request.json()
    user = authenticate_user(body["username"], body["password"])
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    sessions[body["username"]] = user["role"]
    return {"message": "Login successful", "role": user["role"]}

@app.post("/query")
async def query(request: Request):
    body = await request.json()
    username = body.get("username")
    query_text = body.get("query")

    role = sessions.get(username)
    if not role:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Retrieve documents without role filter (get all possible matches)
    docs = search(query_text)

    authorized_docs = []
    authorized_sources = []

    # Check each document using RBAC
    for idx, meta in enumerate(docs['metadatas'][0]):
        if is_authorized(role, meta['category']):
            authorized_docs.append(docs['documents'][0][idx]) 
            authorized_sources.append(meta['source'])

    # If no authorized documents, return a friendly message
    if not authorized_docs:
                # Optional: Role-based customized message
        role_guidance = {
            "finance": "You can ask about financial reports, expenses, and reimbursements.",
            "marketing": "You can ask about campaign performance, customer feedback, and sales metrics.",
            "hr": "You can ask about employee records, attendance, and performance reviews.",
            "engineering": "You can ask about system architecture, development processes, and operational guidelines.",
            "executive": "You have access to all company data.",
            "employee": "You can ask about general company policies, events, and FAQs."
        }

        return {
            "answer": f"This information is outside your access level. {role_guidance.get(role, '')}",
            "sources": []
        }
    # Call the LLM with only the authorized documents
    response = generate_response(query_text, role, authorized_docs, authorized_sources)

    return response