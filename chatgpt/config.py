from openai import AsyncOpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAICredentials(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='OPENAI_')

    API_KEY: str


credentials = OpenAICredentials()
client = AsyncOpenAI(api_key=credentials.API_KEY)
