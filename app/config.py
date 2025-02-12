from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    ACTIVE_CAMPAIGN_ACCOUNT_NAME: str
    ACTIVE_CAMPAIGN_API_TOKEN: str
    ES_HOST: str


def get_settings() -> Settings:
    return Settings()
