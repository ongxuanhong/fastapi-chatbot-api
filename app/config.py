import os

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://admin:admin@localhost:5432/public"
)
# DATABASE_URL = "postgresql://admin:admin@localhost:5432/public"
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
ALGORITHM = "HS256"
