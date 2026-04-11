from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional

from agent.analyzer import analyze_log
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Log Intelligence API")


@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

@app.post("/analyze")
async def analyze_log_api(
    log_text: Optional[str] = Form(None),
    log_file: Optional[UploadFile] = File(None)
):
    logging.info("Request received for log analysis")
    content = log_text

    if log_file:
        logging.info("File uploaded for analysis")
        file_bytes = await log_file.read()
        content = file_bytes.decode("utf-8", errors="ignore")

    if not content or not content.strip():
        logging.warning("Empty log received")
        return {
            "status": "error",
            "message": "No log provided"
        }
    logging.info(f"Processing log: {content}")

    try:
        result = analyze_log(content)

        logging.info(f"Result: {result}")

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
