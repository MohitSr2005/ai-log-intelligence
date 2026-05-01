import logging
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent.analyzer import analyze_log, analyze_logs

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Log Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BatchLogRequest(BaseModel):
    logs: list[str]


@app.get("/")
def home():
    return {"message": "AI Log Intelligence API is running"}

@app.get("/dashboard")
def dashboard():
    sample_logs = [
        "Database connection refused",
        "JWT token expired",
        "Request timeout",
        "No module named sklearn"
    ]

    results = [analyze_log(log) for log in sample_logs]

    return {
        "total_events": len(sample_logs),
        "anomalies_detected": sum(1 for r in results if r["issue_type"] != "unknown"),
        "ai_patterns_found": len(set(r["issue_type"] for r in results)),
        "avg_response_time": "120ms",
        "status": "online"
    }

@app.get("/logs")
def get_logs():
    return [
        "INFO: Server started",
        "ERROR: Database timeout",
        "WARNING: Token expired"
    ]
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

        if result.get("confidence", 0) < 0.60:
            result["issue_type"] = "uncertain"

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

    valid_logs = [log for log in request.logs if log and log.strip()]
    if not valid_logs:
        return {
            "status": "error",
            "message": "No logs provided"
        }

    try:
        result = analyze_logs(valid_logs)
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