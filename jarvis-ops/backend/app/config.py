from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str = ''
    database_url: str = ''
    shopify_api_key: str = ''
    shopify_api_secret: str = ''
    slack_webhook_url: str = ''

    class Config:
        env_file = '.env'

settings = Settings()
