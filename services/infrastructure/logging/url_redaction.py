"""
URL Parameter Redaction Filter for Logging

Security measure to prevent sensitive data (API keys, tokens) from being logged
when passed as URL query parameters.

Created: 2026-01-17
Issue: Security incident - Gemini API key leaked via httpx INFO logs
"""

import logging
import re
from typing import List, Pattern


class URLRedactionFilter(logging.Filter):
    """
    Logging filter that redacts sensitive URL parameters from log messages.

    Redacts query parameters matching patterns like:
    - key=VALUE
    - api_key=VALUE
    - apikey=VALUE
    - token=VALUE
    - secret=VALUE
    - password=VALUE
    - auth=VALUE
    - bearer=VALUE
    - access_token=VALUE
    - client_secret=VALUE

    Example:
        Before: https://api.example.com/v1?key=AIzaSyD123abc&other=value
        After:  https://api.example.com/v1?key=[REDACTED]&other=value
    """

    # Patterns for sensitive URL parameters (case-insensitive)
    SENSITIVE_PARAM_PATTERNS: List[str] = [
        r"key=",
        r"api_key=",
        r"apikey=",
        r"api-key=",
        r"token=",
        r"access_token=",
        r"refresh_token=",
        r"secret=",
        r"client_secret=",
        r"password=",
        r"passwd=",
        r"auth=",
        r"authorization=",
        r"bearer=",
        r"credential=",
        r"credentials=",
    ]

    # Compiled regex pattern for efficient matching
    # Matches: param_name=value (where value continues until & or end of string/whitespace)
    _redaction_pattern: Pattern = None

    def __init__(self, name: str = ""):
        super().__init__(name)
        self._compile_pattern()

    def _compile_pattern(self) -> None:
        """Compile the regex pattern for URL parameter redaction."""
        # Build alternation of all sensitive parameter names
        param_names = "|".join(self.SENSITIVE_PARAM_PATTERNS)
        # Match: (param_name=)(value until & or whitespace or end)
        # The value can contain any characters except & and whitespace
        self._redaction_pattern = re.compile(rf"({param_names})([^&\s]+)", re.IGNORECASE)

    def redact_message(self, message: str) -> str:
        """
        Redact sensitive URL parameters from a message string.

        Args:
            message: The log message to redact

        Returns:
            Message with sensitive parameter values replaced with [REDACTED]
        """
        if not message:
            return message

        # Replace all matches with param_name=[REDACTED]
        return self._redaction_pattern.sub(r"\1[REDACTED]", str(message))

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter method called by logging framework.

        Modifies the log record in place to redact sensitive data.
        Always returns True (allows the record through after redaction).

        Args:
            record: The log record to filter

        Returns:
            True (always allows record, but modifies it)
        """
        # Redact the main message
        if record.msg:
            record.msg = self.redact_message(str(record.msg))

        # Redact any arguments that might contain URLs
        if record.args:
            if isinstance(record.args, dict):
                record.args = {
                    k: self.redact_message(str(v)) if isinstance(v, str) else v
                    for k, v in record.args.items()
                }
            elif isinstance(record.args, tuple):
                record.args = tuple(
                    self.redact_message(str(arg)) if isinstance(arg, str) else arg
                    for arg in record.args
                )

        return True


def install_url_redaction_filter(logger_names: List[str] = None) -> None:
    """
    Install the URL redaction filter on specified loggers.

    If no logger names provided, installs on common HTTP client loggers:
    - httpx
    - httpcore
    - urllib3
    - requests
    - aiohttp

    Args:
        logger_names: Optional list of logger names to filter.
                     If None, uses default HTTP client loggers.
    """
    if logger_names is None:
        logger_names = [
            "httpx",
            "httpcore",
            "urllib3",
            "requests",
            "aiohttp",
            "aiohttp.client",
        ]

    redaction_filter = URLRedactionFilter()

    for name in logger_names:
        logger = logging.getLogger(name)
        # Check if filter already installed to avoid duplicates
        if not any(isinstance(f, URLRedactionFilter) for f in logger.filters):
            logger.addFilter(redaction_filter)


def install_root_redaction_filter() -> None:
    """
    Install the URL redaction filter on the root logger.

    This ensures ALL log messages are filtered, regardless of which
    logger emits them. Use this for maximum security coverage.
    """
    redaction_filter = URLRedactionFilter()
    root_logger = logging.getLogger()

    # Check if filter already installed to avoid duplicates
    if not any(isinstance(f, URLRedactionFilter) for f in root_logger.filters):
        root_logger.addFilter(redaction_filter)
