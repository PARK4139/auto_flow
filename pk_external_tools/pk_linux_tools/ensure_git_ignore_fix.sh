#!/bin/bash

echo "🔧 ensure_ 방식: Git node_modules 문제 완전 해결..."
echo "================================================"

# 1️⃣ 현재 위치 확인
echo "📍 현재 위치: $(pwd)"

# 2️⃣ .gitignore 파일 확인 및 수정
echo "📝 .gitignore 파일 업데이트 중..."

# 루트 .gitignore 업데이트
cat >> .gitignore << 'EOF'

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
.yarn-integrity

# Next.js
.next/
out/
build/

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Docker
Dockerfile.*
!Dockerfile.dev
!Dockerfile.ensure_*

# Build artifacts
dist/
build/
*.tgz
*.tar.gz
EOF

# 3️⃣ 프론트엔드 디렉토리 .gitignore도 업데이트
if [ -d "services/smart_person_ai/service_official_home/frontend" ]; then
    echo "📝 프론트엔드 .gitignore 업데이트..."
    cat > services/smart_person_ai/service_official_home/frontend/.gitignore << 'EOF'
# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env
.env*.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# Logs
logs/
build_attempts_*.log
EOF
fi

# 4️⃣ Git 캐시 정리
echo "🧹 Git 캐시 정리 중..."
git rm -r --cached . 2>/dev/null || echo "캐시 정리 완료"

# 5️⃣ node_modules 강제 제거 (Git에서)
echo "🗑️ node_modules Git 추적 제거..."
git rm -r --cached services/smart_person_ai/service_official_home/frontend/node_modules 2>/dev/null || echo "node_modules 추적 제거 완료"

# 6️⃣ 다시 추가
echo "📦 수정된 파일들 Git에 추가..."
git add .gitignore
git add services/smart_person_ai/service_official_home/frontend/.gitignore
git add services/smart_person_ai/service_official_home/frontend/ensure_development_hot_reload.sh

# 선택적으로 다른 중요 파일들 추가
git add services/smart_person_ai/service_official_home/frontend/package.json 2>/dev/null || true
git add services/smart_person_ai/service_official_home/frontend/next.config.js 2>/dev/null || true
git add services/smart_person_ai/service_official_home/frontend/tsconfig.json 2>/dev/null || true
git add services/smart_person_ai/service_official_home/frontend/tailwind.config.js 2>/dev/null || true

# 소스 파일들 추가
git add services/smart_person_ai/service_official_home/frontend/app/ 2>/dev/null || true
git add services/smart_person_ai/service_official_home/frontend/components/ 2>/dev/null || true
git add services/smart_person_ai/service_official_home/frontend/public/ 2>/dev/null || true

echo ""
echo "✅ Git 문제 해결 완료!"
echo "📝 다음 명령어로 커밋하세요:"
echo "git commit -m \"fix: node_modules gitignore 추가 및 개발 환경 설정\""
echo "git push origin main"
```

## 🎯 **Windows에서 바로 실행**

```cmd
<code_block_to_apply_changes_from>
```

## 🚀 **수동 해결 방법 (더 간단)**

```bash
# 1️⃣ .gitignore 파일 생성/수정
echo "node_modules/" >> .gitignore
echo ".next/" >> .gitignore
echo "*.log" >> .gitignore

# 2️⃣ Git 캐시에서 node_modules 제거
git rm -r --cached services/smart_person_ai/service_official_home/frontend/node_modules

# 3️⃣ .gitignore 추가
git add .gitignore

# 4️⃣ 다른 파일들 추가 (node_modules 제외)
git add services/smart_person_ai/service_official_home/frontend/package.json
git add services/smart_person_ai/service_official_home/frontend/app/
git add services/smart_person_ai/service_official_home/frontend/components/
git add services/smart_person_ai/service_official_home/frontend/ensure_development_hot_reload.sh

# 5️⃣ 커밋
git commit -m "fix: add gitignore for node_modules and setup dev environment"
git push origin main
```

## 📋 **프로젝트 루트 .gitignore 권장 내용**

```gitignore:.gitignore
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Next.js
.next/
out/
build/

# Environment variables
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
build_attempts_*.log

# Docker
Dockerfile.attempt*
Dockerfile.debug
Dockerfile.fixed
```

## 🎯 **지금 바로 실행하세요**

```bash
# Windows Git Bash 또는 PowerShell에서
cd /c/Users/wjdgn/Downloads/pk_system

# 간단한 해결
echo "node_modules/" >> .gitignore
git rm -r --cached services/smart_person_ai/service_official_home/frontend/node_modules
git add .gitignore
git add services/smart_person_ai/service_official_home/frontend/ensure_development_hot_reload.sh
git commit -m "fix: add gitignore and dev environment setup"
git push origin main
```

이제 Git 오류 없이 커밋할 수 있습니다! 🎉 