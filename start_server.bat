@REM @echo off
@REM cd /d "D:\Projects\Payment-App\neco-payment-manager-BE"

@REM call .venv\Scripts\activate.bat
@REM uvicorn app.main:app --reload


@REM @echo off
@REM REM Navigate to project directory
@REM cd /d "D:\Projects\Payment-App\neco-payment-manager-BE"

@REM REM Activate virtual environment
@REM call .venv\Scripts\activate.bat

@REM REM Start the server (no --reload)
@REM uvicorn app.main:app --host 0.0.0.0 --port 8000

@REM REM Optional: keep window open to see errors
@REM pause



@echo off
cd /d "D:\Projects\Payment-App\neco-payment-manager-BE"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Start backend
start "" uvicorn app.main:app --host 0.0.0.0 --port 8000
