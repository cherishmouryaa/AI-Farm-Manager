from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Farm Manager"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    
    # Secrets
    SECRET_KEY: str = "secret-key-change-in-production"
    OPENAI_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None
    
    # DB
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
