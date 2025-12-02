@echo off
echo Starting LangGraph Research Assistant...

:: Start Backend
start "LangGraph Backend" cmd /k "echo Starting Backend... & uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

:: Start Frontend
start "LangGraph Frontend" cmd /k "echo Starting Frontend... & cd frontend & npm run dev"

echo.
echo Both services are starting...
echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
pause
