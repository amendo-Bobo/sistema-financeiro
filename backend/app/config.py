"""Configurações da aplicação"""
import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configurações principais da aplicação"""
    
    # Configurações da aplicação
    APP_NAME: str = "Sistema Financeiro"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Configurações do banco de dados
    DATABASE_URL: Optional[str] = None
    
    # Configurações de segurança
    SECRET_KEY: str = "sua-chave-secreta-aqui-mude-em-producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configurações do ambiente
    ENVIRONMENT: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """Retorna as configurações da aplicação"""
    return Settings()

# Instância global das configurações
settings = get_settings()
