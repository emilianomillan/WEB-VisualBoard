from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
import json


class Settings(BaseSettings):
    PROJECT_NAME: str = "Visual Board API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    SECRET_KEY: str
    DEBUG: bool = False
    
    DATABASE_URL: str
    
    UNSPLASH_ACCESS_KEY: str
    
    CORS_ORIGINS: List[AnyHttpUrl] = []

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'CORS_ORIGINS':
                return json.loads(raw_val)
            return raw_val


settings = Settings()