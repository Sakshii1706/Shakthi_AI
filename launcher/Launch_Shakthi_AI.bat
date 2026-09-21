@echo off
setlocal EnableExtensions EnableDelayedExpansion

title Shakthi AI - Sovereign Edge

echo.
echo ============================================================
echo                  SHAKTHI AI
echo              Sovereign Edge Intelligence
echo ============================================================
echo.

REM ------------------------------------------------------------
REM Resolve application root from this launcher location
REM ------------------------------------------------------------

set "LAUNCHER_DIR=%~dp0"

for %%I in ("%LAUNCHER_DIR%..") do set "APP_ROOT=%%~fI"

REM Current deployment layout:
REM
REM C:\
REM ??? Shakthi_AI\
REM ??? ShakthiAI\
REM ??? ShakthiAI-ASR\
REM
REM The launcher is inside:
REM C:\Shakthi_AI\launcher\
REM
REM Therefore the sibling projects are resolved dynamically.

for %%I in ("%APP_ROOT%\..\ShakthiAI") do set "BACKEND_ROOT=%%~fI"
for %%I in ("%APP_ROOT%\..\ShakthiAI-ASR") do set "ASR_ROOT=%%~fI"

set "UI_PYTHON=%APP_ROOT%\.venv\Scripts\python.exe"
set "ASR_PYTHON=%ASR_ROOT%\ai4bharat-env\Scripts\python.exe"
set "ASR_SCRIPT=%ASR_ROOT%\kannada_asr.py"
set "ASR_MODEL=%ASR_ROOT%\models\indicconformer_stt_kn_hybrid_rnnt_large.nemo"

REM ------------------------------------------------------------
REM Environment variables
REM ------------------------------------------------------------

set "SHAKTHI_APP_ROOT=%APP_ROOT%"
set "SHAKTHI_BACKEND_ROOT=%BACKEND_ROOT%"
set "SHAKTHI_ASR_ROOT=%ASR_ROOT%"

set "SHAKTHI_ASR_PYTHON=%ASR_PYTHON%"
set "SHAKTHI_ASR_SCRIPT=%ASR_SCRIPT%"
set "SHAKTHI_ASR_MODEL_PATH=%ASR_MODEL%"

REM Local Ollama only
set "OLLAMA_HOST=127.0.0.1:11434"

REM Offline model/cache behavior
set "HF_HUB_OFFLINE=1"
set "HF_DATASETS_OFFLINE=1"

REM ------------------------------------------------------------
REM FFmpeg
REM ------------------------------------------------------------

set "FFMPEG_DIR=%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg.Shared_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-full_build-shared\bin"

if exist "%FFMPEG_DIR%\ffmpeg.exe" (
    set "PATH=%FFMPEG_DIR%;%PATH%"
)

echo [1/6] Checking Shakthi AI Python...

if not exist "%UI_PYTHON%" (
    echo ERROR: Shakthi AI Python environment not found.
    echo Expected:
    echo %UI_PYTHON%
    echo.
    echo Run Setup_Shakthi_AI.bat first.
    pause
    exit /b 1
)

"%UI_PYTHON%" --version

if errorlevel 1 (
    echo ERROR: Shakthi AI Python is not working.
    pause
    exit /b 1
)

echo       OK
echo.

REM ------------------------------------------------------------
REM Backend
REM ------------------------------------------------------------

echo [2/6] Checking Shakthi AI backend...

if not exist "%BACKEND_ROOT%\pipeline\rag_pipeline.py" (
    echo ERROR: Backend not found.
    echo Expected:
    echo %BACKEND_ROOT%
    echo.
    pause
    exit /b 1
)

echo       Backend found.
echo.

REM ------------------------------------------------------------
REM Kannada ASR
REM ------------------------------------------------------------

echo [3/6] Checking Kannada ASR...

if not exist "%ASR_PYTHON%" (
    echo ERROR: Kannada ASR Python environment not found.
    echo Expected:
    echo %ASR_PYTHON%
    echo.
    echo Run Setup_Shakthi_AI.bat first.
    pause
    exit /b 1
)

