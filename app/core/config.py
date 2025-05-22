from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Класс для загрузки и валидации конфигурационных параметров из окружения
    """
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_endpoint_url: str
    s3_bucket_name: str
    groq_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
