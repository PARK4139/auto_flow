@echo off
title pk_system Hotkey Monitor
cd /d "%d_pk_system%"

REM 백그라운드에서 단축키 모니터링 시작
echo 🎯 pk_system 단축키 모니터링 서비스 시작...
echo 💡 단축키: Ctrl+Alt+P
echo 💡 종료하려면 Ctrl+C를 누르세요
echo.

REM Python virtual environment 활성화 후 모니터링 시작
call .venv\Scripts\activate.bat
python pk_internal_tools\pk_wrappers\pk_functions\ensure_hotkey_monitor_started.py

REM 오류 발생 시 대기
if errorlevel 1 (
    echo ❌ 모니터링 서비스 오류 발생
    pause
) 