"""
FOODARA AI - Request ID Middleware
Asigna un ID de correlación a cada request para trazar logs de punta a punta.
"""

import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware que inyecta un request_id único en cada request.
    El ID se propaga a los logs a través del contexto y la cabecera de respuesta.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())

        # Contexto temporal para asociar el request_id a los logs de este request
        old_request_id = getattr(logging, "_foodara_request_id", None)
        logging._foodara_request_id = request_id  # type: ignore[attr-defined]

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        # Restaurar contexto anterior
        if old_request_id is None:
            logging._foodara_request_id = None  # type: ignore[attr-defined]
        else:
            logging._foodara_request_id = old_request_id  # type: ignore[attr-defined]

        return response
