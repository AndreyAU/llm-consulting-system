from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "bot-service"
    env: str = "local"

    telegram_bot_token: str

    jwt_secret: str
    jwt_alg: str = "HS256"

    redis_url: str
    rabbitmq_url: str

    openrouter_api_key: str
    openrouter_base_url: str
    openrouter_model: str
    openrouter_site_url: str
    openrouter_app_name: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
