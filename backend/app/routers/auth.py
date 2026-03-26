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
    try:
        print(f"DEBUG: Register attempt for email: {user.email}")
        print(f"DEBUG: User data: {user}")
        
        # Verifica se email já existe
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            print(f"DEBUG: Email already exists: {user.email}")
            raise HTTPException(
                status_code=400,
                detail="Email já cadastrado"
            )
        
        print(f"DEBUG: Creating user...")
        result = create_user(db=db, user=user)
        print(f"DEBUG: User created successfully: {result.email}")
        return result
        
    except Exception as e:
        print(f"DEBUG: Register error: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao criar usuário: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login do usuário e retorno do token JWT"""
    try:
        print(f"DEBUG: Login attempt for username: {form_data.username}")
        print(f"DEBUG: Username type: {type(form_data.username)}")
        print(f"DEBUG: Username value: '{str(form_data.username)}'")
        
        user = authenticate_user(db, form_data.username, form_data.password)
        if not user:
            print(f"DEBUG: Authentication failed for: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        print(f"DEBUG: User authenticated: {user.email}")
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        
        print(f"DEBUG: Token created successfully")
        return {"access_token": access_token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Login error: {str(e)}")
        print(f"DEBUG: Error type: {type(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer login: {str(e)}"
        )

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Retorna dados do usuário logado"""
    return current_user
