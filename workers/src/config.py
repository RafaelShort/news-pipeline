from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    kafka_topic_raw: str
    kafka_topic_processed: str
    kafka_group_id: str

    elasticsearch_uri: str
    elasticsearch_index: str

    nlp_model_ner: str = "pt_core_news_lg"
    nlp_model_classifier: str = "cross-encoder/nli-MiniLM2-L6-H768"
    nlp_model_summarizer: str = "t5-small"  # ← ~242MB vs 1.2GB

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
