@echo off
chcp 65001 >nul
:: ==========================================
:: INICIALIZADOR DO FRONTEND - SISTEMA FINANCAS
:: ==========================================

echo ==========================================
echo   SISTEMA DE FINANCAS - FRONTEND
echo ==========================================
echo.

:: Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Node.js nao encontrado!
    echo.
    echo Para resolver:
    echo 1. Acesse: https://nodejs.org
    echo 2. Clique no botao VERDE "LTS"
    echo 3. Instale e reinicie o computador
    echo.
    pause
    exit /b 1
)

echo [OK] Node.js encontrado
node --version
echo.

:: Ir para diretorio do projeto
cd /d "C:\Users\Usuario\CascadeProjects\sistema-financas\frontend"
if errorlevel 1 (
    echo [ERRO] Diretorio nao encontrado!
    pause
    exit /b 1
)

echo [OK] Diretorio: %CD%
echo.

:: Instalar dependencias (node_modules)
if not exist "node_modules" (
    echo [INFO] Instalando dependencias...
    echo Isso pode levar 2-5 minutos na primeira vez...
    npm install
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias!
        pause
        exit /b 1
    )
    echo [OK] Dependencias instaladas
) else (
    echo [OK] Dependencias ja instaladas
)

echo.
echo ==========================================
echo    INICIANDO SERVIDOR FRONTEND
echo    Acesse: http://localhost:3000
echo ==========================================
echo.
echo Pressione CTRL+C para parar
echo.

npm run dev

pause
