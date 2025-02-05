from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"  # Update as needed
    APP_NAME: str = "My FastAPI App"
    DEBUG: bool = True

settings = Settings()
