"""Router de Dashboard e Estatísticas"""
from datetime import date, timedelta
from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.auth.security import get_current_active_user
from app.models import User, Transacao, TipoTransacao, OrcamentoMensal
from app.schemas import DashboardResumo, OrcamentoResumo
from app.crud.transacoes import get_transacoes, get_resumo_periodo

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/resumo", response_model=DashboardResumo)
def dashboard_resumo(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna resumo completo para o dashboard"""
    hoje = date.today()
    
    # Mês atual
    data_inicio = date(hoje.year, hoje.month, 1)
    if hoje.month == 12:
        data_fim = date(hoje.year + 1, 1, 1) - timedelta(days=1)
    else:
        data_fim = date(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
    
    # Resumo do mês
    resumo = get_resumo_periodo(db, current_user.id, data_inicio, data_fim)
    
    # Transações recentes (últimas 5)
    transacoes_recentes = get_transacoes(
        db, current_user.id, limit=5
    )
    
    # Orçamento vs Real
    orcamentos = db.query(OrcamentoMensal).filter(
        OrcamentoMensal.usuario_id == current_user.id,
        OrcamentoMensal.ano == hoje.year,
        OrcamentoMensal.mes == hoje.month
    ).all()
    
    alertas = []
    for orc in orcamentos:
        # Calcula gasto real na categoria
        gasto = db.query(func.sum(Transacao.valor)).filter(
            Transacao.usuario_id == current_user.id,
            Transacao.categoria == orc.categoria,
            Transacao.tipo == TipoTransacao.SAIDA,
            Transacao.data >= data_inicio,
            Transacao.data <= data_fim
        ).scalar() or 0
        
        diferenca = orc.valor_orcado - gasto
        percentual = (gasto / orc.valor_orcado * 100) if orc.valor_orcado > 0 else 0
        
        if percentual > 80:  # Alerta se gastou mais de 80% do orçado
            alertas.append(OrcamentoResumo(
                categoria=orc.categoria,
                orcado=orc.valor_orcado,
                gasto_real=gasto,
                diferenca=diferenca,
                percentual_usado=round(percentual, 1)
            ))
    
    return DashboardResumo(
        saldo_atual=resumo["saldo"],
        total_entradas_mes=resumo["total_entradas"],
        total_saidas_mes=resumo["total_saidas"],
        balanco_mes=resumo["total_entradas"] - resumo["total_saidas"],
        transacoes_recentes=transacoes_recentes,
        alertas_orcamento=alertas
    )

@router.get("/evolucao-mensal")
def evolucao_mensal(
    meses: int = Query(6, ge=1, le=24),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna evolução financeira dos últimos N meses"""
    hoje = date.today()
    resultado = []
    
    for i in range(meses - 1, -1, -1):
        # Calcula o mês
        ano = hoje.year
        mes = hoje.month - i
        
        while mes <= 0:
            mes += 12
            ano -= 1
        
        data_inicio = date(ano, mes, 1)
        if mes == 12:
            data_fim = date(ano + 1, 1, 1) - timedelta(days=1)
        else:
            data_fim = date(ano, mes + 1, 1) - timedelta(days=1)
        
        resumo = get_resumo_periodo(db, current_user.id, data_inicio, data_fim)
        
        resultado.append({
            "ano": ano,
            "mes": mes,
            "nome_mes": data_inicio.strftime("%b/%Y"),
            "entradas": float(resumo["total_entradas"]),
            "saidas": float(resumo["total_saidas"]),
            "saldo": float(resumo["saldo"])
        })
    
    return resultado
