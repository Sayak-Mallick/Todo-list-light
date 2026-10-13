from pydantic_settings import BaseSettings, SettingsConfigDict


# Load application settings from environment variables.
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",     # Read environment variables from the .env file.
        case_sensitive=False,  # Environment variable names are case-insensitive.
        extra="ignore",  # Ignore unknown configuration fields.
        validate_default=True,  # Validate default values as well.
        frozen=True,  # Prevent changing settings after initialization.
    )


# Create a settings instance for the application.
settings = Settings()