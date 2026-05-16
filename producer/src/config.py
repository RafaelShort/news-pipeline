from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    kafka_topic_raw: str
    rss_fetch_interval: int = 300

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
