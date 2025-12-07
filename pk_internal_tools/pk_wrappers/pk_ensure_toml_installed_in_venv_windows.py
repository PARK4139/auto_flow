#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# virtual environment Python으로 재실행 (필요한 경우)
from pk_internal_tools.pk_functions.ensure_venv_python_path import ensure_venv_python_executed
ensure_venv_python_executed(project_root)

from pk_internal_tools.pk_functions.ensure_toml_installed_in_venv_windows import ensure_toml_installed_in_venv_windows

if __name__ == "__main__":
    print("=== .venv virtual environment toml 모듈 자동 설치 래퍼")
    print(f"현재 실행 중인 Python: {sys.executable}")
    
    # 강제 재설치 옵션 확인
    force_reinstall = "--force" in sys.argv or "-f" in sys.argv
    
    # 실행
    success = ensure_toml_installed_in_venv_windows(force_reinstall=force_reinstall)
    
    if success:
        print("✅ toml 모듈 설치/확인이 완료되었습니다!")
        sys.exit(0)
    else:
        print("❌ toml 모듈 설치에 실패했습니다.")
        sys.exit(1)
