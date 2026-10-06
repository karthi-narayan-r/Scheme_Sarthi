@echo off
TITLE Scheme Sarthi - Server Launcher
echo ============================================================
echo   🏛️  Scheme Sarthi - Government Scheme Gap Analyzer & Log
echo ============================================================
echo.
echo [1/3] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not found on PATH. Please install Python.
    pause
    exit /b
)

echo [2/3] Verifying required Python packages (flask, scikit-learn, numpy, pandas)...
python -c "import flask, sklearn, numpy, pandas" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    python -m pip install flask scikit-learn numpy pandas
)

echo [3/3] Starting Scheme Sarthi Web Application...
start http://127.0.0.1:5000
echo.
echo Application server is running at http://127.0.0.1:5000
echo (Keep this command window open while using Scheme Sarthi)
echo.
python app.py
pause
