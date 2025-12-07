#!/bin/bash
# pk_system Aliases
# This file contains useful aliases for the pk_system

# pk_system root directory
export PK_ROOT="$(dirname "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")")"

# Python virtual environment aliases (Linux/WSL용)
if [ -f "$PK_ROOT/.venv/bin/python" ]; then
    alias pk-python="$PK_ROOT/.venv/bin/python"
    alias pk-pip="$PK_ROOT/.venv/bin/pip"
fi

# pk_system navigation aliases
alias pk-cd="cd $PK_ROOT"
alias pk-py="cd $PK_ROOT/pk_external_tools"
alias pk-sh="cd $PK_ROOT/pk_os_layer_resources"

# pk_system utility functions
pk_enable() {
    echo "🔧 pk_system 활성화 중..."
    cd "$PK_ROOT"
    ./pk_os_layer_resources/ensure_pk_enabled.sh
}

pk_sync() {
    echo "🔄 pk_system 동기화 중..."
    cd "$PK_ROOT"
    uv sync
}

pk_test() {
    echo "🧪 pk_system 테스트 중..."
    cd "$PK_ROOT"
    if [ -f "tests/run_tests.py" ]; then
        pk-python tests/run_tests.py
    else
        echo "❌ 테스트 파일을 찾을 수 없습니다."
    fi
}

# Display pk_system info
pk_interesting_info() {
    echo "🐍 pk_system Information"
    echo "========================"
    echo "📁 Root: $PK_ROOT"
    echo "🐍 Python: $(which python3)"
    if [ -f "$PK_ROOT/.venv/bin/python" ]; then
        echo "🔗 Virtual Env: $PK_ROOT/.venv/bin/python"
    fi
    echo "📦 uv: $(which uv 2>/dev/null || echo 'Not installed')"
    echo "========================"
}

# Create aliases for the functions
alias pk-enable="pk_enable"
alias pk-sync="pk_sync"
alias pk-test="pk_test"
alias pk-info="pk_interesting_info"

echo "✅ pk_system aliases loaded"