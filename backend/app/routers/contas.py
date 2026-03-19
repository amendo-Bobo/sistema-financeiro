"""Router de Contas Bancárias"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.security import get_current_active_user
from app.models import User
from app.schemas import ContaBancaria, ContaBancariaCreate, ContaBancariaUpdate
from app.crud.contas import (
    get_contas_bancarias,
    get_conta,
    create_conta_bancaria,
    update_conta_bancaria,
    delete_conta_bancaria
)

router = APIRouter(prefix="/contas", tags=["Contas Bancárias"])

@router.get("/", response_model=List[ContaBancaria])
def listar_contas(
    ativas_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista contas bancárias do usuário"""
    return get_contas_bancarias(
        db=db, 
        usuario_id=current_user.id,
        ativas_only=ativas_only
    )

@router.post("/", response_model=ContaBancaria, status_code=201)
def criar_conta(
    conta: ContaBancariaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria uma nova conta bancária"""
    return create_conta_bancaria(
        db=db, 
        conta=conta, 
        usuario_id=current_user.id
    )

@router.get("/{conta_id}", response_model=ContaBancaria)
def obter_conta(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém detalhes de uma conta bancária"""
    conta = get_conta(db, conta_id, current_user.id)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta

@router.put("/{conta_id}", response_model=ContaBancaria)
def atualizar_conta(
    conta_id: int,
    conta_update: ContaBancariaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza uma conta bancária"""
    conta = update_conta_bancaria(
        db=db,
        conta_id=conta_id,
        conta_update=conta_update,
        usuario_id=current_user.id
    )
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta

@router.delete("/{conta_id}")
def remover_conta(
    conta_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove (desativa) uma conta bancária"""
    sucesso = delete_conta_bancaria(db, conta_id, current_user.id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return {"message": "Conta removida com sucesso"}
