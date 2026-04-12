from collections import Counter
from model.predict import classify_log
from agent.templates import FIX_SUGGESTIONS


def analyze_log(log_text: str) -> dict:
    result = classify_log(log_text)

    issue_type = str(result.get("issue_type", "unknown"))
    confidence = float(result.get("confidence", 0.0))
    reasoning = str(result.get("reasoning", "No reasoning available"))

    explanation = FIX_SUGGESTIONS.get(
        issue_type,
        FIX_SUGGESTIONS["unknown"]
    )

    return {
        "issue_type": issue_type,
        "confidence": round(confidence, 4),
        "root_cause": explanation["root_cause"],
        "suggested_fix": explanation["suggested_fix"],
        "reasoning": reasoning,
    }


def analyze_logs(logs: list[str]) -> dict:
    if not logs:
        explanation = FIX_SUGGESTIONS["unknown"]
        return {
            "issue_type": "unknown",
            "confidence": 0.0,
            "root_cause": explanation["root_cause"],
            "suggested_fix": explanation["suggested_fix"],
            "reasoning": "No logs provided",
        }

    results = [classify_log(log) for log in logs if log and log.strip()]

    if not results:
        explanation = FIX_SUGGESTIONS["unknown"]
        return {
            "issue_type": "unknown",
            "confidence": 0.0,
            "root_cause": explanation["root_cause"],
            "suggested_fix": explanation["suggested_fix"],
            "reasoning": "No valid logs provided",
        }

    filtered = [r for r in results if r.get("issue_type") != "uncertain"]

    if not filtered:
        final_issue = "uncertain"
        count = len(results)
        matched_results = results
    else:
        issue_counts = Counter(r["issue_type"] for r in filtered)
        final_issue, count = issue_counts.most_common(1)[0]
        matched_results = [r for r in filtered if r["issue_type"] == final_issue]

    avg_confidence = sum(r["confidence"] for r in matched_results) / len(matched_results)

    explanation = FIX_SUGGESTIONS.get(final_issue, FIX_SUGGESTIONS["unknown"])

    return {
        "issue_type": final_issue,
        "confidence": round(avg_confidence, 4),
        "root_cause": explanation["root_cause"],
        "suggested_fix": explanation["suggested_fix"],
        "reasoning": f"{count} out of {len(results)} logs strongly indicate '{final_issue}'",
    }


if __name__ == "__main__":
    sample_log = "JWT token expired for request"
    print(analyze_log(sample_log))

    sample_logs = [
        "Database connection refused on port 5432",
        "Could not connect to PostgreSQL database",
        "Request timeout while waiting for DB"
    ]
    print(analyze_logs(sample_logs))