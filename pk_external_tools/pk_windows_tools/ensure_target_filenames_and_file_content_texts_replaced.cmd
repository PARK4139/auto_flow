chcp 65001
title %~nx0
@echo on
cls

:SAVE_POINT

REM 현재 USERPROFILE 값을 가져오기
setlocal enabledelayedexpansion
set "USERPROFILE_PATH=%USERPROFILE%"

REM 순회할 디렉토리 지정
set "TARGET_DIR=%USERPROFILE%\Downloads\pk_system\.venv"

REM 임시 파일 생성
set "TEMP_FILE=%TEMP%\pyvenv_temp.cfg"

REM 디렉토리 내 모든 파일 순회
for /r "%TARGET_DIR%" %%F in (*) do (
    REM 현재 파일 경로 출력
    echo Processing file: %%F

    REM 파일 읽기 및 치환
    (for /f "usebackq tokens=*" %%A in ("%%F") do (
        set "LINE=%%A"
        set "LINE=!LINE:%USERPROFILE%=%USERPROFILE_PATH%!"
        set "LINE=!LINE:C:\Users\AutonomousTODO=%USERPROFILE_PATH%!"
        echo !LINE!
    )) > "!TEMP_FILE!"

    REM 치환된 내용을 원본 파일로 복사
    move /y "!TEMP_FILE!" "%%F" >nul
)

echo.
echo 모든 파일이 성공적으로 수정되었습니다.

REM 사용자 입력 대기
echo.
echo 계속 exec 하려면 Enter를 누르세요. 종료하려면 Ctrl+C를 누르세요.
pause >nul

REM 루프로 다시 exec
goto SAVE_POINT
