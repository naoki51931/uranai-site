from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    weaviate_url: str = "http://localhost:8080"
    jwt_secret_key: str
    jwt_expire_minutes: int = 1440
    admin_username: str = "admin"
    admin_password: str = "change-me-admin"
    monthly_free_reading_limit: int = 30
    monthly_limit_exempt_emails: str = ""
    stripe_secret_key: str
    stripe_webhook_secret: str = ""
    stripe_price_id: str
    app_base_url: str = "http://localhost"
    billing_enabled: bool = True
    password_reset_expire_minutes: int = 60
    followup_delay_days: int = 14
    followup_poll_seconds: int = 60
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_use_tls: bool = True
    openai_api_key: str = ""
    openai_model: str = ""
    ai_model: str = ""
    openai_base_url: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
