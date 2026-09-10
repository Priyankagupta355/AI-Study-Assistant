from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    groq_api_key: str


    llm_model: str = "openai/gpt-oss-120b"
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_db_path: str = "./data/chroma_db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
