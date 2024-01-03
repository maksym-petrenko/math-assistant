from pydantic_settings import BaseSettings, SettingsConfigDict


class MathpixCredentials(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MATHPIX_')

    APP_ID: str
    APP_KEY: str

credentials = MathpixCredentials()
