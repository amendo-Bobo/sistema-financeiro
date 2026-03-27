"""Modelos do banco de dados"""
from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey, Text, Enum, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class TipoTransacao(str, enum.Enum):
    ENTRADA = "entrada"
    SAIDA = "saida"

class CategoriaTransacao(str, enum.Enum):
    ALIMENTACAO = "alimentacao"
    TRANSPORTE = "transporte"
    MORADIA = "moradia"
    SAUDE = "saude"
    EDUCACAO = "educacao"
    LAZER = "lazer"
    VESTUARIO = "vestuario"
    UTILIDADES = "utilidades"
    SALARIO = "salario"
    INVESTIMENTOS = "investimentos"
    OUTROS = "outros"

class User(Base):
    """Usuário do sistema"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    nome = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    transacoes = relationship("Transacao", back_populates="usuario", cascade="all, delete-orphan")
    contas_bancarias = relationship("ContaBancaria", back_populates="usuario", cascade="all, delete-orphan")
    categorias_personalizadas = relationship("CategoriaPersonalizada", back_populates="usuario", cascade="all, delete-orphan")

class Transacao(Base):
    """Transação financeira"""
    __tablename__ = "transacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    descricao = Column(String(255), nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    tipo = Column(Enum(TipoTransacao), nullable=False)
    categoria = Column(Enum(CategoriaTransacao), nullable=True)
    categoria_personalizada_id = Column(Integer, ForeignKey("categorias_personalizadas.id"), nullable=True)
    data = Column(Date, nullable=False)
    is_fixa = Column(Boolean, default=False)
    is_recorrente = Column(Boolean, default=False)
    observacoes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="transacoes")
    categoria_personalizada = relationship("CategoriaPersonalizada", back_populates="transacoes")

class ContaBancaria(Base):
    """Conta bancária do usuário"""
    __tablename__ = "contas_bancarias"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nome_banco = Column(String(255), nullable=False)
    agencia = Column(String(50), nullable=True)
    conta = Column(String(100), nullable=True)
    tipo_conta = Column(String(50), nullable=True)
    saldo = Column(Numeric(15, 2), default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Para integração futura com bancos
    integracao_tipo = Column(String(100), nullable=True)
    integracao_token = Column(String(500), nullable=True)
    ultima_sincronizacao = Column(DateTime, nullable=True)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="contas_bancarias")

class CategoriaPersonalizada(Base):
    """Categoria personalizada pelo usuário"""
    __tablename__ = "categorias_personalizadas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    cor = Column(String(7), default="#000000")
    icone = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    usuario = relationship("User", back_populates="categorias_personalizadas")
    transacoes = relationship("Transacao", back_populates="categoria_personalizada")

class OrcamentoMensal(Base):
    """Orçamento mensal por categoria"""
    __tablename__ = "orcamentos_mensais"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ano = Column(Integer, nullable=False)
    mes = Column(Integer, nullable=False)
    categoria = Column(Enum(CategoriaTransacao), nullable=False)
    valor_orcado = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
