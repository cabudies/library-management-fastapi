from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Library Management System"
    VERSION: str = "1.0.0"
    # API_V1_STR: str = "/api/v1"
    API_V1_STR: str = "/api"
    
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    # POSTGRES_PASSWORD: str = "password"
    POSTGRES_PASSWORD: str = "gurjas"
    POSTGRES_DB: str = "library_db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    JWT_SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    @property
    def get_database_url(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()
