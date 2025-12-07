# #!/bin/bash

# # Helix 설치
# echo "Helix 설치 중..."
# sudo apt update -y
# sudo apt install -y helix

# # Helix 설정 디렉토리 생성
# echo "Helix 설정 파일 구성..."
# CONFIG_DIR="$HOME/.config/helix"
# mkdir -p "$CONFIG_DIR"

# # 기본 설정 파일 생성
# cat > "$CONFIG_DIR/config.toml" << EOF
# [editor]
# theme = "onedark"        # 테마 설정 (onedark)
# auto_indent = true       # 자동 들여쓰기
# tab_width = 4            # 탭 너비 설정

# [keys.normal]
# "h" = "move_left"
# "j" = "move_down"
# "k" = "move_up"
# "l" = "move_right"
# "w" = "move_word_forward"
# EOF

# # 완료 메시지
# echo "Helix 설치 및 설정 완료."
# echo "Helix 실행: hx [파일명]"



#!/bin/bash

# Helix 설치 스크립트 (WSL Ubuntu 18.04)
echo "Helix 설치 스크립트 시작..."

# 시스템 패키지 업데이트
echo "시스템 패키지 업데이트 중..."
sudo apt update

# 의존성 설치
echo "필요한 의존성 설치 중..."
sudo apt install -y curl tar xz-utils libgcc1 libstdc++6 libssl1.1

# Helix 다운로드 및 설치
echo "Helix 다운로드 중..."
curl -LO https://github.com/helix-editor/helix/releases/latest/download/helix-x86_64-linux.tar.xz
echo "Helix 압축해제 중..."
tar -xf helix-x86_64-linux.tar.xz
# sudo snap install helix --classic

# 실행 파일 이동
echo "Helix 설치 중..."
sudo mv helix /usr/local/bin/hx

# 환경 변수 설정
echo 'export PATH="$PATH:/usr/local/bin"' >> ~/.bashrc
source ~/.bashrc

# 설정 파일 생성
echo "Helix 설정 파일 구성..."
mkdir -p ~/.config/helix
cat > ~/.config/helix/config.toml << EOF
[editor]
theme = "onedark"          # 테마 설정 (onedark)
tab-width = 4              # 탭 너비 설정
indent-guides = "enabled"  # 들여쓰기 튜토리얼 활성화

[keys.normal]
"h" = "cursor_left"
"j" = "cursor_down"
"k" = "cursor_up"
"l" = "cursor_right"
"w" = "move_word_right"
"b" = "move_word_left"
"u" = "undo"
"r" = "redo"
EOF

# 설치 완료
echo "Helix 설치 완료!"
echo "Helix 실행: hx [파일명]"
