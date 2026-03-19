"""Router para importação de extratos bancários"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth.security import get_current_active_user
from app.models import User
from app.schemas import TransacaoCreate, Transacao
from app.crud.transacoes import create_transacao
from app.services.importacao import importar_transacoes

router = APIRouter(prefix="/importar", tags=["Importação"])


@router.post("/arquivo", response_model=List[Transacao])
async def importar_arquivo(
    arquivo: UploadFile = File(...),
    formato: str = Form("auto"),
    banco: str = Form("auto"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Importa transações de arquivo OFX, CSV ou PDF"""
    
    # Validar formato
    if formato == "auto":
        filename = arquivo.filename.lower()
        if filename.endswith('.ofx') or filename.endswith('.qfx'):
            formato = "ofx"
        elif filename.endswith('.csv'):
            formato = "csv"
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            formato = "xlsx"
        elif filename.endswith('.pdf'):
            formato = "pdf"
        else:
            raise HTTPException(
                status_code=400, 
                detail="Formato de arquivo não suportado. Use OFX, QFX, CSV, XLSX ou PDF"
            )
    
    # Ler conteúdo
    try:
        content = await arquivo.read()
        
        if formato.lower() in ['pdf', 'xlsx']:
            # PDF e XLSX são processados como bytes
            content_for_import = content
        else:
            # CSV e OFX são processados como texto
            try:
                content_for_import = content.decode('utf-8')
            except UnicodeDecodeError:
                # Tentar com encoding diferente
                try:
                    content_for_import = content.decode('latin-1')
                except:
                    raise HTTPException(
                        status_code=400,
                        detail="Não foi possível ler o arquivo. Verifique o encoding"
                    )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao ler arquivo: {str(e)}"
        )
    
    # Importar transações
    try:
        print(f"Importando arquivo: formato={formato}, banco={banco}")
        print(f"Tamanho do conteúdo: {len(content_for_import)} bytes")
        
        # Debug: mostrar primeiros 500 caracteres do conteúdo
        if formato.lower() == 'csv':
            print(f"Primeiros 500 chars: {content_for_import[:500]}")
        elif formato.lower() == 'xlsx':
            print(f"Arquivo XLSX detectado, tamanho: {len(content_for_import)} bytes")
        
        transacoes_importadas = importar_transacoes(content_for_import, formato, banco)
        print(f"Transações importadas: {len(transacoes_importadas)}")
    except Exception as e:
        print(f"Erro ao importar: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Erro ao processar arquivo: {str(e)}"
        )
    
    if not transacoes_importadas:
        raise HTTPException(
            status_code=400,
            detail="Nenhuma transação encontrada no arquivo"
        )
    
    # Salvar transações no banco
    transacoes_salvas = []
    for trans_data in transacoes_importadas:
        try:
            transacao_create = TransacaoCreate(**trans_data)
            transacao = create_transacao(db, transacao_create, current_user.id)
            transacoes_salvas.append(transacao)
        except Exception as e:
            print(f"Erro ao salvar transação: {e}")
            continue
    
    return transacoes_salvas


@router.get("/bancos-suportados")
def bancos_suportados():
    """Retorna lista de bancos suportados para importação CSV"""
    return {
        "bancos": [
            {"id": "auto", "nome": "Detectar automaticamente", "formato": "csv/xlsx"},
            {"id": "mercado_pago", "nome": "Mercado Pago", "formato": "csv/xlsx/pdf"},
            {"id": "nubank", "nome": "Nubank", "formato": "csv"},
            {"id": "itau", "nome": "Itaú", "formato": "csv/ofx"},
            {"id": "bradesco", "nome": "Bradesco", "formato": "csv/ofx"},
            {"id": "santander", "nome": "Santander", "formato": "csv/ofx"},
            {"id": "bb", "nome": "Banco do Brasil", "formato": "csv/ofx"},
            {"id": "caixa", "nome": "Caixa Econômica", "formato": "csv/ofx"},
            {"id": "inter", "nome": "Banco Inter", "formato": "csv/ofx"},
            {"id": "c6", "nome": "C6 Bank", "formato": "csv"},
            {"id": "original", "nome": "Banco Original", "formato": "csv"},
            {"id": "generico", "nome": "Outros/Genérico", "formato": "csv"}
        ],
        "formatos": ["ofx", "csv", "qfx", "pdf"]
    }
