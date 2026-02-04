@echo off
REM DocuMind AI - Windows Setup Script

echo ==================================================
echo   DocuMind AI - Automated Setup (Windows)
echo ==================================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.8+
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo [OK] Dependencies installed
echo.

REM Create .env file
echo Setting up environment variables...
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [OK] .env file created
        echo.
        echo [WARNING] Please edit .env file and add your Gemini API key
        echo Get your key at: https://makersuite.google.com/app/apikey
    )
) else (
    echo [OK] .env file already exists
)
echo.

REM Create data directories
echo Creating data directories...
if not exist "data\uploads" mkdir data\uploads
if not exist "data\chroma_db" mkdir data\chroma_db
echo [OK] Data directories created
echo.

REM Run tests
echo Running system tests...
python test_system.py
echo.

echo ==================================================
echo   Setup Complete!
echo ==================================================
echo.
echo Next steps:
echo.
echo 1. Edit .env file and add your Gemini API key:
echo    notepad .env
echo.
echo 2. Run the application:
echo    streamlit run app.py
echo.
echo 3. Open your browser at:
echo    http://localhost:8501
echo.
echo ==================================================
echo.
pause
