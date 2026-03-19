@echo off
chcp 65001 >nul
:: ==========================================
:: INICIALIZADOR DO BACKEND - SISTEMA FINANCAS
:: ==========================================
:: Este script configura automaticamente o ambiente

echo ==========================================
echo   SISTEMA DE FINANCAS - BACKEND
echo ==========================================
echo.

:: Desativar alias do Windows Store temporariamente
set PATH=%PATH:C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps;=%

:: Procurar Python em locais comuns
set PYTHON_CMD=""

:: Verificar python direto
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto :found_python
)

:: Verificar python3
python3 --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    goto :found_python
)

:: Verificar em locais comuns do Windows
if exist "C:\Python311\python.exe" (
    set PYTHON_CMD=C:\Python311\python.exe
    goto :found_python
)
if exist "C:\Python310\python.exe" (
    set PYTHON_CMD=C:\Python310\python.exe
    goto :found_python
)
if exist "C:\Python39\python.exe" (
    set PYTHON_CMD=C:\Python39\python.exe
    goto :found_python
)
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python311\python.exe
    goto :found_python
)
if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python310\python.exe
    goto :found_python
)
if exist "%LOCALAPPDATA%\Programs\Python\Python39\python.exe" (
    set PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python39\python.exe
    goto :found_python
)

goto :python_not_found

:found_python
echo [OK] Python encontrado: %PYTHON_CMD%
%PYTHON_CMD% --version
echo.

:: Ir para diretorio do projeto
cd /d "C:\Users\Usuario\CascadeProjects\sistema-financas\backend"
if errorlevel 1 (
    echo [ERRO] Nao foi possivel acessar o diretorio!
    echo Verifique se o projeto esta em: C:\Users\Usuario\CascadeProjects\sistema-financas\
    pause
    exit /b 1
)

echo [OK] Diretorio: %CD%
echo.

:: Criar ambiente virtual se nao existir
if not exist "venv" (
    echo [INFO] Criando ambiente virtual...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo [ERRO] Falha ao criar ambiente virtual
        pause
        exit /b 1
    )
    echo [OK] Ambiente virtual criado
) else (
    echo [OK] Usando ambiente virtual existente
)

:: Ativar ambiente virtual
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERRO] Falha ao ativar ambiente virtual
    pause
    exit /b 1
)
echo [OK] Ambiente ativado

:: Instalar dependencias
echo.
echo [INFO] Instalando/Atualizando dependencias...
echo Isso pode levar alguns minutos na primeira vez...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERRO] Falha ao instalar dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias prontas

:: Criar .env se nao existir
if not exist ".env" (
    copy .env.example .env >nul 2>&1
    echo [OK] Arquivo .env criado
)

:: Iniciar servidor
echo.
echo ==========================================
echo    SERVIDOR INICIADO!
echo.
echo    Acesse no navegador:
echo    http://localhost:8000
echo.
echo    Documentacao da API:
echo    http://localhost:8000/docs
echo.
echo    Pressione CTRL+C para parar
echo ==========================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
exit /b 0

:python_not_found
echo ==========================================
echo [ERRO] PYTHON NAO ENCONTRADO!
echo ==========================================
echo.
echo O Python nao foi encontrado no seu sistema.
echo.
echo PARA RESOLVER:
echo.
echo OPCAO 1 - Instalar Python:
echo 1. Acesse: https://python.org/downloads
echo 2. Baixe Python 3.11 ou superior
echo 3. NA INSTALACAO, MARQUE:
echo    ☑ "Add Python to PATH"
echo    ☑ "Install pip"
echo 4. Reinicie o computador
echo 5. Execute este script novamente
echo.
echo OPCAO 2 - Desativar alias do Windows Store:
echo 1. Abra: Configuracoes → Aplicativos → Configuracoes avancadas do aplicativo
echo 2. Desative: "Aliases de execucao do aplicativo"
echo    (Desative python.exe e python3.exe)
echo 3. Reinicie o terminal
echo.
pause
exit /b 1
