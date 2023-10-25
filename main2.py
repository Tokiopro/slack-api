from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import hashlib
import hmac
import time

app = FastAPI()

SLACK_SIGNING_SECRET = "b951ffe9aaa0acf3c3c4d978c1eba4f2"

class SlackEvent(BaseModel):
    token: str
    team_id: str
    api_app_id: str
    event: dict
    type: str
    event_id: str
    event_time: int
    authed_users: list
    challenge: str = None

def verify_slack_signature(request_body: bytes, timestamp: str, signature: str):
    req = str.encode(f"v0:{timestamp}:") + request_body
    request_hash = hmac.new(
        bytes(SLACK_SIGNING_SECRET , 'UTF-8'),
        req,
        hashlib.sha256
    ).hexdigest()
    calc_signature = f"v0={request_hash}"
    if not hmac.compare_digest(calc_signature, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

@app.post("/slack/events")
async def read_slack_event(request, event: SlackEvent):
    timestamp = request.headers.get("X-Slack-Request-Timestamp")
    signature = request.headers.get("X-Slack-Signature")
    request_body = await request.body()

    # Verify Slack request signature
    verify_slack_signature(request_body, timestamp, signature)

    # URL verification for Slack
    if event.type == "url_verification":
        return {"challenge": event.challenge}

    # Handle message event
    if event.type == "event_callback":
        if event.event["type"] == "message":
            print(f"Received message: {event.event['text']}")

    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
