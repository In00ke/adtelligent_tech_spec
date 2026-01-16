"""Logging utils."""
import logging
import json


LOG_FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def get_logger(name):
    logger = logging.getLogger(name)
    if not logger.handlers:
        h = logging.StreamHandler()
        h.setFormatter(logging.Formatter(LOG_FMT, DATE_FMT))
        logger.addHandler(h)
        logger.setLevel(logging.DEBUG)
    return logger


def _fmt_json(data):
    if data is None:
        return "None"
    try:
        return json.dumps(data, indent=2, ensure_ascii=False)
    except (TypeError, ValueError):
        return str(data)


def log_request(logger, method, url, headers=None, body=None):
    logger.info(f">>> REQUEST: {method} {url}")
    if headers:
        safe = {k: "***" if "token" in k.lower() else v for k, v in headers.items()}
        logger.debug(f"Headers: {safe}")
    if body:
        safe_body = body.copy() if isinstance(body, dict) else body
        if isinstance(safe_body, dict) and "user" in safe_body:
            u = safe_body["user"].copy()
            if "password" in u:
                u["password"] = "***"
            safe_body["user"] = u
        logger.debug(f"Body: {_fmt_json(safe_body)}")


def log_response(logger, response):
    logger.info(f"<<< RESPONSE: {response.status_code} {response.reason}")
    try:
        body = response.json()
        if isinstance(body, dict) and "User-Token" in body:
            body = body.copy()
            body["User-Token"] = "***"
        logger.debug(f"Body: {_fmt_json(body)}")
    except ValueError:
        logger.debug(f"Body: {response.text[:500]}")
