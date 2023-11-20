from pydantic_settings import BaseSettings


class MathpixCredentials(BaseSettings):
    APP_ID: str
    APP_KEY: str

credentials = MathpixCredentials()
