#!/bin/bash
set -e

echo "📦 uv 설치 중..."

# Check if uv is already installed
if command -v uv &> /dev/null; then
    echo "✅ uv가 이미 설치되어 있습니다: $(uv --version)"
    exit 0
fi

# Update system packages
echo "🔄 시스템 패키지 업데이트 중..."
sudo apt update -y

# Install required dependencies
echo "📦 필수 종속성 설치 중..."
sudo apt install -y curl

# Install uv using official installer
echo "🚀 uv 공식 설치 프로그램 실행 중..."
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH for current session (check both possible locations)
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

# Verify installation
if command -v uv &> /dev/null; then
    echo "✅ uv 설치 완료: $(uv --version)"
else
    echo "❌ uv 설치 실패"
    echo "💡 수동 설치를 시도하세요:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "   source ~/.bashrc"
    exit 1
fi