FIX_SUGGESTIONS = {
    "auth_error": {
        "root_cause": "JWT or token authentication failed.",
        "suggested_fix": "Check token expiry, secret key, and authentication flow."
    },
    "database_error": {
        "root_cause": "Database connection failed or database service is unreachable.",
        "suggested_fix": "Verify database host, port, credentials, and server status."
    },
    "timeout_error": {
        "root_cause": "The request or service exceeded the allowed timeout.",
        "suggested_fix": "Check server load, optimize queries, and increase timeout if needed."
    },
    "server_error": {
        "root_cause": "Internal server failure occurred while processing the request.",
        "suggested_fix": "Inspect backend logs, stack traces, and dependent services."
    },
    "unknown": {
        "root_cause": "Log pattern was not recognized by the model.",
        "suggested_fix": "Inspect logs manually and add more training samples for this issue."
    },
<<<<<<< HEAD
    "api_error": {
        "root_cause": "Server-side route or application logic failed",
        "suggested_fix": "Inspect stack trace, route handler logic, and backend logs"
    },
    "server_error": {
        "root_cause": "Internal server error occurred due to application failure.",
        "suggested_fix": "Check backend logs, stack trace, and server-side code."
    },
    "memory_error": {
        "root_cause": "System ran out of memory while processing request.",
        "suggested_fix": "Optimize memory usage or increase system resources."
    },
    "unknown": {
        "root_cause": "Log pattern not recognized.",
        "suggested_fix": "Check logs manually or improve training dataset."
=======
    "uncertain": {
    "root_cause": "The system could not determine the issue with enough confidence.",
    "suggested_fix": "Provide more detailed logs or additional context."
>>>>>>> 38d73d0 (fixed nested repo issue + added AI improvements)
}
}