from pydantic_settings import BaseSettings, SettingsConfigDict


# Load application settings from environment variables.
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Read environment variables from the .env file.
    model_config = SettingsConfigDict(env_file=".env")


# Create a settings instance for the application.
settings = Settings()