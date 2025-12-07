#!/bin/bash

set -e

# 색상 변수
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
CYAN='\033[1;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# 단계별 출력 함수
print_step() {
    echo -e "${BLUE}${BOLD}[Step $1]${NC} ${CYAN}$2${NC}"
}

print_info() {
    echo -e "${YELLOW}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_warning() {
    echo -e "${RED}$1${NC}"
}

print_step 1 "zsh 설치 확인 및 설치..."
if ! command -v zsh >/dev/null 2>&1; then
    print_info "zsh가 설치되어 있지 않습니다. 설치를 진행합니다."
    sudo apt update
    sudo apt install -y zsh
else
    print_success "zsh가 이미 설치되어 있습니다."
fi

print_step 2 "~/.zshrc 파일 존재 확인..."
if [ ! -f "$HOME/.zshrc" ]; then
    echo "# 기본 zshrc 생성 (자동 생성됨)" > "$HOME/.zshrc"
    echo "export PATH=\"\$PATH:\$HOME/.local/bin\"" >> "$HOME/.zshrc"
    echo "alias ll='ls -alF'" >> "$HOME/.zshrc"
    echo "alias la='ls -A'" >> "$HOME/.zshrc"
    echo "alias l='ls -CF'" >> "$HOME/.zshrc"
    echo "PS1='%n@%m %1~ %# '" >> "$HOME/.zshrc"
    print_success "~/.zshrc 파일이 생성되었습니다."
else
    print_info "~/.zshrc 파일이 이미 존재합니다. 변경하지 않습니다."
fi

print_step 3 "기본 쉘을 zsh로 변경할까요? [y/N]"
read -r answer
if [[ "$answer" =~ ^[Yy]$ ]]; then
    chsh -s "$(command -v zsh)"
    print_success "기본 쉘이 zsh로 변경되었습니다. (재로그인 필요)"
else
    print_warning "기본 쉘 변경을 건너뜁니다."
fi

echo -e "${GREEN}${BOLD}설치 및 설정이 완료되었습니다.${NC}"
