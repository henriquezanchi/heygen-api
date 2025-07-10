from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, time

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

API_KEY = "MDM1NDhlYTE5MzgzNDc4N2I3N2RiNzE4ZmRkMTg2YjktMTc1MjE2NzY3Nw=="

class VideoRequest(BaseModel):
    avatar_id: str
    voice_id: str
    texto: str

@app.get("/avatars")
def listar_avatars():
    resp = requests.get("https://api.heygen.com/v2/avatars", headers={"X-Api-Key": API_KEY})
    return resp.json()

@app.get("/voices")
def listar_voices():
    resp = requests.get("https://api.heygen.com/v2/voices", headers={"X-Api-Key": API_KEY})
    return resp.json()

@app.post("/gerar-video")
def gerar_video(req: VideoRequest):
    payload = {
        "video_inputs": [
            {
                "character": {"type": "avatar", "avatar_id": req.avatar_id},
                "voice": {"type": "text", "voice_id": req.voice_id, "input_text": req.texto},
                "background": {"type": "color", "value": "#ffffff"}
            }
        ],
        "dimension": {"width": 1280, "height": 720},
        "title": "Vídeo via web app"
    }
    r = requests.post("https://api.heygen.com/v2/video/generate",
                      headers={"X-Api-Key": API_KEY, "Content-Type": "application/json"},
                      json=payload)
    if r.status_code != 200:
        return {"erro": r.json()}
    vid = r.json()["data"]["video_id"]
    for _ in range(20):
        time.sleep(5)
        st = requests.get(f"https://api.heygen.com/v2/video/status?video_id={vid}",
                          headers={"X-Api-Key": API_KEY}).json()
        if st.get("data", {}).get("status") == "completed":
            return {"video_url": st["data"]["video_url"]}
    return {"erro": "Tempo esgotado."}
