from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ORIGINS: list[str]
    ALLOWED_HOSTS: list[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()