Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host "       AI-Based Skill Assessment and Career Guidance System (SDG 4)          " -ForegroundColor Cyan
Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Launching Backend (FastAPI on http://localhost:8000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; .\venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

Write-Host "Launching Frontend (Vite on http://localhost:5173)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend'; npm run dev"

Write-Host ""
Write-Host "------------------------------------------------------------------------------" -ForegroundColor Yellow
Write-Host "Web Platform UI: http://localhost:5173" -ForegroundColor Yellow
Write-Host "Swagger API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "ReDoc API Docs:   http://localhost:8000/redoc" -ForegroundColor Yellow
Write-Host ""
Write-Host "Demo Accounts:" -ForegroundColor Magenta
Write-Host "  - Student:   student@demo.com   / Demo@123456" -ForegroundColor White
Write-Host "  - Counselor: counselor@demo.com / Demo@123456" -ForegroundColor White
Write-Host "  - Admin:     admin@demo.com     / Demo@123456" -ForegroundColor White
Write-Host "==============================================================================" -ForegroundColor Cyan
