@echo off
REM 프로젝트 루트 디렉토리로 이동 (bin의 부모 디렉토리)
cd /d "%~dp0\.."

REM 가상환경의 Python 실행 파일 경로
set VENV_PYTHON=.venv\Scripts\python.exe

REM 가상환경이 존재하는지 확인
if not exist "%VENV_PYTHON%" (
    echo 오류: 가상환경을 찾을 수 없습니다. .venv\Scripts\python.exe 파일이 존재하는지 확인해주세요.
    pause
    exit /b 1
)

REM 메인 스크립트 실행
"%VENV_PYTHON%" __main__.py

REM 오류 발생 시 일시 정지
if errorlevel 1 (
    pause
)



