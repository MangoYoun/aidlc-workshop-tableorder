@echo off
echo ========================================
echo   TableOrder Services Launcher
echo ========================================
echo.

REM Backend
echo [1/3] Starting Backend Service...
start "Backend Service" cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn src.main:app --reload --port 8000"
timeout /t 2 /nobreak >nul

REM Customer Frontend
echo [2/3] Starting Customer Frontend...
start "Customer Frontend" cmd /k "cd /d %~dp0customer-frontend && npm run dev"
timeout /t 2 /nobreak >nul

REM Admin Frontend
echo [3/3] Starting Admin Frontend...
start "Admin Frontend" cmd /k "cd /d %~dp0admin-frontend && npm run dev"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo   All Services Started!
echo ========================================
echo.
echo Backend API:        http://localhost:8000
echo API Docs:           http://localhost:8000/docs
echo Customer Frontend:  http://localhost:5173
echo Admin Frontend:     http://localhost:5174
echo.
echo Press any key to exit...
pause >nul
