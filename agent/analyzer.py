# def analyze_log(log_text: str):
#     return {
#         "issue_type": "demo_error",
#         "confidence": 0.99,
#         "root_cause": "This is a test root cause",
#         "suggested_fix": "This is a test fix"
#     }

from model.predict import classify_log
from .templates import FIX_SUGGESTIONS

def analyze_log(log_text: str):
    result = classify_log(log_text)

    issue_type = str(result["issue_type"])
    confidence = float(result["confidence"])

    explanation = FIX_SUGGESTIONS.get(issue_type, {
        "root_cause": "Unknown issue",
        "suggested_fix": "Check logs manually"
    })

    return {
        "issue_type": issue_type,
        "confidence": confidence,
        "root_cause": explanation["root_cause"],
        "suggested_fix": explanation["suggested_fix"]
    }