# Script PowerShell para iniciar Backend e Frontend juntos
Write-Host "====================================" -ForegroundColor Green
Write-Host " INICIANDO SISTEMA FINANCEIRO" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

Write-Host "[1/2] Iniciando Backend..." -ForegroundColor Yellow
$backend = Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d `"%~dp0backend`" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000" -PassThru -WindowStyle Minimized

Start-Sleep -Seconds 3

Write-Host "[2/2] Iniciando Frontend..." -ForegroundColor Yellow
$frontend = Start-Process -FilePath "cmd" -ArgumentList "/k", "cd /d `"%~dp0frontend`" && npm run dev" -PassThru -WindowStyle Minimized

Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host " SISTEMA INICIADO COM SUCESSO!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend:  http://localhost:8000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pressione qualquer tecla para fechar..." -ForegroundColor White
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
