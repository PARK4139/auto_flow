@echo off
setlocal enabledelayedexpansion

echo 🐍 pk_system Enable Script (Windows)
echo ==================================================

:: 현재 스크립트 위치
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\..\..\.."
set "USER_HOME=%USERPROFILE%"

echo 📁 Script directory: %SCRIPT_DIR%
echo 📁 Project root: %PROJECT_ROOT%

:: Python 찾기
echo 🔍 Python 찾는 중...

:: 1. 시스템 python 확인
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 시스템 Python 발견: python
    set "PYTHON_CMD=python"
    goto :run_script
)

:: 2. python3 확인
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 시스템 Python 발견: python3
    set "PYTHON_CMD=python3"
    goto :run_script
)

:: 3. virtual environment python 확인
if exist "%PROJECT_ROOT%\.venv\Scripts\python.exe" (
echo pk_system virtual environment python detected: .venv\Scripts\python.exe
set "PYTHON_CMD=%PROJECT_ROOT%\.venv\Scripts\python.exe"
    goto :run_script
)

:: Python을 찾을 수 없는 경우
echo ❌ Python을 찾을 수 없습니다.
echo 📥 Python 설치를 시도합니다...
echo.
echo 다음 중 하나를 선택하세요:
echo 1. python.org에서 수동 설치 (권장)
echo 2. Microsoft Store에서 설치
echo 3. 취소
echo.
set /p choice="선택 (1-3): "

if "%choice%"=="1" (
    echo 🌐 python.org로 이동 중...
    echo https://www.python.org/downloads/
    echo 설치 완료 후 이 스크립트를 다시 실행하세요.
    pause
    exit /b 1
) else if "%choice%"=="2" (
    echo 🛒 Microsoft Store에서 Python 설치 중...
    start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
    echo 설치 완료 후 이 스크립트를 다시 실행하세요.
    pause
    exit /b 1
) else if "%choice%"=="3" (
    echo 취소되었습니다.
    exit /b 1
) else (
    echo 잘못된 선택입니다.
    exit /b 1
)

:run_script
:: Python 스크립트 실행
echo 🚀 Python 스크립트 실행 중: %PYTHON_CMD% pk_internal_tools\pk_wrappers\pk_ensure_pk_enabled.py
cd /d "%PROJECT_ROOT%"

if exist "pk_internal_tools\pk_wrappers\pk_ensure_pk_enabled.py" (
    %PYTHON_CMD% pk_internal_tools\pk_wrappers\pk_ensure_pk_enabled.py
    set EXIT_CODE=%errorlevel%
    
    if %EXIT_CODE% equ 0 (
        echo ✅ 스크립트 실행 완료
    ) else (
        echo ❌ 스크립트 실행 실패 (오류 코드: %EXIT_CODE%)
        exit /b %EXIT_CODE%
    )
) else (
    echo ❌ pk_ensure_pk_enabled.py 파일을 찾을 수 없습니다.
    echo 📁 찾는 경로: %PROJECT_ROOT%\pk_internal_tools\pk_wrappers\pk_ensure_pk_enabled.py
    echo 📁 현재 디렉토리: %CD%
    echo 📋 파일 목록:
    dir pk_internal_tools\pk_wrappers\*.py 2>nul || echo   (Python 파일 없음)
    exit /b 1
)

echo ==================================================
echo ✅ pk_system Enable Script 완료
pause 