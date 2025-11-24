from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class PlayerImage(BaseModel):
    image_base64: str

@app.post("/predict_team")
def predict_team(data: PlayerImage):
    # Mock prediction: Randomly assign Team A or Team B
    team = random.choice(["Team A", "Team B"])
    return {"team_id": team, "confidence": 0.95}

@app.get("/health")
def health_check():
    return {"status": "ok"}
