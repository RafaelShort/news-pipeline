from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    elasticsearch_uri: str
    elasticsearch_index: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
