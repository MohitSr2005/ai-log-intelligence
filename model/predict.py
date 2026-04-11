from email.mime import text

import joblib

pipeline = joblib.load("model/log_classifier.pkl")

def classify_log(log_text: str):
    text = log_text.lower()
    if "no module named" in text or "importerror" in text:
        return {"issue_type": "dependency_error", "confidence": 0.9}

    if "secret_key" in text or "env" in text:
        return {"issue_type": "config_error", "confidence": 0.9}

    if "database" in text or "connection refused" in text:
        return {"issue_type": "database_error", "confidence": 0.9}
    elif "token" in text or "jwt" in text:
        return {"issue_type": "auth_error", "confidence": 0.85}
    elif "timeout" in text:
        return {"issue_type": "timeout_error", "confidence": 0.8}
    else:
        return {"issue_type": "unknown", "confidence": 0.5}


if __name__ == "__main__":
    test_log = "JWT token expired for request"
    print(classify_log(test_log))
