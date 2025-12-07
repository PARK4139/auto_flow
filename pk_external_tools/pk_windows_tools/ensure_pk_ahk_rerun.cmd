@chcp 65001 >nul
@echo off
setlocal

:: 경로 설정
set AHK_FOLDER=%USERPROFILE%\Downloads\pk_archived\AutoHotkey_Portable
set AHK_EXE=%AHK_FOLDER%\AutoHotkeyU64.exe
set AHK_SCRIPT=%USERPROFILE%\Downloads\pk_system\pk_os_layer_resources\pk_shortcut.ahk

:: AHK 실행 확인
if not exist "%AHK_EXE%" (
    echo ❌ AHK 실행 파일이 존재하지 않습니다: %AHK_EXE%
    pause
    exit /b
)

:: 스크립트 실행
start "" "%AHK_EXE%" "%AHK_SCRIPT%"

echo ---------------------------------------
echo ✔ AHK 스크립트 실행됨: %AHK_SCRIPT%
@REM timeout /t 3 
