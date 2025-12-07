chcp 65001 
@echo off
setlocal

set "modeFile=%TEMP%\display_mode.txt"

rem modeFile이 존재하지 않으면 기본값으로 'internal' 설정
if not exist "%modeFile%" (
    echo internal > "%modeFile%"
)

rem 현재 모드 읽기
set /p currentMode=<"%modeFile%"

rem 모드 전환
if "%currentMode%"=="internal" (
    echo 현재 모드는 '1번 디스플레이에만 표시'입니다. '디스플레이 확장' 모드로 전환합니다.
    DisplaySwitch.exe /extend
    echo extend > "%modeFile%"
) else (
    echo 현재 모드는 '디스플레이 확장'입니다. '1번 디스플레이에만 표시' 모드로 전환합니다.
    DisplaySwitch.exe /internal
    echo internal > "%modeFile%"
)

endlocal
