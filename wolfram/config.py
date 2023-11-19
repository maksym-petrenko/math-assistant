from pydantic_settings import BaseSettings


class WolframCredentials(BaseSettings):
    APP_ID: str


credentials = WolframCredentials()
