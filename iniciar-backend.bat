@echo off
chcp 65001 >nul
echo ==========================================
echo   SISTEMA DE FINANCAS - INICIALIZADOR
echo ==========================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo.
    echo Para resolver:
    echo 1. Instale o Python em: https://python.org
    echo 2. Marque a opcao "Add Python to PATH" na instalacao
    echo 3. Reinicie o computador
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
python --version
echo.

:: Navegar para o diretorio do backend
cd /d "C:\Users\Usuario\CascadeProjects\sistema-financas\backend"
if errorlevel 1 (
    echo [ERRO] Nao foi possivel acessar o diretorio do projeto!
    echo Verifique se o caminho esta correto.
    pause
    exit /b 1
)

echo [OK] Diretorio do projeto: %CD%
echo.

:: Verificar/criar ambiente virtual
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual!
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado
) else (
    echo [OK] Ambiente virtual encontrado
)

:: Ativar ambiente virtual
echo [INFO] Ativando ambiente virtual...
call venv\Scripts\activate
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual!
    pause
    exit /b 1
)
echo [OK] Ambiente virtual ativado

:: Instalar dependencias
echo.
echo [INFO] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias!
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas

:: Criar arquivo .env se nao existir
if not exist ".env" (
    echo [INFO] Criando arquivo .env...
    copy .env.example .env >nul
    echo [OK] Arquivo .env criado (edite se necessario)
)

:: Iniciar servidor
echo.
echo ==========================================
echo    INICIANDO SERVIDOR BACKEND
echo    Acesse: http://localhost:8000
echo    Documentacao: http://localhost:8000/docs
echo ==========================================
echo.
echo Pressione CTRL+C para parar o servidor
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
