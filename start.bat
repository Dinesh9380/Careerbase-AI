@echo off
echo ==============================================================================
echo       AI-Based Skill Assessment and Career Guidance System (SDG 4)
echo ==============================================================================
echo.
echo Launching Backend (FastAPI on http://localhost:8000)...
start "Career Intelligence - Backend (FastAPI)" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

echo Launching Frontend (Vite on http://localhost:5173)...
start "Career Intelligence - Frontend (React + Vite)" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ------------------------------------------------------------------------------
echo Web Platform UI: http://localhost:5173
echo Swagger API Docs: http://localhost:8000/docs
echo ReDoc API Docs:   http://localhost:8000/redoc
echo.
echo Demo Accounts:
echo   - Student:   student@demo.com   / Demo@123456
echo   - Counselor: counselor@demo.com / Demo@123456
echo   - Admin:     admin@demo.com     / Demo@123456
echo ==============================================================================
