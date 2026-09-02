"""
FOODARA AI - Logging Configuration
Setup de logging estructurado y consistente.
"""

import logging
import json
from datetime import datetime, timezone
from typing import Any, Dict
import sys

from app.core.config import settings


class JSONFormatter(logging.Formatter):
    """Formatter que emite logs en JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        request_id = getattr(logging, "_foodara_request_id", None)
        if request_id:
            log_data["request_id"] = request_id

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> None:
    """Configurar logging global de FOODARA."""
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.log_level))

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.log_level))

    if settings.log_format == "json":
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Obtener logger nombrado."""
    return logging.getLogger(name)
