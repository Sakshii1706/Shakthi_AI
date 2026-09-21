@echo off
setlocal EnableExtensions

title Shakthi AI - Sovereign Edge Launcher

echo.
echo ============================================================
echo                 SHAKTHI AI - SOVEREIGN EDGE
echo ============================================================
echo.

set "APP_ROOT=C:\Shakthi_AI"
set "BACKEND_ROOT=C:\ShakthiAI"
set "ASR_ROOT=C:\ShakthiAI-ASR"

set "UI_PYTHON=%APP_ROOT%\.venv\Scripts\python.exe"
set "ASR_PYTHON=%ASR_ROOT%\ai4bharat-env\Scripts\python.exe"
set "ASR_SCRIPT=%ASR_ROOT%\kannada_asr.py"
set "ASR_MODEL=%ASR_ROOT%\models\indicconformer_stt_kn_hybrid_rnnt_large.nemo"

set "FFMPEG_BIN=C:\Users\admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build-shared\bin"

set "SHAKTHI_ASR_PYTHON=%ASR_PYTHON%"
set "SHAKTHI_ASR_SCRIPT=%ASR_SCRIPT%"
set "SHAKTHI_ASR_MODEL_PATH=%ASR_MODEL%"

set "OLLAMA_HOST=127.0.0.1:11434"

rem Force local/offline Hugging Face behavior.
set "HF_HUB_OFFLINE=1"
set "HF_DATASETS_OFFLINE=1"

rem Add local FFmpeg to PATH.
set "PATH=%FFMPEG_BIN%;%PATH%"

echo [1/6] Checking Shakthi AI Python...
if not exist "%UI_PYTHON%" (
    echo ERROR: UI Python not found:
    echo %UI_PYTHON%
    pause
    exit /b 1
)
echo       OK

echo.
echo [2/6] Checking Kannada ASR...
if not exist "%ASR_PYTHON%" (
    echo ERROR: ASR Python not found:
    echo %ASR_PYTHON%
    pause
    exit /b 1
)

if not exist "%ASR_SCRIPT%" (
    echo ERROR: ASR script not found:
    echo %ASR_SCRIPT%
    pause
    exit /b 1
)

if not exist "%ASR_MODEL%" (
    echo ERROR: IndicConformer model not found:
    echo %ASR_MODEL%
    pause
    exit /b 1
)
echo       OK

echo.
echo [3/6] Checking FFmpeg...
if not exist "%FFMPEG_BIN%\ffmpeg.exe" (
    echo ERROR: FFmpeg not found:
    echo %FFMPEG_BIN%\ffmpeg.exe
    pause
    exit /b 1
)
echo       OK

echo.
echo [4/6] Checking Ollama...

set "OLLAMA_EXE="
for /f "delims=" %%O in ('where ollama 2^>nul') do (
    if not defined OLLAMA_EXE set "OLLAMA_EXE=%%O"
)

if not defined OLLAMA_EXE (
    echo ERROR: Ollama executable not found in PATH.
    pause
    exit /b 1
)

powershell -NoProfile -Command ^
    "$ok=$false; try { Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2 | Out-Null; $ok=$true } catch {}; if($ok){exit 0}else{exit 1}"

if errorlevel 1 (
    echo       Starting local Ollama server...
    start "" /B "%OLLAMA_EXE%" serve
)

echo       Waiting for local Ollama...

powershell -NoProfile -Command ^
    "$ok=$false; for($i=0;$i -lt 30;$i++){ try { Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 2 | Out-Null; $ok=$true; break } catch { Start-Sleep -Seconds 1 } }; if($ok){exit 0}else{exit 1}"

if errorlevel 1 (
    echo ERROR: Local Ollama server did not become ready.
    pause
    exit /b 1
)

echo       Ollama is ready.

echo.
echo       Checking Gemma 3 4B...
"%OLLAMA_EXE%" list | findstr /I /C:"gemma3:4b" >nul

if errorlevel 1 (
    echo ERROR: gemma3:4b is not installed locally.
    echo The launcher will NOT download it.
    pause
    exit /b 1
)

echo       gemma3:4b found locally.

echo.
echo [5/6] Checking local Streamlit...
"%UI_PYTHON%" -m streamlit --version

if errorlevel 1 (
    echo ERROR: Streamlit is not available in the UI environment.
    pause
    exit /b 1
)

echo       OK

echo.
echo [6/6] Launching Shakthi AI...
echo.
echo Local URL:
echo http://127.0.0.1:8501
echo.
echo Air-gapped runtime variables configured.
echo No package installation or model download will be performed.
echo.

start "" "%UI_PYTHON%" -m streamlit run "%APP_ROOT%\app.py" --server.address 127.0.0.1 --server.port 8501

echo Waiting for Streamlit...

powershell -NoProfile -Command ^
    "$ok=$false; for($i=0;$i -lt 30;$i++){ try { $r=Invoke-WebRequest -Uri 'http://127.0.0.1:8501' -UseBasicParsing -TimeoutSec 2; if($r.StatusCode -ge 200){$ok=$true; break} } catch { Start-Sleep -Seconds 1 } }; if($ok){exit 0}else{exit 1}"

if errorlevel 1 (
    echo WARNING: Streamlit did not respond within the expected time.
    echo Check the Streamlit window for details.
    pause
    exit /b 1
)

echo       Streamlit is ready.
echo.
echo Opening Shakthi AI...
start "" "http://127.0.0.1:8501"

echo.
echo ============================================================
echo Shakthi AI is running locally.
echo Keep the Streamlit process open while using the application.
echo ============================================================
echo.
pause