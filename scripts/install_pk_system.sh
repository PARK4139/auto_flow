#!/bin/bash
# pk_system 자동 설치 스크립트 - Linux/WSL 래퍼
# Python 스크립트를 호출하는 간단한 래퍼

echo "__________________________________________________________________"
echo "# Python 설치 확인"
echo "__________________________________________________________________"

# Python 명령어 찾기
PYTHON_CMD=""

# uv Python 확인 (uv run python)
if command -v uv >/dev/null 2>&1; then
    if uv python --version >/dev/null 2>&1; then
        PYTHON_CMD="uv run python"
    fi
fi

# python3 확인
if [ -z "$PYTHON_CMD" ] && command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
fi

# python 확인
if [ -z "$PYTHON_CMD" ] && command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
fi

# Python 없으면 오류
if [ -z "$PYTHON_CMD" ]; then
    echo ""
    echo "__________________________________________________________________"
    echo "# Python을 찾을 수 없습니다"
    echo "__________________________________________________________________"
    echo ""
    echo "Python 설치 방법:"
    echo "Ubuntu/Debian: sudo apt update && sudo apt install python3"
    echo "CentOS/RHEL: sudo yum install python3"
    echo "macOS: brew install python3"
    echo ""
    echo "또는 uv로 Python 설치:"
    echo "uv python install"
    echo ""
    exit 1
fi

# Python 버전 확인
echo "Python 명령어: $PYTHON_CMD"
if ! $PYTHON_CMD --version 2>/dev/null; then
    echo ""
    echo "__________________________________________________________________"
    echo "# Python 실행 실패"
    echo "__________________________________________________________________"
    echo ""
    echo "Python이 올바르게 설치되었는지 확인해주세요."
    exit 1
fi
echo ""

# 가상 환경 변수 임시 제거 (시스템 Python 사용)
if [ -n "$VIRTUAL_ENV" ]; then
    export VIRTUAL_ENV_BACKUP="$VIRTUAL_ENV"
    unset VIRTUAL_ENV
fi

# 스크립트 디렉토리에서 Python 스크립트 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="${SCRIPT_DIR}/install_pk_system.py"

# Python 스크립트 존재 확인
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo ""
    echo "__________________________________________________________________"
    echo "# install_pk_system.py 파일을 찾을 수 없습니다"
    echo "__________________________________________________________________"
    echo ""
    echo "경로: $PYTHON_SCRIPT"
    exit 1
fi

# Python 스크립트 실행
export PYTHONIOENCODING=utf-8
export PYTHONNOUSERSITE=1
echo ""
echo "__________________________________________________________________"
echo "# Python 스크립트 실행 중"
echo "__________________________________________________________________"
echo ""
$PYTHON_CMD -u "$PYTHON_SCRIPT" "$@"
EXIT_CODE=$?

# 가상 환경 변수 복원
if [ -n "$VIRTUAL_ENV_BACKUP" ]; then
    export VIRTUAL_ENV="$VIRTUAL_ENV_BACKUP"
    unset VIRTUAL_ENV_BACKUP
fi

# 오류 발생 시 메시지
if [ $EXIT_CODE -ne 0 ]; then
    echo ""
    echo "__________________________________________________________________"
    echo "# 오류 발생"
    echo "__________________________________________________________________"
    echo ""
    echo "종료 코드: $EXIT_CODE"
    echo ""
fi

exit $EXIT_CODE
