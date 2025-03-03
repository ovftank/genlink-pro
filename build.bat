@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

echo Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1

if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install dependencies
    exit /b 1
)

echo Building application...
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
pyinstaller --noconfirm --onefile --windowed --icon "icon.ico" --add-data "icon.ico;." "main.py" >nul 2>&1

if %ERRORLEVEL% neq 0 (
    echo Error: Build failed
    exit /b 1
)

if not exist "dist\main.exe" (
    echo Error: Output file not found
    exit /b 1
)

echo Build completed successfully
exit /b 0