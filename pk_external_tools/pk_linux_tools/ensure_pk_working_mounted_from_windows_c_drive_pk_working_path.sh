#!/bin/bash

# ============================================================================
# pk_working 마운트 문제 해결 스크립트
# 올바른 Windows 사용자 폴더 찾기 및 권한 문제 해결
# ============================================================================

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo "============================================================================"
echo "pk_working 마운트 문제 해결 도구"
echo "============================================================================"

# ============================================================================
# n. 사용 가능한 Windows 사용자 폴더 찾기
# ============================================================================
log_info "사용 가능한 Windows 사용자 폴더를 찾는 중..."

WIN_USERS_PATH="/mnt/c/Users"
VALID_USERS=()
CURRENT_USER=$(whoami)

if [ -d "$WIN_USERS_PATH" ]; then
    echo ""
    echo "발견된 Windows 사용자 폴더들:"
    echo "----------------------------------------"
    
    for user_dir in "$WIN_USERS_PATH"/*; do
        if [ -d "$user_dir" ]; then
            username=$(basename "$user_dir")
            downloads_path="$user_dir/Downloads"
            
            # 접근 권한 및 Downloads 폴더 확인
            if [ -d "$downloads_path" ] && [ -r "$downloads_path" ] && [ -w "$downloads_path" ]; then
                VALID_USERS+=("$username")
                echo "✅ $username (읽기/쓰기 가능)"
            elif [ -d "$downloads_path" ] && [ -r "$downloads_path" ]; then
                echo "📖 $username (읽기만 가능)"
            elif [ -d "$user_dir" ]; then
                echo "❌ $username (접근 불가)"
            fi
        fi
    done
else
    log_error "Windows 사용자 폴더에 접근할 수 없습니다: $WIN_USERS_PATH"
    exit 1
fi

echo "----------------------------------------"

# ============================================================================
# n. 적절한 사용자 선택
# ============================================================================
if [ ${#VALID_USERS[@]} -eq 0 ]; then
    log_error "쓰기 권한이 있는 Windows 사용자 폴더를 찾을 수 없습니다."
    echo ""
    echo "해결 방법 옵션:"
    echo "1. Windows에서 현재 사용자의 Downloads 폴더에 pk_working 폴더를 직접 생성"
    echo "2. 다른 경로 사용 (예: /mnt/d/, /tmp/ 등)"
    echo "3. WSL 내부 경로만 사용"
    echo ""
    
    # 대안 경로 제시
    log_info "대안 해결책을 제시합니다..."
    
    # WSL 내부에 pk_working 생성
    WSL_PK_WORKING="$HOME/pk_working"
    
    read -p "WSL 내부에 pk_working 폴더를 생성하시겠습니까? ($WSL_PK_WORKING) [Y/n]: " CREATE_WSL_ONLY
    
    if [[ ! $CREATE_WSL_ONLY =~ ^[Nn]$ ]]; then
        mkdir -p "$WSL_PK_WORKING"
        
        # bashrc 업데이트
        BASHRC_FILE="$HOME/.bashrc"
        sed -i '/export PK_WORKING/d' "$BASHRC_FILE" 2>/dev/null || true
        sed -i "/alias cdpk/d" "$BASHRC_FILE" 2>/dev/null || true
        
        echo "" >> "$BASHRC_FILE"
        echo "# pk_working WSL 내부 경로 설정" >> "$BASHRC_FILE"
        echo "export PK_WORKING=\"$WSL_PK_WORKING\"" >> "$BASHRC_FILE"
        echo "alias cdpk='cd \$PK_WORKING'" >> "$BASHRC_FILE"
        
        log_success "WSL 내부 pk_working 폴더 생성: $WSL_PK_WORKING"
        log_success "환경변수 및 별칭 설정 완료"
        
        # 즉시 적용
        export PK_WORKING="$WSL_PK_WORKING"
        alias cdpk="cd $PK_WORKING"
        
        echo ""
        echo "========================================="
        echo "설정 완료!"
        echo "========================================="
        echo "경로: $WSL_PK_WORKING"
        echo "사용법: cdpk 또는 cd \$PK_WORKING"
        echo "설정 적용: source ~/.bashrc"
        echo "========================================="
        
        exit 0
    fi
    
    exit 1
    
elif [ ${#VALID_USERS[@]} -eq 1 ]; then
    SELECTED_USER="${VALID_USERS[0]}"
    log_success "자동 선택된 사용자: $SELECTED_USER"
else
    echo ""
    log_info "여러 사용 가능한 사용자가 발견되었습니다. 선택해주세요:"
    echo ""
    
    for i in "${!VALID_USERS[@]}"; do
        echo "$((i+1)). ${VALID_USERS[$i]}"
    done
    echo ""
    
    while true; do
        read -p "사용자 번호를 선택하세요 (1-${#VALID_USERS[@]}): " USER_CHOICE
        
        if [[ $USER_CHOICE =~ ^[0-9]+$ ]] && [ $USER_CHOICE -ge 1 ] && [ $USER_CHOICE -le ${#VALID_USERS[@]} ]; then
            SELECTED_USER="${VALID_USERS[$((USER_CHOICE-1))]}"
            break
        else
            log_warning "올바른 번호를 입력해주세요."
        fi
    done
fi

log_info "선택된 Windows 사용자: $SELECTED_USER"

# ============================================================================
# n. 경로 설정 및 폴더 생성
# ============================================================================
WIN_PK_WORKING="/mnt/c/Users/$SELECTED_USER/Downloads/pk_working"
LINUX_PK_WORKING="$HOME/Downloads/pk_working"

log_info "Windows 경로: $WIN_PK_WORKING"
log_info "Linux 마운트 경로: $LINUX_PK_WORKING"

# Windows 폴더 생성
log_info "Windows pk_working 폴더 생성 중..."
if [ ! -d "$WIN_PK_WORKING" ]; then
    if mkdir -p "$WIN_PK_WORKING" 2>/dev/null; then
        log_success "Windows pk_working 폴더 생성 완료"
    else
        log_error "폴더 생성 실패. Windows에서 직접 생성해주세요: C:\\Users\\$SELECTED_USER\\Downloads\\pk_working"
        
        read -p "Windows에서 폴더를 생성한 후 Enter를 눌러주세요..." WAIT_INPUT
        
        if [ ! -d "$WIN_PK_WORKING" ]; then
            log_error "여전히 폴더를 찾을 수 없습니다. 스크립트를 종료합니다."
            exit 1
        fi
    fi
else
    log_success "Windows pk_working 폴더가 이미 존재합니다"
fi

# ============================================================================
# n. Linux 심볼릭 링크 설정
# ============================================================================
log_info "Linux 심볼릭 링크 설정 중..."

# Downloads 디렉토리 생성
mkdir -p "$HOME/Downloads"

# 기존 링크/폴더 처리
if [ -L "$LINUX_PK_WORKING" ]; then
    log_warning "기존 심볼릭 링크를 제거합니다"
    rm "$LINUX_PK_WORKING"
elif [ -d "$LINUX_PK_WORKING" ]; then
    BACKUP_NAME="${LINUX_PK_WORKING}_backup_$(date +%Y%m%d_%H%M%S)"
    log_warning "기존 폴더를 백업합니다: $BACKUP_NAME"
    mv "$LINUX_PK_WORKING" "$BACKUP_NAME"
fi

# 심볼릭 링크 생성
if ln -s "$WIN_PK_WORKING" "$LINUX_PK_WORKING"; then
    log_success "심볼릭 링크 생성 완료"
else
    log_error "심볼릭 링크 생성 실패"
    exit 1
fi

# ============================================================================
# n. 환경변수 및 별칭 설정
# ============================================================================
log_info "환경변수 및 별칭 설정 중..."

BASHRC_FILE="$HOME/.bashrc"

# 기존 설정 제거
sed -i '/export PK_WORKING/d' "$BASHRC_FILE" 2>/dev/null || true
sed -i "/alias cdpk/d" "$BASHRC_FILE" 2>/dev/null || true

# 새 설정 추가
echo "" >> "$BASHRC_FILE"
echo "# pk_working 자동 마운트 설정 ($(date))" >> "$BASHRC_FILE"
echo "export PK_WORKING=\"$LINUX_PK_WORKING\"" >> "$BASHRC_FILE"
echo "alias cdpk='cd \$PK_WORKING'" >> "$BASHRC_FILE"

# 즉시 적용
export PK_WORKING="$LINUX_PK_WORKING"
alias cdpk="cd $PK_WORKING"

log_success "환경변수 및 별칭 설정 완료"

# ============================================================================
# 6. 테스트 및 확인
# ============================================================================
log_info "설정 테스트 중..."

# 권한 테스트
TEST_FILE="$WIN_PK_WORKING/test_$(date +%s).txt"
if echo "test" > "$TEST_FILE" 2>/dev/null; then
    rm "$TEST_FILE"
    log_success "읽기/쓰기 권한 테스트 통과"
else
    log_warning "쓰기 권한 테스트 실패 (읽기 전용일 수 있음)"
fi

# 심볼릭 링크 테스트
if [ -L "$LINUX_PK_WORKING" ] && [ -d "$LINUX_PK_WORKING" ]; then
    log_success "심볼릭 링크 정상 작동 확인"
else
    log_error "심볼릭 링크 작동 실패"
fi

# ============================================================================
# 7. 완료 안내
# ============================================================================
echo ""
echo "============================================================================"
echo "🎉 pk_working 마운트 설정 완료!"
echo "============================================================================"
echo "Windows 경로: $WIN_PK_WORKING"
echo "Linux 경로:   $LINUX_PK_WORKING"
echo "환경변수:     \$PK_WORKING"
echo "별칭:         cdpk"
echo ""
echo "사용법:"
echo "  cdpk                    # pk_working 폴더로 이동"
echo "  cd \$PK_WORKING         # 환경변수 사용"
echo "  ls ~/Downloads/pk_working # 직접 경로 사용"
echo ""
echo "설정 적용:"
echo "  source ~/.bashrc        # 현재 터미널에 즉시 적용"
echo "  또는 새 터미널 창 열기"
echo "============================================================================"

# 현재 터미널에서 즉시 사용 가능하도록 설정
cd "$LINUX_PK_WORKING" 2>/dev/null && pwd && log_success "현재 pk_working 폴더로 이동했습니다!"

# 추가 도움말
echo ""
log_info "문제 해결 팁:"
echo "• Windows에서 파일을 생성하면 WSL에서도 즉시 보입니다"
echo "• WSL에서 생성한 파일은 Windows 탐색기에서도 보입니다"
echo "• 권한 문제가 있다면 Windows에서 폴더 속성을 확인해보세요"
echo ""