from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from agent.analyzer import analyze_log

app = FastAPI(title="AI Log Intelligence API")

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

@app.post("/analyze")
async def analyze_log_api(
    log_text: Optional[str] = Form(None),
    log_file: Optional[UploadFile] = File(None)
):
    content = log_text

    if log_file:
        file_bytes = await log_file.read()
        content = file_bytes.decode("utf-8", errors="ignore")

    if not content:
        return {"error": "No log provided"}

    return analyze_log(content)