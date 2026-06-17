from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import openai
import os

app = FastAPI(title="AI Inference Service")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    message: str
    conversation_history: list[dict] = []
    max_context_tokens: int = 4096

def build_prompt(history: list[dict], message: str) -> list[dict]:
    """Build prompt with sliding context window."""
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": message})
    return messages

@app.post("/chat")
def chat(request: ChatRequest):
    """Non-streaming chat endpoint."""
    messages = build_prompt(request.conversation_history, request.message)
    response = client.chat.completions.create(model="gpt-4", messages=messages)
    return {"response": response.choices[0].message.content}

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    """Streaming chat endpoint using SSE."""
    messages = build_prompt(request.conversation_history, request.message)

    def generate():
        stream = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "ai-inference-service"}