if not exist "%ASR_SCRIPT%" (
    echo ERROR: Kannada ASR script not found.
    echo Expected:
    echo %ASR_SCRIPT%
    pause
    exit /b 1
)

if not exist "%ASR_MODEL%" (
    echo ERROR: Kannada ASR model not found.
    echo Expected:
    echo %ASR_MODEL%
    pause
    exit /b 1
)

echo       ASR environment: OK
echo       ASR script:      OK
echo       ASR model:       OK
echo.

REM ------------------------------------------------------------
REM FFmpeg
REM ------------------------------------------------------------

echo [4/6] Checking FFmpeg...

where ffmpeg >nul 2>&1

if errorlevel 1 (
    echo ERROR: FFmpeg was not found.
    echo Install FFmpeg before running Shakthi AI.
    pause
    exit /b 1
)

echo       OK
echo.

REM ------------------------------------------------------------
REM Ollama
REM ------------------------------------------------------------

echo [5/6] Checking local Ollama...

where ollama >nul 2>&1

if errorlevel 1 (
    echo ERROR: Ollama was not found.
    echo Install Ollama before running Shakthi AI.
    pause
    exit /b 1
)

echo       Ollama found.

curl.exe -s --max-time 3 http://127.0.0.1:11434/api/tags >nul 2>&1

if errorlevel 1 (
    echo       Starting local Ollama...

    start "" /B ollama serve

    set "OLLAMA_READY=0"

    for /L %%N in (1,1,20) do (
        timeout /t 1 /nobreak >nul

        curl.exe -s --max-time 2 http://127.0.0.1:11434/api/tags >nul 2>&1

        if not errorlevel 1 (
            set "OLLAMA_READY=1"
            goto :OLLAMA_READY
        )
    )

    if "!OLLAMA_READY!"=="0" (
        echo ERROR: Local Ollama did not become ready.
        pause
        exit /b 1
    )
)

:OLLAMA_READY

echo       Ollama is ready.

ollama list | findstr /I "gemma3:4b" >nul 2>&1

if errorlevel 1 (
    echo ERROR: gemma3:4b is not installed locally.
    echo.
    echo The model must be transferred/installed before
    echo offline use.
    pause
    exit /b 1
)

echo       gemma3:4b found locally.
echo.

REM ------------------------------------------------------------
REM Streamlit
REM ------------------------------------------------------------

echo [6/6] Checking local Streamlit...

"%UI_PYTHON%" -m streamlit --version

if errorlevel 1 (
    echo ERROR: Streamlit is not installed correctly.
    pause
    exit /b 1
)

echo       OK
echo.

REM ------------------------------------------------------------
REM Launch
REM ------------------------------------------------------------

echo ============================================================
echo Launching Shakthi AI
echo ============================================================
echo.
echo Application root:
echo %APP_ROOT%
echo.
echo Backend:
echo %BACKEND_ROOT%
echo.
echo ASR:
echo %ASR_ROOT%
echo.
echo Local URL:
echo http://127.0.0.1:8501
echo.
echo Air-gapped runtime variables configured.
echo No package installation or model download will be performed.
echo.

cd /d "%APP_ROOT%"

start "" "%UI_PYTHON%" -m streamlit run "%APP_ROOT%\app.py" --server.address 127.0.0.1 --server.port 8501

echo Waiting for Streamlit...

set "STREAMLIT_READY=0"

for /L %%N in (1,1,30) do (
    timeout /t 1 /nobreak >nul

    curl.exe -s --max-time 2 http://127.0.0.1:8501/_stcore/health >nul 2>&1

    if not errorlevel 1 (
        set "STREAMLIT_READY=1"
        goto :STREAMLIT_READY
    )
)

:STREAMLIT_READY

if "!STREAMLIT_READY!"=="0" (
    echo WARNING: Streamlit health endpoint did not respond yet.
    echo The application process may still be starting.
) else (
    echo       Streamlit is ready.
)

echo.
echo Opening Shakthi AI...

start "" http://127.0.0.1:8501

echo.
echo ============================================================
echo Shakthi AI is running locally.
echo ============================================================
echo.

pause
