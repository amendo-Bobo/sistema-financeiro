@echo off
title Sistema Financeiro - Backend + Frontend
color 0A
echo.
echo ====================================
echo  INICIANDO SISTEMA FINANCEIRO
echo ====================================
echo.

echo [1/2] Iniciando Backend...
cd /d "%~dp0backend"
start "Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak > nul

echo [2/2] Iniciando Frontend...
cd /d "%~dp0frontend"
start "Frontend" cmd /k "npm run dev"

echo.
echo ====================================
echo  SISTEMA INICIADO COM SUCESSO!
echo ====================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause > nul
