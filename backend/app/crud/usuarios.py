"""CRUD operations para Usuários"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.auth.security import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Busca usuário pelo ID"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Busca usuário pelo email"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Cria um novo usuário"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        nome=user.nome,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(
    db: Session, 
    user_id: int, 
    user_update: UserUpdate
) -> Optional[User]:
    """Atualiza dados do usuário"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    """Deleta um usuário (soft delete)"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db_user.is_active = False
    db.commit()
    return True

def change_password(db: Session, user_id: int, new_password: str) -> bool:
    """Altera a senha do usuário"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db_user.hashed_password = get_password_hash(new_password)
    db.commit()
    return True
