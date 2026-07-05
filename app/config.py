from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    mongodb_uri: str
    jwt_secret: str
    jwt_expire_minutes: int = 1440  # 24h

    class Config:
        env_file = ".env"


settings = Settings()
