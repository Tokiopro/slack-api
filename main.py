from fastapi import FastAPI, Depends
from slackeventsapi import SlackEventAdapter
from starlette.requests import Request
import requests
url = url = "https://slack.com/api/conversations.history"
token = "xoxb-4237706031364-6076555905863-akYICXYKNlguI3eoNUVl74us"
response = requests.get('http://www.example.com')

app = FastAPI()

# Slackの署名秘密鍵を設定
SLACK_SIGNING_SECRET = "b951ffe9aaa0acf3c3c4d978c1eba4f2"
slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events")

# メッセージイベントのハンドラを定義
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    print(f"Received message: {message['text']}")

# FastAPIのエンドポイントでslackeventsapiの処理を呼び出す
@app.post("/slack/events")
async def slack_events(request: Request):
    return slack_events_adapter.server.handle(request)

# サーバーの起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
