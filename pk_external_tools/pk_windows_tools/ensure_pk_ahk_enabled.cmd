@chcp 65001 >nul
@echo off
setlocal

echo [AutoHotKey 포터블 다운로드 및 실행 준비 중...]

:: 경로 설정
set AHK_ZIP_URL=https://www.autohotkey.com/download/1.1/AutoHotkey_1.1.36.02.zip
set F_AHK_PORTABLE_ZIP=%USERPROFILE%\Downloads\pk_archived\AutoHotkey_Portable.zip
set D_AHK_PORTABLE=%USERPROFILE%\Downloads\pk_archived\AutoHotkey_Portable
set F_AHK_EXE=%D_AHK_PORTABLE%\AutoHotkeyU64.exe
set F_PK_SHORTCUT_AHK=%USERPROFILE%\Downloads\pk_system\pk_os_layer_resources\pk_shortcut.ahk

cd /d "%USERPROFILE%\Downloads"

:: 정리
if exist "%F_AHK_PORTABLE_ZIP%" del /f /q "%F_AHK_PORTABLE_ZIP%"
if exist "%D_AHK_PORTABLE%" rmdir /s /q "%D_AHK_PORTABLE%"

echo [1/3] 포터블 AHK 다운로드 중...
curl -L -o "%F_AHK_PORTABLE_ZIP%" "%AHK_ZIP_URL%"

if not exist "%F_AHK_PORTABLE_ZIP%" (
    echo 다운로드 실패! 인터넷 연결 또는 curl 사용 가능 여부 확인.
    pause
    exit /b
)

echo [2/3] 압축해제 시도 중...
powershell -NoLogo -NoProfile -ExecutionPolicy Bypass ^
  -Command "Expand-Archive -Path '%F_AHK_PORTABLE_ZIP%' -DestinationPath '%D_AHK_PORTABLE%' -Force"

if not exist "%F_AHK_EXE%" (
    echo ❌ 실행 파일이 없습니다: %F_AHK_EXE%
    echo 압축해제에 실패했거나 ZIP 구조가 바뀌었을 수 있습니다.
    echo 폴더를 정리합니다...
    if exist "%D_AHK_PORTABLE%" rmdir /s /q "%D_AHK_PORTABLE%"
    if exist "%F_AHK_PORTABLE_ZIP%" del /f /q "%F_AHK_PORTABLE_ZIP%"
    pause
    exit /b
)

echo [3/3] 포터블 AHK 실행 및 단축키 스크립트 실행 중...
start "" "%F_AHK_EXE%" "%F_PK_SHORTCUT_AHK%"

:: 다운로드 ZIP 제거
if exist "%F_AHK_PORTABLE_ZIP%" del /f /q "%F_AHK_PORTABLE_ZIP%"

echo ---------------------------------------
echo ✔ pk shortcut is imported