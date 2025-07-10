
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import os

app = FastAPI()
API_KEY = "MDM1NDhlYTE5MzgzNDc4N2I3N2RiNzE4ZmRkMTg2YjktMTc1MjE2NzY3Nw=="

app.mount("/static", StaticFiles(directory="static"), name="static")

class VideoRequest(BaseModel):
    avatar_id: str
    voice_id: str
    texto: str

@app.get("/", response_class=HTMLResponse)
async def get_index():
    return FileResponse("index.html")

@app.get("/avatars")
async def get_avatars():
    url = "https://api.heygen.com/v2/avatars.list"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

@app.get("/voices")
async def get_voices():
    url = "https://api.heygen.com/v2/voices.list"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()

@app.post("/gerar-video")
async def gerar_video(req: VideoRequest):
    url = "https://api.heygen.com/v2/video.create"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "avatar_id": req.avatar_id,
        "voice_id": req.voice_id,
        "test": True,
        "video_inputs": [
            {
                "input_text": req.texto
            }
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=response.text)
    return response.json()
