"""Router de Transações Financeiras"""
from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.security import get_current_active_user
from app.models import User, TipoTransacao, CategoriaTransacao
from app.schemas import (
    Transacao, 
    TransacaoCreate, 
    TransacaoUpdate,
    TransacaoResumo,
    GraficoDados
)
from app.crud.transacoes import (
    get_transacoes,
    get_transacao,
    create_transacao,
    update_transacao,
    delete_transacao,
    get_resumo_periodo,
    get_gastos_por_categoria
)

router = APIRouter(prefix="/transacoes", tags=["Transações"])

@router.get("/", response_model=List[Transacao])
def listar_transacoes(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    tipo: Optional[TipoTransacao] = None,
    categoria: Optional[CategoriaTransacao] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Lista todas as transações do usuário com filtros opcionais"""
    return get_transacoes(
        db=db,
        usuario_id=current_user.id,
        skip=skip,
        limit=limit,
        data_inicio=data_inicio,
        data_fim=data_fim,
        tipo=tipo,
        categoria=categoria
    )

@router.post("/", response_model=Transacao, status_code=201)
def criar_transacao(
    transacao: TransacaoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Cria uma nova transação"""
    return create_transacao(db=db, transacao=transacao, usuario_id=current_user.id)

@router.get("/{transacao_id}", response_model=Transacao)
def obter_transacao(
    transacao_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Obtém detalhes de uma transação específica"""
    transacao = get_transacao(db, transacao_id, current_user.id)
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transacao

@router.put("/{transacao_id}", response_model=Transacao)
def atualizar_transacao(
    transacao_id: int,
    transacao_update: TransacaoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Atualiza uma transação existente"""
    transacao = update_transacao(
        db=db, 
        transacao_id=transacao_id, 
        transacao_update=transacao_update,
        usuario_id=current_user.id
    )
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return transacao

@router.delete("/{transacao_id}")
def remover_transacao(
    transacao_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Remove uma transação"""
    sucesso = delete_transacao(db, transacao_id, current_user.id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Transação não encontrada")
    return {"message": "Transação removida com sucesso"}

@router.get("/resumo/mensal", response_model=TransacaoResumo)
def resumo_mensal(
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna resumo financeiro do mês especificado (ou mês atual)"""
    hoje = date.today()
    ano = ano or hoje.year
    mes = mes or hoje.month
    
    data_inicio = date(ano, mes, 1)
    if mes == 12:
        data_fim = date(ano + 1, 1, 1) - timedelta(days=1)
    else:
        data_fim = date(ano, mes + 1, 1) - timedelta(days=1)
    
    resumo = get_resumo_periodo(db, current_user.id, data_inicio, data_fim)
    
    # Conta transações
    transacoes = get_transacoes(db, current_user.id, data_inicio=data_inicio, data_fim=data_fim)
    
    return TransacaoResumo(
        total_entradas=resumo["total_entradas"],
        total_saidas=resumo["total_saidas"],
        saldo=resumo["saldo"],
        quantidade_transacoes=len(transacoes)
    )

@router.get("/graficos/gastos-por-categoria", response_model=GraficoDados)
def grafico_gastos_categoria(
    ano: Optional[int] = None,
    mes: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna dados para gráfico de gastos por categoria"""
    hoje = date.today()
    ano = ano or hoje.year
    mes = mes or hoje.month
    
    data_inicio = date(ano, mes, 1)
    if mes == 12:
        data_fim = date(ano + 1, 1, 1) - timedelta(days=1)
    else:
        data_fim = date(ano, mes + 1, 1) - timedelta(days=1)
    
    dados = get_gastos_por_categoria(db, current_user.id, data_inicio, data_fim)
    
    # Cores para cada categoria
    cores_categoria = {
        "alimentacao": "#FF6384",
        "transporte": "#36A2EB",
        "moradia": "#FFCE56",
        "saude": "#4BC0C0",
        "educacao": "#9966FF",
        "lazer": "#FF9F40",
        "vestuario": "#FF6384",
        "utilidades": "#C9CBCF",
        "outros": "#666666"
    }
    
    labels = [d["categoria"].value for d in dados]
    valores = [d["total"] for d in dados]
    cores = [cores_categoria.get(d["categoria"].value, "#666666") for d in dados]
    
    return GraficoDados(labels=labels, valores=valores, cores=cores)
