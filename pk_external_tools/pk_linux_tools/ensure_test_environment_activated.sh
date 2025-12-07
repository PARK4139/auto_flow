#!/bin/bash
# Linux/WSL 환경에서 테스트 환경 자동 활성화 스크립트
# virtual environment 을 자동으로 활성화하고 테스트를 실행

set -e  # 오류 발생 시 즉시 종료

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 로깅 함수
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 프로젝트 루트 디렉토리로 이동
cd "$(dirname "$0")/.." || exit 1
PROJECT_ROOT=$(pwd)
log_info "프로젝트 루트: $PROJECT_ROOT"

# OS 환경 확인
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if grep -q Microsoft /proc/version; then
        log_info "WSL 환경 감지됨"
        ENV_TYPE="wsl"
    else
        log_info "Linux 환경 감지됨"
        ENV_TYPE="linux"
    fi
else
    log_warning "지원되지 않는 OS: $OSTYPE"
    ENV_TYPE="unknown"
fi

# virtual environment 찾기
VENV_PATH=""
if [[ -d "$PROJECT_ROOT/.venv" ]]; then
    VENV_PATH="$PROJECT_ROOT/.venv"
    log_info "Linux 전용 virtual environment 발견: $VENV_PATH"
elif [[ -d "$PROJECT_ROOT/.venv" ]]; then
    VENV_PATH="$PROJECT_ROOT/.venv"
    log_info "공통 virtual environment 발견: $VENV_PATH"
elif [[ -d "$PROJECT_ROOT/venv" ]]; then
    VENV_PATH="$PROJECT_ROOT/venv"
    log_info "기본 virtual environment 발견: $VENV_PATH"
else
    log_warning "virtual environment 을 찾을 수 없음"
fi

# Python 실행 파일 찾기
PYTHON_CMD=""
if command -v uv &> /dev/null; then
    PYTHON_CMD="uv"
    log_info "uv 발견됨"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    log_info "python3 발견됨"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    log_info "python 발견됨"
else
    log_error "Python 실행 파일을 찾을 수 없음"
    exit 1
fi

# virtual environment 활성화
if [[ -n "$VENV_PATH" ]]; then
    log_info "virtual environment 활성화 중: $VENV_PATH"
    
    if [[ -f "$VENV_PATH/bin/activate" ]]; then
        source "$VENV_PATH/bin/activate"
        log_success "virtual environment 활성화 완료"
        
        # Python 경로 확인
        VENV_PYTHON=$(which python)
        log_info "virtual environment Python: $VENV_PYTHON"
    else
        log_warning "virtual environment 활성화 스크립트를 찾을 수 없음"
    fi
else
    log_warning "virtual environment 없음 - 시스템 Python 사용"
fi

# 의존성 설치
log_info "의존성 설치 확인 중..."

if [[ -f "$PROJECT_ROOT/uv.lock" ]]; then
    log_info "uv.lock 파일 발견 - uv sync 실행"
    if command -v uv &> /dev/null; then
        cd "$PROJECT_ROOT"
        uv sync --active
        log_success "uv sync --active 완료"
    else
        log_warning "uv 명령어를 찾을 수 없음"
    fi
elif [[ -f "$PROJECT_ROOT/requirements.txt" ]]; then
    log_info "requirements.txt 파일 발견 - pip install 실행"
    cd "$PROJECT_ROOT"
    $PYTHON_CMD -m pip install -r requirements.txt
    log_success "pip install 완료"
elif [[ -f "$PROJECT_ROOT/pyproject.toml" ]]; then
    log_info "pyproject.toml 파일 발견 - pip install -e 실행"
    cd "$PROJECT_ROOT"
    $PYTHON_CMD -m pip install -e .
    log_success "pip install -e 완료"
else
    log_warning "의존성 설치 파일을 찾을 수 없음"
fi

# 테스트 실행
log_info "테스트 실행 준비 완료"

if [[ $# -eq 0 ]]; then
    # 기본 테스트 실행
    log_info "기본 테스트 실행 중..."
    
    if [[ -f "$PROJECT_ROOT/pk_external_tools/pk_functions/ensure_losslesscut_pk_event_test.py" ]]; then
        cd "$PROJECT_ROOT/pk_external_tools/pk_functions"
        log_info "LosslessCut Event 시스템 테스트 실행"
        $PYTHON_CMD ensure_losslesscut_pk_event_test.py
        log_success "테스트 완료"
    else
        log_warning "기본 테스트 파일을 찾을 수 없음"
    fi
else
    # 지정된 테스트 실행
    TEST_FILE="$1"
    log_info "지정된 테스트 실행: $TEST_FILE"
    
    if [[ -f "$TEST_FILE" ]]; then
        cd "$(dirname "$TEST_FILE")"
        $PYTHON_CMD "$(basename "$TEST_FILE")"
        log_success "테스트 완료"
    else
        log_error "테스트 파일을 찾을 수 없음: $TEST_FILE"
        exit 1
    fi
fi

log_success "모든 작업 완료!"
