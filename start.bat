@echo off
echo === Telugu AI Tutor - Quick Start ===
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo X Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo √ Docker is running
echo.

REM Start infrastructure
echo Starting infrastructure services...
docker-compose up -d

echo Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check services
echo.
echo Checking services...
docker ps

echo.
echo === Setup Complete ===
echo.
echo Next steps:
echo 1. Setup database:
echo    cd backend ^&^& python app/db/migrate.py
echo.
echo 2. Ingest data:
echo    python -m scripts.ingest_data --source custom --path ./data/sample
echo    python -m scripts.ingest_data --source samanantar --path ./data/samanantar
echo.
echo 3. Start backend (Terminal 1):
echo    cd backend ^&^& uvicorn app.main:app --reload
echo.
echo 4. Start frontend (Terminal 2):
echo    cd frontend ^&^& npm run dev
echo.
echo 5. Open http://localhost:3000
echo.
pause
