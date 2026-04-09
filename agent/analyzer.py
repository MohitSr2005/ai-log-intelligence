from model.predict import classify_log
from agent.templates import FIX_SUGGESTIONS

def analyze_log(log_text: str):
    result = classify_log(log_text)
    issue_type = str(result["issue_type"])
    confidence = float(result["confidence"])

    explanation = FIX_SUGGESTIONS.get(issue_type, {
        "root_cause": "Unknown issue",
        "suggested_fix": "Inspect logs manually"
    })

    return {
        "issue_type": issue_type,
        "confidence": confidence,
        "root_cause": explanation["root_cause"],
        "suggested_fix": explanation["suggested_fix"]
    }