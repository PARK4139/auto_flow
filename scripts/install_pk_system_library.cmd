@echo off
REM pk_system auto installation script - Windows wrapper
REM Simple wrapper to call Python script

chcp 65001 >nul
setlocal enabledelayedexpansion

echo __________________________________________________________________
echo # Python 설치 확인
echo __________________________________________________________________

REM Find Python command
set "PYTHON_CMD="

REM Check uv Python (uv run python)
where uv >nul 2>&1
if not errorlevel 1 (
    uv run python --version >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=uv run python"
        goto :python_found
    )
)

REM Check py launcher
where py >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=py -3"
    goto :python_found
)

REM Check python3
where python3 >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python3"
    goto :python_found
)

REM Check python
where python >nul 2>&1
if not errorlevel 1 (
    set "PYTHON_CMD=python"
    goto :python_found
)

REM Python not found
echo.
echo __________________________________________________________________
echo # Python을 찾을 수 없습니다
echo __________________________________________________________________
echo.
echo Python 설치 방법:
echo Download: https://www.python.org/downloads/
echo 설치 시 "Add Python to PATH" 옵션을 선택하세요.
echo.
echo 또는 Python launcher (py) 설치:
echo Windows Store에서 "Python" 검색 후 설치
echo.
echo 또는 uv로 Python 설치:
echo uv python install
echo.
pause
exit /b 1

:python_found
REM Check Python version
echo Python command: !PYTHON_CMD!
!PYTHON_CMD! --version 2>&1
if errorlevel 1 (
    echo.
    echo __________________________________________________________________
    echo # Python 실행 실패
    echo __________________________________________________________________
    echo.
    echo Python이 올바르게 설치되었는지 확인해주세요.
    pause
    exit /b 1
)
echo.

REM Remove virtual environment variables
if defined VIRTUAL_ENV (
    set "VIRTUAL_ENV_BACKUP=!VIRTUAL_ENV!"
    set "VIRTUAL_ENV="
)
if defined CONDA_DEFAULT_ENV (
    set "CONDA_DEFAULT_ENV_BACKUP=!CONDA_DEFAULT_ENV!"
    set "CONDA_DEFAULT_ENV="
)
if defined PIP_REQUIRE_VENV (
    set "PIP_REQUIRE_VENV_BACKUP=!PIP_REQUIRE_VENV!"
    set "PIP_REQUIRE_VENV="
)

REM Find script directory
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=!SCRIPT_DIR!install_pk_system_library.py"

REM Check if Python script exists
if not exist "!PYTHON_SCRIPT!" (
    echo.
    echo __________________________________________________________________
    echo # install_pk_system_library.py 파일을 찾을 수 없습니다
    echo __________________________________________________________________
    echo.
    echo 경로: !PYTHON_SCRIPT!
    pause
    exit /b 1
)

REM Execute Python script
set "PYTHONIOENCODING=utf-8"
set "PYTHONNOUSERSITE=1"
echo.
echo __________________________________________________________________
echo # Python 스크립트 실행 중
echo __________________________________________________________________
echo.

!PYTHON_CMD! -u "!PYTHON_SCRIPT!" %* 2>&1
set "EXIT_CODE=!ERRORLEVEL!"

REM Restore virtual environment variables
if defined VIRTUAL_ENV_BACKUP (
    set "VIRTUAL_ENV=!VIRTUAL_ENV_BACKUP!"
    set "VIRTUAL_ENV_BACKUP="
)
if defined CONDA_DEFAULT_ENV_BACKUP (
    set "CONDA_DEFAULT_ENV=!CONDA_DEFAULT_ENV_BACKUP!"
    set "CONDA_DEFAULT_ENV_BACKUP="
)
if defined PIP_REQUIRE_VENV_BACKUP (
    set "PIP_REQUIRE_VENV=!PIP_REQUIRE_VENV_BACKUP!"
    set "PIP_REQUIRE_VENV_BACKUP="
)

REM Show error message if any
if !EXIT_CODE! neq 0 (
    echo.
    echo __________________________________________________________________
    echo # 오류 발생
    echo __________________________________________________________________
    echo.
    echo 종료 코드: !EXIT_CODE!
    echo.
)

REM Always pause
pause

exit /b !EXIT_CODE!
