"""
FOODARA AI - Core Configuration
Centraliza todas las configuraciones de la aplicación.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """
    Configuración principal de FOODARA AI.
    Las variables se cargan desde .env
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ============================================
    # APPLICATION
    # ============================================
    app_name: str = "FOODARA AI"
    app_version: str = "2.0.0"
    app_env: str = "development"
    debug: bool = False

    # ============================================
    # API
    # ============================================
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_prefix: str = "/api/v1"

    # ============================================
    # DATABASE
    # ============================================
    db_engine: str = "postgresql"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "foodara"
    db_password: str = ""
    db_name: str = "foodara_db"

    @property
    def database_url(self) -> str:
        """Construir URL de base de datos async"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def database_url_sync(self) -> str:
        """Construir URL de base de datos sincrónica (para Alembic)"""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    # ============================================
    # SECURITY
    # ============================================
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # ============================================
    # AI PROVIDERS
    # ============================================
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_enabled: bool = False

    anthropic_api_key: str = ""
    anthropic_model: str = "claude-3-opus-20240229"
    anthropic_enabled: bool = True

    local_ai_enabled: bool = False
    local_ai_url: str = "http://localhost:8001"

    default_ai_provider: str = "anthropic"

    # ============================================
    # VISION & OCR
    # ============================================
    vision_enabled: bool = False
    vision_provider: str = "mock"
    vision_confidence_threshold: float = 0.7

    ocr_enabled: bool = False
    ocr_provider: str = "mock"

    # ============================================
    # CORS
    # ============================================
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]

    # ============================================
    # LOGGING
    # ============================================
    log_level: str = "INFO"
    log_format: str = "json"

    # ============================================
    # RATE LIMITING
    # ============================================
    rate_limit_enabled: bool = True
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    # ============================================
    # ARGENTINA DEFAULTS
    # ============================================
    currency: str = "ARS"
    language: str = "es"
    timezone: str = "America/Argentina/Buenos_Aires"
    country: str = "AR"

    # ============================================
    # VALIDACIÓN DE SEGURIDAD EN ARRANQUE
    # ============================================

    def validate_security(self) -> None:
        """
        Validar que la configuración sea segura en el entorno actual.
        Lanza un error si la configuración podría comprometer el sistema
        en producción. Llamar al arranque de la aplicación.
        """
        import logging

        if self.app_env.lower() in ("production", "prod") and not self.secret_key:
            raise RuntimeError(
                "SECRET_KEY no configurado. FOODARA no arranca en producción "
                "sin una clave secreta fuerte. Defina SECRET_KEY en el entorno."
            )
        if not self.debug and not self.secret_key:
            raise RuntimeError(
                "SECRET_KEY no configurado. Defina SECRET_KEY en el entorno."
            )
        if self.debug and not self.secret_key:
            logging.getLogger(__name__).warning(
                "SECRET_KEY no configurado. Usando clave de desarrollo NO segura. "
                "NUNCA ejecutar así en producción."
            )
            self.secret_key = "dev-only-insecure-secret-key-do-not-use-in-prod"


# Instancia global de configuración
settings = Settings()
