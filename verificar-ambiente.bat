@echo off
chcp 65001 >nul
cls
echo ==========================================
echo   VERIFICADOR DE AMBIENTE - SISTEMA FINANCAS
echo ==========================================
echo.

set PYTHON_OK=0
set NODE_OK=0
set ERROS=0

:: ==========================================
echo [1/4] Verificando PYTHON...
:: ==========================================
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo     ✓ Python encontrado!
    python --version
    set PYTHON_OK=1
) else (
    echo     ✗ PYTHON NAO ENCONTRADO
    set /a ERROS+=1
)
echo.

:: ==========================================
echo [2/4] Verificando PIP...
:: ==========================================
pip --version >nul 2>&1
if %errorlevel% == 0 (
    echo     ✓ PIP encontrado!
    pip --version
) else (
    echo     ✗ PIP NAO ENCONTRADO
    set /a ERROS+=1
)
echo.

:: ==========================================
echo [3/4] Verificando NODE.JS...
:: ==========================================
node --version >nul 2>&1
if %errorlevel% == 0 (
    echo     ✓ Node.js encontrado!
    node --version
    set NODE_OK=1
) else (
    echo     ✗ NODE.JS NAO ENCONTRADO
    set /a ERROS+=1
)
echo.

:: ==========================================
echo [4/4] Verificando NPM...
:: ==========================================
npm --version >nul 2>&1
if %errorlevel% == 0 (
    echo     ✓ NPM encontrado!
    npm --version
) else (
    echo     ✗ NPM NAO ENCONTRADO
    set /a ERROS+=1
)
echo.

:: ==========================================
echo ==========================================
echo   RESULTADO DA VERIFICACAO
echo ==========================================
echo.

if %ERROS% == 0 (
    echo ✓✓✓ TUDO PRONTO! ✓✓✓
    echo.
    echo Para iniciar o sistema:
    echo.
    echo 1. BACKEND: Execute start-backend.bat
    echo 2. FRONTEND: Execute start-frontend.bat
    echo.
    pause
    exit /b 0
)

echo ✗ FALTAM %ERROS% COMPONENTE(S)
echo.

if %PYTHON_OK% == 0 (
    echo ==========================================
    echo INSTALAR PYTHON:
    echo ==========================================
    echo 1. Acesse: https://python.org/downloads
    echo 2. Clique em "Download Python 3.11.x"
    echo 3. NA INSTALACAO, MARQUE:
    echo    [x] Add Python to PATH  ^<-- IMPORTANTE!
    echo    [x] Install pip
    echo 4. Clique "Install Now"
    echo.
)

if %NODE_OK% == 0 (
    echo ==========================================
    echo INSTALAR NODE.JS:
    echo ==========================================
    echo 1. Acesse: https://nodejs.org
    echo 2. Clique no botao VERDE "LTS"
    echo 3. Execute o instalador e clique "Next"
    echo.
)

echo ==========================================
echo DEPOIS DE INSTALAR:
echo ==========================================
echo 1. FECHE este terminal
    echo 2. Abra um NOVO terminal
    echo 3. Execute este script novamente
    echo    para verificar se deu certo
    echo.
    
    pause
    exit /b 1
