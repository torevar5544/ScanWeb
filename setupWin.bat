@echo off
echo ==========================================
echo Website Security Scanner - Windows Setup
echo ==========================================

:: Check if winget is installed
where winget >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] Winget not found. Please install App Installer from Microsoft Store first.
    pause
    exit /b
)

:: Install Python 3
echo [*] Installing Python 3 via winget...
winget install --id Python.Python.3 -e --source winget

:: Refresh environment variables
echo [*] Refreshing environment variables...
setx PATH "%PATH%;C:\Users\%USERNAME%\AppData\Local\Programs\Python\Python310\Scripts\"

:: Create virtual environment
echo [*] Creating virtual environment...
python -m venv venv

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Upgrade pip
echo [*] Upgrading pip...
python -m pip install --upgrade pip

:: Install Python dependencies
echo [*] Installing Python dependencies...
pip install -r requirements.txt

:: Install system tools via winget
echo [*] Installing Nmap...
winget install --id Nmap.Nmap -e --source winget

echo [*] Installing WinMTR (MTR alternative)...
winget install --id WinMTR.WinMTR -e --source winget

echo ==========================================
echo [✓] Setup completed!
echo To start the scanner:
echo 1. Activate virtual environment: call venv\Scripts\activate.bat
echo 2. Run the scanner: python web_security_scanner.py
pause
