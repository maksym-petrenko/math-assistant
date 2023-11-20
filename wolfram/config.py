from pydantic_settings import BaseSettings, SettingsConfigDict


class WolframCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='WOLFRAM_')

    APP_ID: str

credentials = WolframCredentials()
