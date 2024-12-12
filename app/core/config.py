from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Gamified Chat"
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"


settings = Settings()
