from fastapi import FastAPI, Request
from pydantic import BaseModel
# from slack_sdk.signature import SignatureVerifier

# # SLACK_SIGNING_SECRETを設定
# SLACK_SIGNING_SECRET = "b951ffe9aaa0acf3c3c4d978c1eba4f2"
# verifier = SignatureVerifier(signing_secret)

app = FastAPI()

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

@app.post("/slack/events")
async def read_slack_event(request: Request, event: SlackEvent):
    # # Slackからのリクエストの署名を検証
    # if not verifier.is_valid_request(await request.body(), request.headers):
    #     return {"error": "invalid request"}


    # SlackのURL検証のための応答
    if event.type == "url_verification":
        return {"challenge": event.challenge}

    # メッセージイベントの処理
    if event.type == "event_callback":
        if event.event["type"] == "message":
            print(f"Received message from channel {event.event['channel']}: {event.event['text']}")

    return {"status": "ok"}
