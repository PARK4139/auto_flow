@echo off
title ensure_pk_wrapper_executed.cmd
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Get the directory of this script (where this batch file is located)
SET "PK_USERPROFILE=%USERPROFILE%"
SET "PROJECT_ROOT=%PK_USERPROFILE%\Downloads\pk_system"

REM Change to the project root
cd /d "%PROJECT_ROOT%"

REM Construct full absolute paths
SET "F_UV_PYTHON_EXE=%PK_USERPROFILE%\Downloads\pk_system\.venv\Scripts\python.exe"
SET "F_PK_ENSURE_PK_WRAPPER_STARTED_PY=%PK_USERPROFILE%\Downloads\pk_system\pk_internal_tools\pk_wrappers\pk_ensure_pk_system_cli_executed.py"

REM Debugging: Verify calculated paths
echo Debugging: Current CD is "%CD%"
echo Debugging: Calculated PROJECT_ROOT is "%PROJECT_ROOT%"
echo Debugging: F_UV_PYTHON_EXE is "%F_UV_PYTHON_EXE%"
echo Debugging: F_PK_ENSURE_PK_WRAPPER_STARTED_PY is "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%"
echo Debugging: Quoted F_UV_PYTHON_EXE is "%F_UV_PYTHON_EXE%"
echo Debugging: Quoted F_PK_ENSURE_PK_WRAPPER_STARTED_PY is "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%"

REM Check if the target script exists using 'where' command
where "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%" >nul 2>nul
if !ERRORLEVEL! NEQ 0 (
    echo pk_error: Target script not found at "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%"
    pause
    exit /b 1
)

REM Execute the script

"%F_UV_PYTHON_EXE%" "%F_PK_ENSURE_PK_WRAPPER_STARTED_PY%"

set PYTHON_EXIT_CODE=!ERRORLEVEL!

REM Python 실행 후 즉시 ERRORLEVEL 저장 (다른 명령이 ERRORLEVEL을 덮어쓸 수 있음)
REM timeout 명령 전에 이미 저장했으므로 안전함

REM Check if Python script exited with an error
if !PYTHON_EXIT_CODE! NEQ 0 (
    echo.
    echo ============================================================
    echo # pk_error
    echo 오류 코드: !PYTHON_EXIT_CODE!
    echo.
    echo 위의 traceback을 확인하세요.
    echo.
    echo continue:enter
    echo ============================================================
    pause >nul
    exit /b !PYTHON_EXIT_CODE!
)
endlocal
echo.
echo Script finished.
echo.
echo exit:enter
pause

