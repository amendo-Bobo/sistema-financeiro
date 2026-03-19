"""Router de Autenticação"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.security import (
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_active_user
)
from app.crud.usuarios import create_user, get_user_by_email
from app.models import User
from app.schemas import UserCreate, User, Token
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Registra um novo usuário"""
    # Verifica se email já existe
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email já cadastrado"
        )
    
    return create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login do usuário e retorno do token JWT"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Retorna dados do usuário logado"""
    return current_user
