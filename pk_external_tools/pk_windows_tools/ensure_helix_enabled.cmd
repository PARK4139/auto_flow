@echo off
chcp 65001 >nul

setlocal enabledelayedexpansion
set "HX_URL=https://github.com/helix-editor/helix/releases/download/25.01.1/helix-25.01.1-x86_64-windows.zip"
set "HX_DIR=C:\helix"
set "HX_ZIP=%TEMP%\helix.zip"

echo.
echo [1/5] Helix 다운로드 중...
powershell -Command "Invoke-WebRequest -Uri !HX_URL! -OutFile !HX_ZIP!" || (
    echo 다운로드 실패. 종료합니다.
    exit /b 1
)

echo [2/5] Helix 설치 경로 초기화...
if exist "!HX_DIR!" rmdir /s /q "!HX_DIR!"
mkdir "!HX_DIR!" >nul 2>&1

echo [3/5] Helix 압축해제 중...
powershell -Command "Expand-Archive -Path !HX_ZIP! -DestinationPath !HX_DIR! -Force" || (
    echo 압축해제 실패. 종료합니다.
    exit /b 1
)

echo [4/5] Helix 설치 경로 확인 중...
for /d %%D in ("!HX_DIR!\*") do (
    if exist "%%D\hx.exe" (
        set "HX_DIR=%%D"
        goto :SET_PATH
    )
)

:SET_PATH
echo 환경 변수 설정 중...
setx PATH "%PATH%;!HX_DIR!" >nul

echo.
echo Helix 버전 확인:
"%HX_DIR%\hx.exe" --version || (
    echo Helix 실행에 실패했습니다. 환경 변수가 제대로 설정되지 않았을 수 있습니다.
)

echo.
echo [5/5] 다운로드된 helix.zip 파일 삭제 중...
del /f /q "!HX_ZIP!" >nul 2>&1

echo.
echo 설치 및 정리 완료.
