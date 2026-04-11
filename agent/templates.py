FIX_SUGGESTIONS = {
    "database_error": {
        "root_cause": "Database server may be down, unreachable, or configured incorrectly",
        "suggested_fix": "Check DB host, port, credentials, and whether the database service is running"
    },
    "auth_error": {
        "root_cause": "Authentication token is invalid, missing, or expired",
        "suggested_fix": "Check token generation, token expiry, and authorization headers"
    },
    "timeout_error": {
        "root_cause": "The service took too long to respond",
        "suggested_fix": "Check network latency, server load, and timeout configuration"
    },
    "dependency_error": {
        "root_cause": "A required library or module is missing or incompatible",
        "suggested_fix": "Install missing dependencies and verify package versions"
    },
    "config_error": {
        "root_cause": "Required configuration or environment variables are missing or incorrect",
        "suggested_fix": "Check environment variables, secrets, and configuration files"
    },
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
}
}