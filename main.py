from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import requests

app = FastAPI()

API_KEY = "MDM1NDhlYTE5MzgzNDc4N2I3N2RiNzE4ZmRkMTg2YjktMTc1MjE2NzY3Nw=="
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/avatars")
async def listar_avatars():
    try:
        response = requests.get("https://api.heygen.com/v2/avatars", headers=HEADERS)
        return response.json()
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)

@app.get("/voices")
async def listar_voices():
    try:
        response = requests.get("https://api.heygen.com/v2/voices", headers=HEADERS)
        return response.json()
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)

@app.post("/gerar-video")
async def gerar_video(request: Request):
    data = await request.json()
    payload = {
        "video_inputs": {
            "avatar_id": data["avatar_id"],
            "voice_id": data["voice_id"],
            "script": {
                "type": "text",
                "input": data["texto"]
            }
        }
    }
    try:
        response = requests.post("https://api.heygen.com/v1/video.create", headers=HEADERS, json=payload)
        return response.json()
    except Exception as e:
        return JSONResponse(content={"erro": str(e)}, status_code=500)