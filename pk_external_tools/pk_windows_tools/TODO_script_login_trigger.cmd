title pk 메인콘솔 
@echo off
setlocal

:: 경로 설정
set "SCRIPT_DIR=%USERPROFILE%\Downloads\pk_system"
set "VENV_ACTIVATE=%SCRIPT_DIR%\.venv\Scripts\activate.bat"
set "PKG_DIR=%SCRIPT_DIR%\pk_external_tools"
set "USER_SCRIPT=%SCRIPT_DIR%\_temp_user_run.bat"

:: 관리자 권한 여부 확인
whoami /groups | find "S-1-16-12288" >nul
if %errorlevel%==0 (
    echo 현재 관리자 권한입니다. 사용자 권한으로 다시 실행합니다...

    :: 사용자 권한으로 실행할 배치 파일을 생성
    > "%USER_SCRIPT%" (
        echo @echo off
        echo call "%VENV_ACTIVATE%"
        echo cd /d "%PKG_DIR%"
        echo python ensure_pk_wrapper_starter_executed
        echo python pk_wsl.py
        echo python pk_shell_start_up.py
        echo cmd /k
    )

    :: 사용자 권한으로 새 CMD 창 열고 사용자 권한 배치 실행
    powershell -windowstyle hidden -command ^
        "Start-Process cmd -ArgumentList '/c \"%USER_SCRIPT%\"' -WorkingDirectory '%SCRIPT_DIR%'"

    :: 임시 스크립트가 너무 빨리 지워지지 않도록 약간 대기 후 삭제
    timeout /t 3 >nul
    del "%USER_SCRIPT%"
    exit /b
)

:: 이미 사용자 권한이면 여기에 도달함
echo 일반 사용자 권한으로 실행 중입니다.
call "%VENV_ACTIVATE%"
cd /d "%PKG_DIR%"
python pk_shell_start_up.py
cmd /k
