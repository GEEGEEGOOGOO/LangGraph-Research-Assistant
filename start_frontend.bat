@echo off
echo Installing frontend dependencies...
cd frontend
call npm install

echo.
echo Starting development server...
call npm run dev

pause
