@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
@REM setlocal EnableExtensions EnableDelayedExpansion

set "d_pk_system=%USERPROFILE%\Downloads\pk_system"
set "d_pk_external_tools=%USERPROFILE%\Downloads\pk_system\pk_os_layer_resources"
set "D_VENV=%d_pk_system%\.venv"
set "F_UV_PYTHON=%D_VENV%\Scripts\python.exe"
set "F_UV_ACTIVATE=%D_VENV%\Scripts\activate"
set "F_ENSURE_UV_ENABLED_CMD=%d_pk_external_tools%\ensure_uv_enabled.cmd"
set "F_UV=%d_pk_system%\uv.exe"


@REM     echo uv 미설치, uv 를 설치해야 합니다.
@REM    call "%F_ENSURE_UV_ENABLED_CMD%"

REM === virtual environment 확인/생성 ===
if exist "%F_UV_PYTHON%" (
    echo pk_system virtual environment python detected: "%F_UV_PYTHON%"
    call "%F_UV_ACTIVATE%"
    goto :run_script
) else (
    if exist "%D_VENV%" (
        echo .venv virtual environment 경로 발견 %D_VENV%
    ) else (
        cd /d %d_pk_system%
        %F_UV% venv ".venv" || (echo ❌ uv venv 생성 실패 & popd & exit /b 1)
        call "%F_UV_ACTIVATE%"
@REM         %F_UV% sync -vvv
        %F_UV% sync
    )

    popd
    if exist "%F_UV_PYTHON%" (
        echo pk_system virtual environment python detected: "%F_UV_PYTHON%"
        goto :run_script
    ) else (
        echo ❌ virtual environment Python 경로가 없습니다: "%F_UV_PYTHON%"
        exit /b 1
        pause
    )
)


@REM TODO : ensure_python_installed.cmd
@REM @REM Python을 찾을 수 없는 경우
@REM echo ❌ Python을 찾을 수 없습니다.
@REM echo ✅ Python 설치를 시도합니다...
@REM echo.
@REM echo 다음 중 하나를 선택하세요:
@REM echo 1. Microsoft Store에서 Python 설치 (권장)
@REM echo 2. python.org에서 수동 설치
@REM echo 3. 취소
@REM echo.
@REM set /p choice="선택 (1-3): "
@REM if "%choice%"=="1" (
@REM     echo 🛒 Microsoft Store에서 Python 설치 중...
@REM     start ms-windows-store://pdp/?ProductId=9PNRBTZXMB4Z
@REM     echo 설치 완료 후 이 스크립트를 다시 실행하세요.
@REM     pause
@REM     exit /b 1
@REM ) else if "%choice%"=="2" (
@REM     echo 🌐 python.org로 이동 중...
@REM     start https://www.python.org/downloads/
@REM     echo 설치 완료 후 이 스크립트를 다시 실행하세요.
@REM     pause
@REM     exit /b 1
@REM ) else (
@REM     echo 취소되었습니다.
@REM     pause
@REM     exit /b 1
@REM )

:run_script
echo 실행 중: %F_UV_PYTHON% -m pk_internal_tools.pk_wrappers.pk_ensure_pk_enabled
if exist "%F_UV_ACTIVATE%" (
    cd /d "%d_pk_system%"
    @REM     call "%d_pk_system%\.venv\Scripts\activate"   (이거 잘 동작함)
    call "%F_UV_ACTIVATE%"
    uv run -m pk_internal_tools.pk_wrappers.pk_ensure_pk_enabled
)