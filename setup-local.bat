@echo off
echo ========================================
echo   TableOrder Local Setup Script
echo ========================================
echo.

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.9+
    pause
    exit /b 1
)
python --version
echo.

REM Check Node.js
echo [2/6] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found! Please install Node.js 20+
    pause
    exit /b 1
)
node --version
echo.

REM Create Python virtual environment
echo [3/6] Creating Python virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

REM Install Python dependencies
echo [4/6] Installing Python dependencies...
call venv\Scripts\activate
pip install --upgrade pip
pip install -r config\requirements.txt
echo.

REM Create .env file
echo [5/6] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please update DATABASE_URL with your PostgreSQL password.
) else (
    echo .env file already exists.
)
echo.

REM Create logs directory
echo [6/6] Creating logs directory...
if not exist logs (
    mkdir logs
    echo Logs directory created.
) else (
    echo Logs directory already exists.
)
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Install PostgreSQL and create 'tableorder' database
echo 2. Update .env file with your PostgreSQL password
echo 3. Run: python -c "from src.database import engine, Base; from src.models import *; Base.metadata.create_all(bind=engine)"
echo 4. Install Frontend dependencies:
echo    - cd customer-frontend ^&^& npm install
echo    - cd admin-frontend ^&^& npm install
echo 5. Run: start-all.bat
echo.
pause
