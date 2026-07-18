from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_host: str = "localhost"
    database_port: int = 5432
    database_name: str = "car_dealership_db"
    database_user: str = "postgres"
    database_password: str = ""
    database_url: str | None = None
    secret_key: str = "change-this-development-secret"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            "postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}@{self.database_host}:"
            f"{self.database_port}/{self.database_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
