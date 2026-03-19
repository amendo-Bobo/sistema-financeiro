"""Configurações da aplicação"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Configurações do sistema de finanças"""
    
    # App
    APP_NAME: str = "Sistema de Finanças Pessoais"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "sqlite:///./financas.db"
    
    # Security
    SECRET_KEY: str = "sua-chave-secreta-mude-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Plaid (para integração bancária futura)
    PLAID_CLIENT_ID: str | None = None
    PLAID_SECRET: str | None = None
    PLAID_ENV: str = "sandbox"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
