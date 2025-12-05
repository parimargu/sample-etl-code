from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "NLP Search API"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database
    SQLITE_DB_PATH: str = "/home/marguai/work/workarea/code/Google_Antigravity/nlp_etl_pipeline_1/data/processed/vector_db.sqlite"
    
    # Model
    EMBEDDING_MODEL: str = "sentence-transformers/sentence-t5-base"

    class Config:
        case_sensitive = True

settings = Settings()
