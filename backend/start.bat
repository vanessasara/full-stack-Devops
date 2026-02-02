@echo off
REM Sony Interior Backend Startup Script for Windows

echo Starting Sony Interior Backend API...

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Please run setup first:
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo    pip install -r requirements.txt
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Check if .env file exists
if not exist ".env" (
    echo .env file not found. Copying from .env.example...
    copy .env.example .env
    echo Please edit .env and add your API keys before running again.
    exit /b 1
)

REM Start the server
echo Starting FastAPI server on http://localhost:8000
echo API docs available at http://localhost:8000/docs
echo.
uvicorn main:app --reload --host 0.0.0.0 --port 8000
