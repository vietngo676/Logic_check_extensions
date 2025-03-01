import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load API key từ file .env
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

if not MISTRAL_API_KEY:
    raise ValueError("API key của Mistral chưa được thiết lập!")

# Khởi tạo FastAPI
app = FastAPI()

# Định nghĩa request body model
class TextRequest(BaseModel):
    text: str

# API endpoint của Mistral (OpenAI-compatible)
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

# Hàm phân tích văn bản bằng API mới của Mistral AI
def analyze_text_with_mistral(text: str):
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistral-medium",
        "messages": [{"role": "user", "content": text}]
    }

    response = requests.post(MISTRAL_API_URL, json=payload, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()["choices"][0]["message"]["content"]

# API kiểm tra server
@app.get("/")
def read_root():
    return {"message": "Hello, Logic Check Extension!"}

# API phân tích logic văn bản
@app.post("/analyze")
async def analyze_text(request: TextRequest):
    analysis = analyze_text_with_mistral(request.text)
    return {"success": True, "analysis": analysis}
    