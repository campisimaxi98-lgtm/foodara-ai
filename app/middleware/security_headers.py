"""
FOODARA AI - Security Headers Middleware
Agrega cabeceras de seguridad HTTP recomendadas.
"""

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Cabeceras de seguridad estándar: HSTS, X-Content-Type-Options,
    X-Frame-Options, Referrer-Policy, X-XSS-Protection.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        # HSTS solo sobre HTTPS
        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains"
            )

        return response
