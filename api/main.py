from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
<<<<<<< HEAD
from agent.analyzer import analyze_log

app = FastAPI(title="AI Log Intelligence API")
=======

from agent.analyzer import analyze_log

app = FastAPI()

>>>>>>> e729cf9fc5311c125a25022a0a70f4137b5b7919

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

<<<<<<< HEAD
=======

>>>>>>> e729cf9fc5311c125a25022a0a70f4137b5b7919
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

<<<<<<< HEAD
    return analyze_log(content)
=======
    result = analyze_log(content)

    return result
>>>>>>> e729cf9fc5311c125a25022a0a70f4137b5b7919
