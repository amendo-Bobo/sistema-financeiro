"""Schemas Pydantic para validação de dados"""
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from app.models import TipoTransacao, CategoriaTransacao

# ==================== USER SCHEMAS ====================

class UserBase(BaseModel):
    email: EmailStr
    nome: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_active: bool
    created_at: datetime

class UserInDB(User):
    hashed_password: str

# ==================== TOKEN SCHEMAS ====================

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# ==================== TRANSAÇÃO SCHEMAS ====================

class TransacaoBase(BaseModel):
    descricao: str = Field(..., min_length=1, max_length=255)
    valor: Decimal = Field(..., gt=0)
    tipo: str  # Mudar para string
    categoria: str = "outros"  # Mudar para string
    data: date
    is_fixa: bool = False
    is_recorrente: bool = False
    observacoes: Optional[str] = None
    categoria_personalizada_id: Optional[int] = None

class TransacaoCreate(TransacaoBase):
    usuario_id: Optional[int] = None

class TransacaoUpdate(BaseModel):
    descricao: Optional[str] = Field(None, min_length=1, max_length=255)
    valor: Optional[Decimal] = Field(None, gt=0)
    tipo: Optional[TipoTransacao] = None
    categoria: Optional[CategoriaTransacao] = None
    data: Optional[date] = None
    is_fixa: Optional[bool] = None
    is_recorrente: Optional[bool] = None
    observacoes: Optional[str] = None
    categoria_personalizada_id: Optional[int] = None

class Transacao(TransacaoBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int
    created_at: datetime
    updated_at: datetime

class TransacaoResumo(BaseModel):
    """Resumo de transações por período"""
    total_entradas: Decimal
    total_saidas: Decimal
    saldo: Decimal
    quantidade_transacoes: int

# ==================== CATEGORIA PERSONALIZADA SCHEMAS ====================

class CategoriaPersonalizadaBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    cor: str = Field(default="#000000", pattern="^#[0-9A-Fa-f]{6}$")
    icone: Optional[str] = None

class CategoriaPersonalizadaCreate(CategoriaPersonalizadaBase):
    pass

class CategoriaPersonalizada(CategoriaPersonalizadaBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int
    created_at: datetime

# ==================== CONTA BANCÁRIA SCHEMAS ====================

class ContaBancariaBase(BaseModel):
    nome_banco: str = Field(..., min_length=1, max_length=255)
    agencia: Optional[str] = Field(None, max_length=50)
    conta: Optional[str] = Field(None, max_length=100)
    tipo_conta: Optional[str] = None
    saldo: Decimal = Field(default=0)

class ContaBancariaCreate(ContaBancariaBase):
    pass

class ContaBancariaUpdate(BaseModel):
    nome_banco: Optional[str] = Field(None, min_length=1, max_length=255)
    agencia: Optional[str] = Field(None, max_length=50)
    conta: Optional[str] = Field(None, max_length=100)
    tipo_conta: Optional[str] = None
    saldo: Optional[Decimal] = Field(None)
    is_active: Optional[bool] = None

class ContaBancaria(ContaBancariaBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int
    is_active: bool
    integracao_tipo: Optional[str]
    ultima_sincronizacao: Optional[datetime]
    created_at: datetime
    updated_at: datetime

# ==================== ORÇAMENTO SCHEMAS ====================

class OrcamentoMensalBase(BaseModel):
    ano: int = Field(..., ge=2000, le=2100)
    mes: int = Field(..., ge=1, le=12)
    categoria: CategoriaTransacao
    valor_orcado: Decimal = Field(..., gt=0)

class OrcamentoMensalCreate(OrcamentoMensalBase):
    pass

class OrcamentoMensal(OrcamentoMensalBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    usuario_id: int
    created_at: datetime

class OrcamentoResumo(BaseModel):
    """Resumo de orçamento vs gastos reais"""
    categoria: CategoriaTransacao
    orcado: Decimal
    gasto_real: Decimal
    diferenca: Decimal
    percentual_usado: float

# ==================== DASHBOARD SCHEMAS ====================

class DashboardResumo(BaseModel):
    """Resumo geral para o dashboard"""
    saldo_atual: Decimal
    total_entradas_mes: Decimal
    total_saidas_mes: Decimal
    balanco_mes: Decimal
    transacoes_recentes: List[Transacao]
    alertas_orcamento: List[OrcamentoResumo]

class GraficoDados(BaseModel):
    """Dados para gráficos"""
    labels: List[str]
    valores: List[Decimal]
    cores: Optional[List[str]] = None

class FiltroTransacao(BaseModel):
    """Filtros para busca de transações"""
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    tipo: Optional[TipoTransacao] = None
    categoria: Optional[CategoriaTransacao] = None
    min_valor: Optional[Decimal] = None
    max_valor: Optional[Decimal] = None
