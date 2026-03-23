"""Aplicação FastAPI principal"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, transacoes, dashboard, contas, importacao
from pathlib import Path

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
    """Endpoint raiz - serve frontend ou API"""
    static_dir = Path(__file__).parent.parent / "static"
    index_file = static_dir / "index.html"
    
    print(f"DEBUG: static_dir exists: {static_dir.exists()}")
    print(f"DEBUG: index_file exists: {index_file.exists()}")
    print(f"DEBUG: static_dir path: {static_dir}")
    print(f"DEBUG: index_file path: {index_file}")
    
    if index_file.exists():
        print("DEBUG: Serving index.html")
        return FileResponse(str(index_file))
    
    print("DEBUG: Serving JSON fallback")
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "online",
        "debug": {
            "static_dir_exists": static_dir.exists(),
            "index_file_exists": index_file.exists(),
            "static_dir_path": str(static_dir),
            "index_file_path": str(index_file)
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

# Servir arquivos estáticos do frontend (se existirem)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        """Serve frontend React app for all non-API routes"""
        # Se for uma rota da API, não serve o frontend
        if full_path.startswith("api/") or full_path in ["health", "docs", "openapi.json"]:
            return {"detail": "Not Found"}
        
        # Tenta servir o arquivo estático
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        
        # Se não encontrar, serve o index.html (SPA behavior)
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        
        # Se não houver frontend buildado, retorna JSON da API
        return {
            "app": settings.APP_NAME,
            "version": "1.0.0",
            "status": "online",
            "message": "API is running. Frontend not built yet."
        }
