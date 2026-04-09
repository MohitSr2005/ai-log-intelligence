# def analyze_log(log_text: str):
#     return {
#         "issue_type": "demo_error",
#         "confidence": 0.99,
#         "root_cause": "Test root cause",
#         "suggested_fix": "Test fix"
#     }

from model.predict import classify_log
from agent.templates import FIX_SUGGESTIONS


def analyze_log(log_text: str) -> dict:
    result = classify_log(log_text)

    issue_type = str(result.get("issue_type", "unknown"))
    confidence = float(result.get("confidence", 0.0))

    explanation = FIX_SUGGESTIONS.get(
        issue_type,
        FIX_SUGGESTIONS["unknown"]
    )

    return {
        "issue_type": issue_type,
        "confidence": round(confidence, 4),
        "root_cause": explanation["root_cause"],
        "suggested_fix": explanation["suggested_fix"],
    }