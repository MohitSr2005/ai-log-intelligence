FIX_SUGGESTIONS = {
    "database_error": {
        "root_cause": "Database connection failed",
        "suggested_fix": "Check DB server, port, credentials"
    },
    "auth_error": {
        "root_cause": "Authentication failed",
        "suggested_fix": "Check token, credentials, login flow"
    },
    "timeout_error": {
        "root_cause": "Request took too long",
        "suggested_fix": "Check server load and timeout settings"
    },
    "dependency_error": {
        "root_cause": "Missing or incompatible dependency",
        "suggested_fix": "Install required packages"
    },
    "config_error": {
        "root_cause": "Configuration missing or incorrect",
        "suggested_fix": "Check environment variables and config files"
    },
    "api_error": {
        "root_cause": "Backend logic failure",
        "suggested_fix": "Check API code and logs"
    }
}