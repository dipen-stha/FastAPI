from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ORIGINS: str

    class Config:
        env_file = ".env"

settings = Settings()