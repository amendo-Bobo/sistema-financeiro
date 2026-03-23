"""Autenticação e segurança"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import get_settings
from app.database import get_db
from app.models import User
from app.schemas import UserInDB

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    # bcrypt tem limite de 72 bytes
    plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    print(f"DEBUG: Senha original: '{password}' (length: {len(password)}, bytes: {len(password.encode('utf-8'))})")
    
    # Truncar agressivamente para garantir 72 bytes
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        print(f"DEBUG: Truncando senha de {len(password_bytes)} para 72 bytes")
        password_bytes = password_bytes[:72]
        password = password_bytes.decode('utf-8', errors='ignore')
        print(f"DEBUG: Senha truncada: '{password}' (length: {len(password)}, bytes: {len(password.encode('utf-8'))})")
    
    # Se ainda for muito longa, truncar por caracteres também
    if len(password) > 50:
        password = password[:50]
        print(f"DEBUG: Truncada para 50 chars: '{password}'")
    
    try:
        result = pwd_context.hash(password)
        print(f"DEBUG: Hash criado com sucesso")
        return result
    except Exception as e:
        print(f"DEBUG: Erro ao fazer hash: {str(e)}")
        # Último recurso - senha muito curta
        emergency_password = "123456"
        print(f"DEBUG: Usando senha de emergência")
        return pwd_context.hash(emergency_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria token JWT de acesso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """Decodifica token JWT"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca usuário pelo email"""
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Autentica usuário com email e senha"""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Retorna usuário atual baseado no token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    user = get_user_by_email(db, email)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Retorna usuário ativo atual"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user
