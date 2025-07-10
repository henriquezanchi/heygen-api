
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()
templates = Jinja2Templates(directory="templates")

API_KEY = "MDM1NDhlYTE5MzgzNDc4N2I3N2RiNzE4ZmRkMTg2YjktMTc1MjE2NzY3Nw=="
BASE_URL = "https://api.heygen.com/v2"

headers = {
    "X-Api-Key": API_KEY,
    "Content-Type": "application/json"
}


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    avatars_res = requests.get(f"{BASE_URL}/avatars", headers=headers)
    voices_res = requests.get(f"{BASE_URL}/voices", headers=headers)

    avatars = avatars_res.json().get("data", [])
    voices = voices_res.json().get("data", [])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "avatars": avatars,
        "voices": voices
    })


@app.post("/gerar-video")
async def gerar_video(request: Request, text: str = Form(...), avatar_id: str = Form(...), voice_id: str = Form(...)):
    payload = {
        "avatar_id": avatar_id,
        "voice_id": voice_id,
        "test": True,
        "input_text": text
    }

    response = requests.post(f"{BASE_URL}/videos", headers=headers, json=payload)
    result = response.json()

    return {"resposta_api": result}
