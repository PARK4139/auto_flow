@echo off
title %~nx0
chcp 65001 >nul
setlocal enabledelayedexpansion

SET "SCRIPT_DIR=%~dp0"
SET "PYTHONPATH=%SCRIPT_DIR%"
SET "F_UV_PYTHON_EXE=.venv\Scripts\python.exe"
SET "F_PK_ENSURE_PK_WRAPPER_STARTED_PY=pk_internal_tools\pk_wrappers\pk_ensure_pk_system_cli_executed.py"


echo %~nx0 started

@REM below code is for debugging, if you want to debug, 주석해제
@REM echo Debugging: CD is "%CD%"
@REM echo Debugging: SCRIPT_DIR is "%SCRIPT_DIR%"
@REM echo Debugging: F_UV_PYTHON_EXE is "%F_UV_PYTHON_EXE%"
@REM echo Debugging: F_PK_ENSURE_PK_WRAPPER_STARTED_PY is "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%"



REM Change to the project root dynamically
cd /d "%SCRIPT_DIR%"

REM Check if the files exist
if not exist "%F_UV_PYTHON_EXE%" (
    echo pk_error: Python executable not found at "%F_UV_PYTHON_EXE%"
    pause
    exit /b 1
)

if not exist "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%" (
    echo pk_error: Target script not found at "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%"
    pause
    exit /b 1
)

REM Execute the script
"%F_UV_PYTHON_EXE%" "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%"


set PYTHON_EXIT_CODE=!ERRORLEVEL!
if !PYTHON_EXIT_CODE! NEQ 0 (
    echo ============================================================
    echo # Python 스크립트 실행 중 오류 발생
    echo 위의 에러 메시지를 확인하세요.
    echo Python 스크립트가 에러로 종료되었습니다.
    echo 위의 traceback을 확인하세요.
    echo continue:enter
    echo ============================================================
    pause >nul
    exit /b !PYTHON_EXIT_CODE!
)
endlocal

@REM below code is for debugging, if you want to debug, 주석해제
@REM echo.
echo %~nx0 finished.
@REM echo.
@REM echo continue:enter
@REM pause >nul