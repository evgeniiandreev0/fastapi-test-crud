import os

SECRET_KEY: str = os.getenv("SECRET_KEY", "replace_with_more_secure_key")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@postgres:5432/task_manager")
DEFAULT_EXPIRE_TIME: int = int(os.getenv("DEFAULT_EXPIRE_TIME", 60))
