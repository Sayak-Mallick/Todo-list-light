from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


# Load application settings from environment variables.
class Settings(BaseSettings):
    # DATABASE_URL: str
    database_hostname: str
    database_port: int = 5432
    database_name: str
    database_username: str
    database_password: str
    database_use_ssl: bool = True
    database_pool_size: int = 5
    database_max_overflow: int = 5

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

    @property
    def database_url(self) -> URL:
        return URL.create(
            "postgresql+psycopg",
            username=self.database_username,
            password=self.database_password,
            host=self.database_hostname,
            port=self.database_port,
            database=self.database_name,
            query={
                "sslmode": "require",
                "channel_binding": "require",
            },
        )


# Create a settings instance for the application.
settings = Settings()