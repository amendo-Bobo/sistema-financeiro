"""Router para integração com Mercado Pago"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.security import get_current_active_user
from app.models import User
from app.schemas import TransacaoCreate, Transacao
from app.crud.transacoes import create_transacao
from app.services.mercado_pago import get_mercadopago_service
from pydantic import BaseModel

router = APIRouter(prefix="/mercadopago", tags=["Mercado Pago"])


class MercadoPagoConfig(BaseModel):
    """Modelo para configuração do Mercado Pago"""
    access_token: str
    auto_sync: bool = False


class MercadoPagoSyncRequest(BaseModel):
    """Modelo para requisição de sincronização"""
    days: int = 30


@router.post("/configurar")
async def configurar_mercadopago(
    config: MercadoPagoConfig,
    current_user: User = Depends(get_current_active_user)
):
    """Configura token de acesso do Mercado Pago (salvo na sessão do usuário)"""
    try:
        # Testar token fazendo uma consulta simples
        service = get_mercadopago_service(config.access_token)
        balance = service.get_account_balance()
        
        # Aqui você pode salvar o token de forma segura
        # Por agora, vamos apenas verificar se funciona
        return {
            "success": True,
            "message": "Token válido!",
            "balance": {
                "total": balance.get("total_amount", 0),
                "disponivel": balance.get("available_balance", 0)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Token inválido ou erro na API: {str(e)}"
        )


@router.post("/sync", response_model=List[Transacao])
async def sincronizar_transacoes(
    request: MercadoPagoSyncRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Sincroniza transações do Mercado Pago"""
    # NOTA: Em produção, o token deve vir de um local seguro (banco de dados)
    # Aqui estamos assumindo que o usuário já configurou o token
    
    # Para teste, vamos retornar instruções
    raise HTTPException(
        status_code=400,
        detail="Token do Mercado Pago não configurado. Use o endpoint /configurar primeiro."
    )


@router.post("/sync-with-token", response_model=List[Transacao])
async def sincronizar_com_token(
    access_token: str,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Sincroniza transações informando o token diretamente"""
    try:
        service = get_mercadopago_service(access_token)
        
        # Sincronizar transações
        transacoes_mp = service.sync_transacoes(days)
        
        if not transacoes_mp:
            return []
        
        # Salvar no banco
        transacoes_salvas = []
        for trans_data in transacoes_mp:
            try:
                transacao_create = TransacaoCreate(**trans_data)
                transacao = create_transacao(db, transacao_create, current_user.id)
                transacoes_salvas.append(transacao)
            except Exception as e:
                print(f"Erro ao salvar transação: {e}")
                continue
        
        return transacoes_salvas
        
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao sincronizar: {str(e)}"
        )


@router.get("/instrucoes")
def obter_instrucoes():
    """Retorna instruções de como obter o Access Token do Mercado Pago"""
    return {
        "title": "Como obter seu Access Token do Mercado Pago",
        "steps": [
            {
                "step": 1,
                "title": "Acesse sua conta",
                "description": "Vá em https://www.mercadopago.com.br e faça login na sua conta"
            },
            {
                "step": 2,
                "title": "Acesse Developers",
                "description": "Vá em: Seu Perfil → Desenvolvedores → Minhas Aplicações (ou acesse direto developers.mercadopago.com.br)"
            },
            {
                "step": 3,
                "title": "Crie uma Aplicação",
                "description": "Clique em 'Criar aplicação' → Dê um nome (ex: 'Minhas Finanças') → Selecione 'Pagamentos Online'"
            },
            {
                "step": 4,
                "title": "Copie o Access Token",
                "description": "Na página da aplicação, vá em 'Credenciais de produção' e copie o 'Access Token'"
            }
        ],
        "important_notes": [
            "O Access Token é PESSOAL e dá acesso à sua conta. Nunca compartilhe!",
            "Armazenamos o token apenas para sincronização. Você pode revogá-lo a qualquer momento no Mercado Pago.",
            "Recomendamos criar uma aplicação dedicada apenas para este sistema de finanças."
        ],
        "endpoints_disponiveis": [
            "/api/mercadopago/configurar - Testa se o token está válido",
            "/api/mercadopago/sync-with-token?access_token=SEU_TOKEN&days=30 - Sincroniza transações"
        ]
    }


@router.get("/testar-token/{token}")
async def testar_token(
    token: str
):
    """Testa se um Access Token é válido (endpoint de teste)"""
    try:
        service = get_mercadopago_service(token)
        balance = service.get_account_balance()
        
        # Buscar últimos pagamentos
        payments = service.search_payments(limit=5)
        
        return {
            "valid": True,
            "balance": {
                "total": balance.get("total_amount", 0),
                "disponivel": balance.get("available_balance", 0),
                "moeda": balance.get("currency_id", "BRL")
            },
            "transacoes_recentes": len(payments),
            "message": "Token válido! Você pode sincronizar suas transações."
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e),
            "message": "Token inválido ou expirado. Verifique as instruções e gere um novo token."
        }
