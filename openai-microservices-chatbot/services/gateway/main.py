from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI(title="API Gateway", description="Central gateway for all microservices")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SERVICES = {
    "users": os.getenv("USER_SERVICE_URL", "http://user_service:8001"),
    "conversations": os.getenv("CONVERSATION_SERVICE_URL", "http://conversation_service:8002"),
    "ai": os.getenv("AI_SERVICE_URL", "http://ai_inference_service:8003"),
}

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "service": "api-gateway"}

@app.post("/api/v1/auth/register")
async def register(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['users']}/register", json=body)
    return response.json()

@app.post("/api/v1/auth/login")
async def login(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['users']}/login", json=body)
    return response.json()

@app.post("/api/v1/conversations")
async def create_conversation(request: Request):
    body = await request.json()
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{SERVICES['conversations']}/conversations", json=body)
    return response.json()
