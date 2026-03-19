"""CRUD operations para Contas Bancárias"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import ContaBancaria
from app.schemas import ContaBancariaCreate, ContaBancariaUpdate

def get_conta(db: Session, conta_id: int, usuario_id: int) -> Optional[ContaBancaria]:
    """Busca uma conta bancária específica do usuário"""
    return db.query(ContaBancaria).filter(
        ContaBancaria.id == conta_id,
        ContaBancaria.usuario_id == usuario_id
    ).first()

def get_contas_bancarias(
    db: Session, 
    usuario_id: int,
    skip: int = 0, 
    limit: int = 100,
    ativas_only: bool = True
) -> List[ContaBancaria]:
    """Lista contas bancárias do usuário"""
    query = db.query(ContaBancaria).filter(ContaBancaria.usuario_id == usuario_id)
    
    if ativas_only:
        query = query.filter(ContaBancaria.is_active == True)
    
    return query.offset(skip).limit(limit).all()

def create_conta_bancaria(
    db: Session, 
    conta: ContaBancariaCreate, 
    usuario_id: int
) -> ContaBancaria:
    """Cria uma nova conta bancária"""
    db_conta = ContaBancaria(
        **conta.model_dump(),
        usuario_id=usuario_id
    )
    db.add(db_conta)
    db.commit()
    db.refresh(db_conta)
    return db_conta

def update_conta_bancaria(
    db: Session, 
    conta_id: int, 
    conta_update: ContaBancariaUpdate, 
    usuario_id: int
) -> Optional[ContaBancaria]:
    """Atualiza uma conta bancária existente"""
    db_conta = get_conta(db, conta_id, usuario_id)
    if not db_conta:
        return None
    
    update_data = conta_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_conta, field, value)
    
    db.commit()
    db.refresh(db_conta)
    return db_conta

def delete_conta_bancaria(db: Session, conta_id: int, usuario_id: int) -> bool:
    """Deleta (desativa) uma conta bancária"""
    db_conta = get_conta(db, conta_id, usuario_id)
    if not db_conta:
        return False
    
    db_conta.is_active = False
    db.commit()
    return True
