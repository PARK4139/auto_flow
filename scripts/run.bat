@echo off
REM 프로젝트 루트 디렉토리로 이동
cd /d "%~dp0\.."
title auto_flow_setup

echo Running setup script...
REM run.py를 실행하기 위해 시스템 Python을 사용합니다.
REM run.py가 가상환경을 생성하고 관리합니다.
python scripts/run.py

REM 오류 발생 시 일시 정지
if errorlevel 1 (
    echo.
    echo Script failed with an error.
    pause
) else (
    echo.
    echo Script completed successfully.
)
