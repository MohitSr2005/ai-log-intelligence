import logging
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.analyzer import analyze_log, analyze_logs

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Log Intelligence API")

# ✅ ADD THIS BLOCK (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend (localhost:5501)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BatchLogRequest(BaseModel):
    logs: list[str]


@app.get("/")
def home():
    return {
        "message": "AI Log Intelligence API is running"
    }


@app.post("/analyze")
async def analyze_log_api(
    log_text: Optional[str] = Form(None),
    log_file: Optional[UploadFile] = File(None)
):
    logging.info("Request received for single log analysis")

    content = log_text

    if log_file:
        logging.info("File uploaded for single log analysis")
        file_bytes = await log_file.read()
        content = file_bytes.decode("utf-8", errors="ignore")

    if not content or not content.strip():
        logging.warning("Empty log received")
        return {
            "status": "error",
            "message": "No log provided"
        }

    try:
        result = analyze_log(content)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")

        return {
            "status": "error",
            "message": "Internal server error"
        }


@app.post("/analyze-batch")
async def analyze_batch_logs(request: BatchLogRequest):
    logging.info("Request received for batch log analysis")

    if not request.logs or not any(log.strip() for log in request.logs):
        return {
            "status": "error",
            "message": "No logs provided"
        }

    try:
        result = analyze_logs(request.logs)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        logging.error(f"Batch error occurred: {str(e)}")

        return {
            "status": "error",
            "message": "Internal server error"
        }