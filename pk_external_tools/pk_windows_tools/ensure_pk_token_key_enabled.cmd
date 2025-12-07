@echo off
chcp 65001 >nul

setlocal enabledelayedexpansion

REM [1] 설정
set "GIT_REPO_URL=https://github.com/PARK4139/pk_data.git"
set "DOWNLOADS_DIR=%USERPROFILE%\Downloads"
set "TARGET_DIR=%DOWNLOADS_DIR%\pk_system\pk_data"
set "CLONE_DIR=%DOWNLOADS_DIR%\pk_data"
set "TOML_FILE=pk_token_key.toml"
set "TOML_SRC=%CLONE_DIR%\%TOML_FILE%"

REM [2] 다운로드 디렉토리로 이동
cd /d "%DOWNLOADS_DIR%" || (
    echo ❌ 다운로드 디렉토리 진입 실패: %DOWNLOADS_DIR%
    exit /b 1
)

REM [3] 기존 clone 디렉토리 제거
if exist "%CLONE_DIR%" (
    echo 🔄 기존 디렉토리 삭제 중: "%CLONE_DIR%"
    rmdir /s /q "%CLONE_DIR%" || (
        echo ❌ 디렉토리 삭제 실패: %CLONE_DIR%
        exit /b 1
    )
)

REM [4] Git 클론
echo 📥 Git 클론 중...
git clone "%GIT_REPO_URL%" || (
    echo ❌ Git clone 실패
    exit /b 1
)

REM [5] TOML 파일 존재 확인
if not exist "%TOML_SRC%" (
    echo ❌ TOML 파일이 존재하지 않음: %TOML_SRC%
    exit /b 1
)

REM [6] 대상 디렉토리 생성 (없으면)
if not exist "%TARGET_DIR%" (
    echo 📁 대상 디렉토리 생성: %TARGET_DIR%
    mkdir "%TARGET_DIR%" || (
        echo ❌ 디렉토리 생성 실패: %TARGET_DIR%
        exit /b 1
    )
)

REM [7] TOML 파일 이동
echo 📄 TOML 파일 이동 중...
move /Y "%TOML_SRC%" "%TARGET_DIR%" || (
    echo ❌ TOML 파일 이동 실패
    exit /b 1
)

REM [8] 클론된 전체 디렉토리 삭제
echo 🧹 불필요한 파일 제거 중...
rmdir /s /q "%CLONE_DIR%" || (
    echo ❌ 클론 디렉토리 삭제 실패
    exit /b 1
)

echo ✅ 모든 작업이 성공적으로 완료되었습니다.
endlocal
