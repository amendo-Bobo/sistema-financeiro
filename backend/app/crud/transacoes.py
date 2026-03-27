"""CRUD operations para Transações"""
from datetime import date
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Transacao, TipoTransacao, CategoriaTransacao
from app.schemas import TransacaoCreate, TransacaoUpdate

def get_transacao(db: Session, transacao_id: int, usuario_id: int) -> Optional[Transacao]:
    """Busca uma transação específica do usuário"""
    return db.query(Transacao).filter(
        Transacao.id == transacao_id,
        Transacao.usuario_id == usuario_id
    ).first()

def get_transacoes(
    db: Session, 
    usuario_id: int,
    skip: int = 0, 
    limit: int = 100,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    tipo: Optional[TipoTransacao] = None,
    categoria: Optional[CategoriaTransacao] = None
) -> List[Transacao]:
    """Lista transações do usuário com filtros opcionais"""
    query = db.query(Transacao).filter(Transacao.usuario_id == usuario_id)
    
    if data_inicio:
        query = query.filter(Transacao.data >= data_inicio)
    if data_fim:
        query = query.filter(Transacao.data <= data_fim)
    if tipo:
        query = query.filter(Transacao.tipo == tipo)
    if categoria:
        query = query.filter(Transacao.categoria == categoria)
    
    return query.order_by(Transacao.data.desc()).offset(skip).limit(limit).all()

def create_transacao(db: Session, transacao: TransacaoCreate, usuario_id: int) -> Transacao:
    """Cria uma nova transação"""
    # Remover usuario_id do dict para evitar duplicação
    transacao_data = transacao.model_dump()
    transacao_data.pop('usuario_id', None)
    
    # Conversão direta como no login
    if 'tipo' in transacao_data:
        transacao_data['tipo'] = str(transacao_data['tipo']).lower()
    if 'categoria' in transacao_data:
        transacao_data['categoria'] = str(transacao_data['categoria']).lower()
    
    print(f"DEBUG: Final tipo: '{transacao_data['tipo']}'")
    print(f"DEBUG: Final categoria: '{transacao_data['categoria']}'")
    
    db_transacao = Transacao(
        **transacao_data,
        usuario_id=usuario_id
    )
    db.add(db_transacao)
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

def update_transacao(
    db: Session, 
    transacao_id: int, 
    transacao_update: TransacaoUpdate, 
    usuario_id: int
) -> Optional[Transacao]:
    """Atualiza uma transação existente"""
    db_transacao = get_transacao(db, transacao_id, usuario_id)
    if not db_transacao:
        return None
    
    update_data = transacao_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transacao, field, value)
    
    db.commit()
    db.refresh(db_transacao)
    return db_transacao

def delete_transacao(db: Session, transacao_id: int, usuario_id: int) -> bool:
    """Deleta uma transação"""
    db_transacao = get_transacao(db, transacao_id, usuario_id)
    if not db_transacao:
        return False
    
    db.delete(db_transacao)
    db.commit()
    return True

def get_resumo_periodo(
    db: Session,
    usuario_id: int,
    data_inicio: date,
    data_fim: date
) -> dict:
    """Retorna resumo financeiro de um período"""
    entradas = db.query(func.sum(Transacao.valor)).filter(
        Transacao.usuario_id == usuario_id,
        Transacao.tipo == TipoTransacao.ENTRADA,
        Transacao.data >= data_inicio,
        Transacao.data <= data_fim
    ).scalar() or 0
    
    saidas = db.query(func.sum(Transacao.valor)).filter(
        Transacao.usuario_id == usuario_id,
        Transacao.tipo == TipoTransacao.SAIDA,
        Transacao.data >= data_inicio,
        Transacao.data <= data_fim
    ).scalar() or 0
    
    return {
        "total_entradas": entradas,
        "total_saidas": saidas,
        "saldo": entradas - saidas
    }

def get_gastos_por_categoria(
    db: Session,
    usuario_id: int,
    data_inicio: date,
    data_fim: date
) -> List[dict]:
    """Retorna gastos agrupados por categoria"""
    result = db.query(
        Transacao.categoria,
        func.sum(Transacao.valor).label("total")
    ).filter(
        Transacao.usuario_id == usuario_id,
        Transacao.tipo == TipoTransacao.SAIDA,
        Transacao.data >= data_inicio,
        Transacao.data <= data_fim
    ).group_by(Transacao.categoria).all()
    
    return [{"categoria": r.categoria, "total": r.total} for r in result]
