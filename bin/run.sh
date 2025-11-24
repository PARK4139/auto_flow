#!/bin/bash

# 프로젝트 루트 디렉토리로 이동 (bin의 부모 디렉토리)
cd "$(dirname "$0")/.."

# 가상환경의 Python 실행 파일 경로
VENV_PYTHON=".venv/bin/python"

# 가상환경이 존재하는지 확인
if [ ! -f "$VENV_PYTHON" ]; then
    echo "오류: 가상환경을 찾을 수 없습니다. .venv/bin/python 파일이 존재하는지 확인해주세요."
    exit 1
fi

# 메인 스크립트 실행
"$VENV_PYTHON" __main__.py

