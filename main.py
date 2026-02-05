from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from detector import is_scam
from agent_loop import run_honeypot
import os
API_KEY = os.getenv("HONEYPOT_API_KEY")

app = FastAPI(title="Agentic Honeypot API")


class Message(BaseModel):
    message: str


@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # Auth check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Safely extract message
    message = ""
    try:
        data = await request.json()
        message = data.get("message", "")
    except:
        try:
            message = (await request.body()).decode("utf-8")
        except:
            message = ""

    # Validation-only path (hackathon tester)
    if not message or message.strip() == "":
        return {
            "status": "ok",
            "authenticated": True,
            "endpoint": "honeypot",
            "honeypot_ready": True
        }

    # Actual logic
    if not is_scam(message):
        return {
            "status": "ok",
            "is_scam": False
        }

    result = run_honeypot(message, mock_scammer_api)

    return {
        "status": "ok",
        "is_scam": True,
        "persona_used": "confused_upi_user",
        **result
    }
    
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Agentic Honeypot API",
        "message": "Use /honeypot or /docs"
    }

@app.get("/health")
def health():
return {"status": "healthy"}

@app.get("/favicon.ico")
def favicon():
    return {}
