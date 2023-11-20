from pydantic_settings import BaseSettings


class WolframCredentials(BaseSettings):
    APP_ID: str

class MathpixCredentials(BaseSettings):
    APP_ID: str
    APP_KEY: str

wolfram_credentials = WolframCredentials()
mathpix_credentials = MathpixCredentials()
