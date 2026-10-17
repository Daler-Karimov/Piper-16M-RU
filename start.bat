@echo off
title Piper TTS Web UI
cd /d "%~dp0"

echo ===================================================
echo            Starting Piper TTS Web UI
echo ===================================================
echo.

rem 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in system PATH!
    echo Please install Python and ensure it is added to PATH.
    pause
    exit /b 1
)

rem 2. Create virtual environment if missing
if not exist .venv\Scripts\python.exe (
    echo [1/3] Creating virtual environment [.venv]...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
    echo Installing dependencies into .venv...
    .venv\Scripts\python.exe -m pip install -r requirements.txt
) else (
    echo [1/3] Virtual environment [.venv] ready.
)

rem 3. Check voice model
echo [2/3] Checking voice models...
if not exist voices\ru_RU-dmitri-medium.onnx (
    echo Downloading default voice model...
    if not exist voices mkdir voices
    curl.exe -L "https://huggingface.co/rhasspy/piper-voices/raw/main/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx.json" -o "voices\ru_RU-dmitri-medium.onnx.json"
    curl.exe -L "https://huggingface.co/rhasspy/piper-voices/resolve/main/ru/ru_RU/dmitri/medium/ru_RU-dmitri-medium.onnx" -o "voices\ru_RU-dmitri-medium.onnx"
)
echo Voice models ready.

rem 4. Launch app using .venv Python
echo [3/3] Starting web server...
echo.
echo ===================================================
echo   Press Ctrl+C or close this window to stop.
echo ===================================================
echo.

.venv\Scripts\python.exe app.py

if errorlevel 1 (
    echo.
    echo [!] Server stopped with an error.
    pause
)
