from pathlib import Path
import joblib

MODEL_PATH = Path(__file__).resolve().parent / "log_classifier.pkl"

pipeline = None
if MODEL_PATH.exists():
    try:
        pipeline = joblib.load(MODEL_PATH)
    except Exception:
        pipeline = None


def make_result(issue_type: str, confidence: float, reasoning: str) -> dict:
    return {
        "issue_type": issue_type,
        "confidence": round(confidence, 2),
        "reasoning": reasoning,
    }


def adjust_confidence(base_confidence: float, log_text: str) -> float:
    text = log_text.lower()
    boost_words = [
        "error",
        "failed",
        "timeout",
        "database",
        "connection",
        "unauthorized",
        "forbidden",
    ]
    matches = sum(1 for word in boost_words if word in text)
    boost = min(matches * 0.02, 0.10)
    return min(base_confidence + boost, 0.99)


def _rule_based_classify(log_text: str) -> dict:
    text = log_text.lower()

    if any(word in text for word in [
        "no module named",
        "importerror",
        "modulenotfounderror",
        "dependency",
        "package not found",
    ]):
        return make_result(
            "dependency_error",
            0.90,
            "Matched dependency-related keywords",
        )

    if any(word in text for word in [
        "secret_key",
        "environment variable",
        ".env",
        "missing env",
        "env var",
        "configuration missing",
        "missing configuration",
    ]):
        return make_result(
            "config_error",
            0.90,
            "Matched configuration-related keywords",
        )

    if any(word in text for word in [
        "jwt",
        "token expired",
        "unauthorized",
        "forbidden",
        "authentication failed",
        "auth failed",
        "access denied",
    ]):
        return make_result(
            "auth_error",
            0.90,
            "Matched authentication-related keywords",
        )

    if any(word in text for word in [
        "database",
        "db error",
        "connection refused",
        "sql",
        "postgres",
        "postgresql",
        "mysql",
        "could not connect",
        "port 5432",
    ]):
        return make_result(
            "database_error",
            0.89,
            "Matched database-related keywords",
        )

    if any(word in text for word in [
        "timeout",
        "timed out",
        "gateway timeout",
        "request timeout",
    ]):
        return make_result(
            "timeout_error",
            0.88,
            "Matched timeout-related keywords",
        )

    if any(word in text for word in [
        "internal server error",
        "http 500",
        "500 internal",
        "server crashed",
        "service unavailable",
    ]):
        return make_result(
            "server_error",
            0.84,
            "Matched server-error-related keywords",
        )

    if any(word in text for word in [
        "out of memory",
        "memory error",
        "oom",
        "killed process",
    ]):
        return make_result(
            "memory_error",
            0.87,
            "Matched memory-related keywords",
        )

    return make_result(
        "unknown",
        0.50,
        "No strong rule-based pattern matched",
    )


def classify_log(log_text: str) -> dict:
    if not log_text or not log_text.strip():
        return make_result("unknown", 0.0, "Empty log input")

    rule_result = _rule_based_classify(log_text)
    if rule_result["issue_type"] != "unknown" and rule_result["confidence"] >= 0.88:
        return rule_result

    if pipeline is not None:
        try:
            pred = pipeline.predict([log_text])[0]

            confidence = 0.80
            if hasattr(pipeline, "predict_proba"):
                probs = pipeline.predict_proba([log_text])[0]
                confidence = float(max(probs))

            confidence = adjust_confidence(confidence, log_text)

            if confidence < 0.60:
                return make_result(
                    "uncertain",
                    confidence,
                    "Model confidence is too low, more context is needed",
                )

            return make_result(
                str(pred),
                confidence,
                "Prediction made by trained ML model",
            )
        except Exception:
            pass

    if rule_result["issue_type"] != "unknown":
        return rule_result

    return make_result(
        "uncertain",
        0.40,
        "Neither rules nor model could confidently classify the log",
    )


if __name__ == "__main__":
    test_log = "Database connection refused on port 5432"
    print(classify_log(test_log))