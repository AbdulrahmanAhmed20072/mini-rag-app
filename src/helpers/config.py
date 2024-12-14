from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class Settings( BaseSettings ):
    
    APP_NAME: str
    APP_VERSION: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int # 512 KB

    MONGODB_URL: str
    MONGODB_DATABASE: str

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()