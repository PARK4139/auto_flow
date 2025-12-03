@echo off
REM 프로젝트 루트 디렉토리로 이동
cd /d "%~dp0\.."
title auto_flow_run

echo Running application...

REM 가상 환경을 활성화하고 메인 스크립트를 실행합니다.
set "VENV_PATH=%~dp0\..\.venv"

if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

call "%VENV_PATH%\Scripts\activate.bat"
python __main__.py

REM 스크립트가 종료되므로 비활성화가 필수는 아니지만, 좋은 습관입니다.
call deactivate