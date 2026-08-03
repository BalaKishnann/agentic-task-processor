import json
import logging
import sys
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """
    Formats log records as single-line JSON, so logs are easy to
    ingest into any log aggregator (CloudWatch, Datadog, ELK, etc.)
    without a separate parsing step.
    """

    def format(self, record: logging.LogRecord) -> str:

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Attach any extra fields passed via logger.info(..., extra={...})
        # e.g. request_id, duration_ms, tool_name, status
        standard_keys = set(
            logging.LogRecord("", 0, "", 0, "", (), None).__dict__.keys()
        )

        for key, value in record.__dict__.items():
            if key not in standard_keys and key != "message":
                log_entry[key] = value

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry)


def configure_logging(log_level: str, json_format: bool = True) -> None:

    handler = logging.StreamHandler(stream=sys.stdout)

    if json_format:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))
    root_logger.handlers = [handler]
