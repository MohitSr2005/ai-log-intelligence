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
        "anomaly_score": round(1 - confidence, 2),
        "reasoning": reasoning,
    }


def _rule_based_classify(log_text: str) -> dict:
    text = log_text.lower()

    if any(w in text for w in [
        "jwt", "token expired", "unauthorized", "forbidden",
        "authentication failed", "auth failed", "access denied",
        "invalid credentials", "permission denied", "oauth"
    ]):
        return make_result("auth_error", 0.90, "Matched authentication-related keywords")

    if any(w in text for w in [
        "database", "db ", "sql", "postgres", "postgresql",
        "mysql", "mongodb", "connection pool", "port 5432",
        "could not connect", "connection refused"
    ]):
        return make_result("database_error", 0.89, "Matched database-related keywords")

    if any(w in text for w in [
        "timeout", "timed out", "gateway timeout",
        "request timeout", "read timeout"
    ]):
        return make_result("timeout_error", 0.88, "Matched timeout-related keywords")

    if any(w in text for w in [
        "internal server error", "http 500", "500 internal",
        "server crashed", "service unavailable",
        "backend crashed", "server failure"
    ]):
        return make_result("server_error", 0.86, "Matched server-error-related keywords")

    if any(w in text for w in [
        "no module named", "importerror", "modulenotfounderror",
        "dependency", "package not found", "missing library",
        "required module"
    ]):
        return make_result("dependency_error", 0.90, "Matched dependency-related keywords")

    if any(w in text for w in [
        "secret_key", "environment variable", ".env",
        "missing env", "env var", "configuration missing",
        "missing configuration", "config validation",
        "settings file"
    ]):
        return make_result("config_error", 0.90, "Matched configuration-related keywords")

    if any(w in text for w in [
        "out of memory", "memory error", "oom",
        "killed process", "memory killed", "heap space",
        "cannot allocate memory", "memory pressure"
    ]):
        return make_result("memory_error", 0.88, "Matched memory-related keywords")

    if any(w in text for w in [
        "api", "endpoint", "rest", "gateway",
        "payload", "invalid response", "api error",
        "request handler", "api controller", "malformed response"
    ]):
        return make_result("api_error", 0.88, "Matched API-related keywords")

    if any(w in text for w in [
        "server started successfully", "started successfully",
        "service started", "running successfully",
        "healthy", "startup complete",
        "all systems operational", "health check passed",
        "operating normally"
    ]):
        return make_result("normal", 0.85, "Matched normal execution pattern")

    return make_result("unknown", 0.50, "No strong rule-based pattern matched")


def classify_log(log_text: str) -> dict:
    if not log_text or not log_text.strip():
        return make_result("unknown", 0.0, "Empty log input")

    rule_result = _rule_based_classify(log_text)

    if rule_result["issue_type"] != "unknown":
        return rule_result

    if pipeline is not None:
        try:
            pred = pipeline.predict([log_text])[0]

            confidence = 0.80
            if hasattr(pipeline, "predict_proba"):
                probs = pipeline.predict_proba([log_text])[0]
                confidence = float(max(probs))

            if confidence < 0.60:
                return make_result(
                    "uncertain",
                    confidence,
                    "Model confidence is too low"
                )

            return make_result(
                str(pred),
                confidence,
                "Prediction made by trained ML model"
            )

        except Exception:
            pass

    return make_result(
        "uncertain",
        0.40,
        "Neither rules nor model could confidently classify the log"
    )


if __name__ == "__main__":
    print(classify_log("API gateway returned invalid payload"))