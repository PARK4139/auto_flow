#!/bin/bash

set -e
set -u

# SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# source "$SCRIPT_DIR/ensure_pk_os_constants_imported.sh"

# ✅ 필요한 디렉토리 생성
mkdir -p "$(dirname "$F_UV_ZIP")"      # ~/Downloads
mkdir -p "$d_pk_external_tools"

echo "📥 다운로드 중: $PK_URL → $F_UV_ZIP"
curl -L -o "$F_UV_ZIP" "$PK_URL"

# HTML 검사
if file "$F_UV_ZIP" | grep -qi 'html'; then
    echo "❌ 다운로드 실패: HTML 파일이 저장됨. URL 확인 필요!"
    head -n 5 "$F_UV_ZIP"
    exit 1
fi

# zip인지 확인
if file "$F_UV_ZIP" | grep -qi 'zip archive'; then
    echo "📦 zip 파일 감지됨 → 압축해제 (~/Downloads)"
    unzip -o "$F_UV_ZIP" -d "$(dirname "$F_UV_ZIP")"
    mv "$(dirname "$F_UV_ZIP")/uv.exe" "$F_UV"
else
    echo "⚠️ zip 파일이 아님 → 실행파일로 간주하고 설치 중"
    mv "$F_UV_ZIP" "$F_UV"
    chmod +x "$F_UV"
fi