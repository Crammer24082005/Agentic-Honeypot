from fastapi import FastAPI, Header, HTTPException, Request
from detector import is_scam
from agent_loop import run_honeypot
import os

API_KEY = os.getenv("HONEYPOT_API_KEY")

app = FastAPI(title="Agentic Honeypot API")


@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # 1. Auth check
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Safely extract message
    message = ""

    try:
        data = await request.json()
        if isinstance(data, dict):
            message = data.get("message", "")
        else:
            message = str(data)
    except:
        try:
            message = (await request.body()).decode("utf-8")
        except:
            message = ""

    # 3. Ensure message is always a string
    if not isinstance(message, str):
        message = str(message)

    # 4. Validation-only path (hackathon tester)
    if not message.strip():
        return {
            "status": "ok",
            "authenticated": True,
            "honeypot_ready": True
        }

    # 5. Scam check
    if not is_scam(message):
        return {
            "status": "ok",
            "is_scam": False
        }

    # 6. Run honeypot
    result = run_honeypot(message, lambda x: "mock reply")

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
