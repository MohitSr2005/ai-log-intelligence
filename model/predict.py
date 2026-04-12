
from email.mime import text


from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).resolve().parent / "log_classifier.pkl"

pipeline = None
if MODEL_PATH.exists():
    try:
        pipeline = joblib.load(MODEL_PATH)
    except Exception:
        pipeline = None


def _rule_based_classify(log_text: str) -> dict:
    text = log_text.lower()
    if "no module named" in text or "importerror" in text:
        return {"issue_type": "dependency_error", "confidence": 0.9}

    if "secret_key" in text or "env" in text:
        return {"issue_type": "config_error", "confidence": 0.9}

    if any(word in text for word in [
        "no module named", "importerror", "modulenotfounderror", "dependency", "package not found"
    ]):
        return {
            "issue_type": "dependency_error",
            "confidence": 0.90,
            "reasoning": "Matched dependency-related keywords"
        }

    if any(word in text for word in [
        "secret_key", "env", "environment variable", "configuration missing", "missing configuration"
    ]):
        return {
            "issue_type": "config_error",
            "confidence": 0.90,
            "reasoning": "Matched configuration-related keywords"
        }

    if any(word in text for word in [
        "jwt", "token expired", "unauthorized", "forbidden", "authentication failed", "auth failed"
    ]):
        return {
            "issue_type": "auth_error",
            "confidence": 0.90,
            "reasoning": "Matched authentication-related keywords"
        }

    if any(word in text for word in [
        "database", "db error", "connection refused", "sql", "postgres", "postgresql",
        "mysql", "could not connect", "db", "port 5432"
    ]):
        return {
            "issue_type": "database_error",
            "confidence": 0.89,
            "reasoning": "Matched database-related keywords"
        }

    if any(word in text for word in [
        "timeout", "timed out", "gateway timeout", "request timeout"
    ]):
        return {
            "issue_type": "timeout_error",
            "confidence": 0.88,
            "reasoning": "Matched timeout-related keywords"
        }

    if any(word in text for word in [
        "500", "internal server error", "nullpointer", "exception", "traceback"
    ]):
        return {
            "issue_type": "server_error",
            "confidence": 0.84,
            "reasoning": "Matched server-error-related keywords"
        }

    if any(word in text for word in [
        "out of memory", "memory error", "oom", "killed process"
    ]):
        return {
            "issue_type": "memory_error",
            "confidence": 0.87,
            "reasoning": "Matched memory-related keywords"
        }

    return {
        "issue_type": "unknown",
        "confidence": 0.50,
        "reasoning": "No strong rule-based pattern matched"
    }


def classify_log(log_text: str) -> dict:
    if not log_text or not log_text.strip():
        return {
            "issue_type": "unknown",
            "confidence": 0.0,
            "reasoning": "Empty log input"
        }

    # 1. Try rules first
    rule_result = _rule_based_classify(log_text)
    if rule_result["issue_type"] != "unknown":
        return rule_result

    # 2. Then try ML
    if pipeline is not None:
        try:
            pred = pipeline.predict([log_text])[0]

            confidence = 0.80
            if hasattr(pipeline, "predict_proba"):
                probs = pipeline.predict_proba([log_text])[0]
                confidence = float(max(probs))

            if confidence < 0.60:
                return {
                    "issue_type": "uncertain",
                    "confidence": confidence,
                    "reasoning": "Model confidence is too low, more context is needed"
                }

            return {
                "issue_type": str(pred),
                "confidence": confidence,
                "reasoning": "Prediction made by trained ML model"
            }
        except Exception:
            pass

    return {
        "issue_type": "uncertain",
        "confidence": 0.40,
        "reasoning": "Neither rules nor model could confidently classify the log"
    }


if __name__ == "__main__":
    test_log = "Database connection refused on port 5432"
    print(classify_log(test_log))