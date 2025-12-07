@echo off
REM Windows 환경에서 테스트 환경 자동 활성화 스크립트
REM virtual environment 을 자동으로 활성화하고 테스트를 실행

setlocal enabledelayedexpansion

REM 프로젝트 루트 디렉토리로 이동
cd /d "%~dp0\.."
set PROJECT_ROOT=%CD%
echo [INFO] 프로젝트 루트: %PROJECT_ROOT%

REM OS 환경 확인
echo [INFO] Windows 환경 감지됨

REM virtual environment 찾기
set VENV_PATH=
if exist "%PROJECT_ROOT%\.venv" (
    set VENV_PATH=%PROJECT_ROOT%\.venv
    echo [INFO] Windows virtual environment 발견: %VENV_PATH%
) else if exist "%PROJECT_ROOT%\venv" (
    set VENV_PATH=%PROJECT_ROOT%\venv
    echo [INFO] 기본 virtual environment 발견: %VENV_PATH%
) else if exist "%PROJECT_ROOT%\env" (
    set VENV_PATH=%PROJECT_ROOT%\env
    echo [INFO] 환경 virtual environment 발견: %VENV_PATH%
) else (
    echo [WARNING] virtual environment 을 찾을 수 없음
)

REM Python 실행 파일 찾기
set PYTHON_CMD=
where uv >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=uv
    echo [INFO] uv 발견됨
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% == 0 (
        set PYTHON_CMD=python
        echo [INFO] python 발견됨
    ) else (
        where python3 >nul 2>&1
        if %ERRORLEVEL% == 0 (
            set PYTHON_CMD=python3
            echo [INFO] python3 발견됨
        ) else (
            where py >nul 2>&1
            if %ERRORLEVEL% == 0 (
                set PYTHON_CMD=py
                echo [INFO] py 발견됨
            ) else (
                echo [ERROR] Python 실행 파일을 찾을 수 없음
                exit /b 1
            )
        )
    )
)

REM virtual environment 활성화
if defined VENV_PATH (
    echo [INFO] virtual environment 활성화 중: %VENV_PATH%
    
    if exist "%VENV_PATH%\Scripts\activate.bat" (
        call "%VENV_PATH%\Scripts\activate.bat"
        echo [SUCCESS] virtual environment 활성화 완료
        
        REM Python 경로 확인
        where python
        set VENV_PYTHON=%ERRORLEVEL%
        echo [INFO] virtual environment Python: %VENV_PYTHON%
    ) else (
        echo [WARNING] virtual environment 활성화 스크립트를 찾을 수 없음
    )
) else (
    echo [WARNING] virtual environment 없음 - 시스템 Python 사용
)

REM 의존성 설치
echo [INFO] 의존성 설치 확인 중...

if exist "%PROJECT_ROOT%\uv.lock" (
    echo [INFO] uv.lock 파일 발견 - uv sync 실행
    where uv >nul 2>&1
    if %ERRORLEVEL% == 0 (
        cd /d "%PROJECT_ROOT%"
        uv sync --active
        echo [SUCCESS] uv sync --active 완료
    ) else (
        echo [WARNING] uv 명령어를 찾을 수 없음
    )
) else if exist "%PROJECT_ROOT%\requirements.txt" (
    echo [INFO] requirements.txt 파일 발견 - pip install 실행
    cd /d "%PROJECT_ROOT%"
    %PYTHON_CMD% -m pip install -r requirements.txt
    echo [SUCCESS] pip install 완료
) else if exist "%PROJECT_ROOT%\pyproject.toml" (
    echo [INFO] pyproject.toml 파일 발견 - pip install -e 실행
    cd /d "%PROJECT_ROOT%"
    %PYTHON_CMD% -m pip install -e .
    echo [SUCCESS] pip install -e 완료
) else (
    echo [WARNING] 의존성 설치 파일을 찾을 수 없음
)

REM 테스트 실행
echo [INFO] 테스트 실행 준비 완료

if "%1"=="" (
    REM 기본 테스트 실행
    echo [INFO] 기본 테스트 실행 중...
    
    if exist "%PROJECT_ROOT%\pk_internal_tools\pk_wrappers\pk_functions\ensure_losslesscut_pk_event_test.py" (
        cd /d "%PROJECT_ROOT%\pk_internal_tools\pk_wrappers\pk_functions"
        echo [INFO] LosslessCut Event 시스템 테스트 실행
        %PYTHON_CMD% ensure_losslesscut_pk_event_test.py
        echo [SUCCESS] 테스트 완료
    ) else (
        echo [WARNING] 기본 테스트 파일을 찾을 수 없음
    )
) else (
    REM 지정된 테스트 실행
    set TEST_FILE=%1
    echo [INFO] 지정된 테스트 실행: %TEST_FILE%
    
    if exist "%TEST_FILE%" (
        cd /d "%TEST_FILE%\.."
        %PYTHON_CMD% "%TEST_FILE%"
        echo [SUCCESS] 테스트 완료
    ) else (
        echo [ERROR] 테스트 파일을 찾을 수 없음: %TEST_FILE%
        exit /b 1
    )
)

echo [SUCCESS] 모든 작업 완료!
endlocal
