import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_ID               : str = os.getenv("DB_ID")
    NOTION_TOKEN        : str = os.getenv("NOTION_TOKEN")
    SLACK_TOKEN         : str = os.getenv("SLACK_TOKEN")
    CLOVA_CLIENT_ID     : str = os.getenv("CLIENT_ID")
    CLOVA_CLIENT_SECRET : str = os.getenv("CLIENT_SECRET")


settings = Settings()
