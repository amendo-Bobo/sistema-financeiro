"""Aplicação FastAPI principal"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, transacoes, dashboard, contas, importacao

settings = get_settings()

# Criar tabelas no startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Criar tabelas
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup (se necessário)

app = FastAPI(
    title=settings.APP_NAME,
    description="API para controle de finanças pessoais",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api")
app.include_router(transacoes.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(contas.router, prefix="/api")
app.include_router(importacao.router, prefix="/api")

@app.get("/")
def root():
    """Endpoint raiz"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
