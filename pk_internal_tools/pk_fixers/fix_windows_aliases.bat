@echo off
echo ========================================
echo Windows pk_system 별칭 문제 해결 도구
echo ========================================

echo.
echo 1. 현재 레지스트리 AutoRun 설정 확인:
reg query "HKCU\Software\Microsoft\Command Processor" /v AutoRun

echo.
echo 2. 기존 AutoRun 설정 제거:
reg delete "HKCU\Software\Microsoft\Command Processor" /v AutoRun /f

echo.
echo 3. 새로운 배치 파일 기반 AutoRun 설정:
set "pk_PATH=C:\Users\wjdgn\Downloads\pk_system"
set "BATCH_FILE=%pk_PATH%\pk_cache_private\pk_doskey.bat"

if exist "%BATCH_FILE%" (
    reg add "HKCU\Software\Microsoft\Command Processor" /v AutoRun /t REG_SZ /d "\"%BATCH_FILE%\"" /f
    echo ✅ 새로운 AutoRun 설정 완료: %BATCH_FILE%
) else (
    echo ❌ 배치 파일을 찾을 수 없습니다: %BATCH_FILE%
)

@REM TODO : 별칭재등록

echo 5. 등록된 별칭 확인:
doskey /macros

echo.
echo ========================================
echo 문제 해결 완료!
echo 새 CMD 창을 열어서 별칭이 작동하는지 확인하세요.
echo ========================================
pause 