#!/bin/bash
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}[1/7] zsh 설치 확인...${NC}"
if ! command -v zsh &> /dev/null; then
    echo -e "${YELLOW}zsh를 설치합니다...${NC}"
    sudo apt update && sudo apt install -y zsh
else
    echo -e "${GREEN}zsh가 이미 설치되어 있습니다.${NC}"
fi

echo -e "${CYAN}[2/7] oh-my-zsh 설치 확인...${NC}"
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo -e "${YELLOW}oh-my-zsh를 설치합니다...${NC}"
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
else
    echo -e "${GREEN}oh-my-zsh가 이미 설치되어 있습니다.${NC}"
fi

echo -e "${CYAN}[3/7] zsh-autosuggestions 플러그인 설치 확인...${NC}"
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" ]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions \
        ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    echo -e "${GREEN}zsh-autosuggestions 설치 완료.${NC}"
else
    echo -e "${GREEN}zsh-autosuggestions 이미 설치됨.${NC}"
fi

echo -e "${CYAN}[4/7] zsh-syntax-highlighting 플러그인 설치 확인...${NC}"
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting" ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
        ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    echo -e "${GREEN}zsh-syntax-highlighting 설치 완료.${NC}"
else
    echo -e "${GREEN}zsh-syntax-highlighting 이미 설치됨.${NC}"
fi

# echo -e "${CYAN}[5/7] fzf 설치 확인...${NC}"
# if ! command -v fzf &> /dev/null; then
#     echo -e "${YELLOW}fzf를 설치합니다...${NC}"
#     sudo apt install -y fzf
# else
#     echo -e "${GREEN}fzf가 이미 설치되어 있습니다.${NC}"
# fi

echo -e "${CYAN}[6/7] .zshrc 플러그인 항목 자동 추가...${NC}"
# 원하는 플러그인 목록
PLUGIN_LIST="git
zsh-autosuggestions
yarn
web-search
jsontools
macports
node
osx
sudo
thor
docker
zsh-syntax-highlighting
mouse
iterm2"

# plugins 블록 삭제 (시작~끝까지)
sed -i '/^plugins=(/,/^)/d' ~/.zshrc

# plugins 블록 맨 아래쪽에 추가 (혹은 원하는 위치에 삽입)
{
echo "plugins=("
for p in $PLUGIN_LIST; do
    echo "  $p"
done
echo ")"
} >> ~/.zshrc

echo 'export ZSH="$HOME/.oh-my-zsh" '>> ~/.zshrc
echo 'ZSH_THEME="powerlevel10k/powerlevel10k"  # 없으면 원하는 테마로  '>> ~/.zshrc
echo 'source $ZSH/oh-my-zsh.sh   '>> ~/.zshrc



echo -e "${CYAN}[7/7] zshrc 테마 추천(powerlevel10k) 설치 여부 확인...${NC}"
if [ ! -d "${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k" ]; then
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
        ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
    sed -i 's/^ZSH_THEME=.*/ZSH_THEME="powerlevel10k\/powerlevel10k"/' ~/.zshrc
    echo -e "${GREEN}powerlevel10k 테마가 설치되었습니다.${NC}"
else
    echo -e "${GREEN}powerlevel10k 테마가 이미 설치되어 있습니다.${NC}"
fi

echo -e "${GREEN}★ 모든 설정이 완료되었습니다. zsh를 재시작 하세요!${NC}"



# 필요시 기본쉘 변경 물어보기
if [ "$SHELL" != "/usr/bin/zsh" ]; then
    read -p "zsh를 기본쉘로 변경할까요? [y/N]: " yn
    if [[ "$yn" =~ ^[Yy]$ ]]; then
        chsh -s $(which zsh)
        echo -e "${GREEN}기본쉘이 zsh로 변경되었습니다.${NC}"
    else
        echo -e "${YELLOW}기본쉘 변경은 건너뜁니다.${NC}"
    fi
fi
