@echo off
title PCUtil Windows Compiler Tools
echo ==================================================================
echo 🚀 PCUtil Automated Windows Compilation Engine
echo ==================================================================

:: 1. Verify and satisfy pip packages
echo 📦 Step 1: Checking build tool requirements...
pip install pyinstaller pyqt6 --quiet

:: 2. Compile application with elevated UAC manifest enforcement
echo ⚙️  Step 2: Compiling assets into an elevated standalone .exe executable...
pyinstaller --onefile --windowed --uac-admin --add-data "core_engine.ps1;." --name PCUtil --clean app.py

if not exist "dist\PCUtil.exe" (
    echo ❌ Error: Compilation failure. Check your setup dependencies.
    pause
    exit /b 1
)

echo ==================================================================
echo ✅ Success! Your standalone package is located inside: .\dist\PCUtil.exe
echo 🔒 Note: Running it will automatically trigger the Windows UAC permission window.
echo ==================================================================
pause
