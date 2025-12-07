#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pk_system 버전 업데이트 스크립트

사용법:
    python scripts/update_version.py [YYYY.M.D]
    
예시:
    python scripts/update_version.py 2025.11.21
    python scripts/update_version.py  # 오늘 날짜로 자동 생성
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


def get_current_date_version() -> str:
    """오늘 날짜를 버전 형식으로 반환"""
    today = datetime.now()
    return f"{today.year}.{today.month}.{today.day}"


def create_version_tag(version: str, message: str = None) -> bool:
    """Git 태그 생성"""
    tag_name = f"v{version}"
    
    # 이미 태그가 있는지 확인
    result = subprocess.run(
        ["git", "tag", "-l", tag_name],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent
    )
    
    if result.stdout.strip():
        print(f"[WARNING] 태그 {tag_name}가 이미 존재합니다.")
        response = input(f"기존 태그를 삭제하고 새로 생성하시겠습니까? (y/N): ")
        if response.lower() == 'y':
            subprocess.run(
                ["git", "tag", "-d", tag_name],
                cwd=Path(__file__).parent.parent
            )
        else:
            print("[CANCELLED] 태그 생성이 취소되었습니다.")
            return False
    
    # 태그 메시지 생성
    if not message:
        message = f"Version {version}: Auto-generated tag"
    
    # 태그 생성
    try:
        subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", message],
            check=True,
            cwd=Path(__file__).parent.parent
        )
        print(f"[SUCCESS] 태그 {tag_name}가 생성되었습니다.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] 태그 생성 실패: {e}")
        return False


def get_version_from_git() -> str:
    """Git에서 현재 버전 가져오기"""
    try:
        result = subprocess.run(
            ["git", "describe", "--tags", "--dirty"],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "unknown"
    except Exception as e:
        print(f"[WARNING] Git 버전 확인 실패: {e}")
        return "unknown"


def main():
    """메인 함수"""
    # 버전 인자 확인
    if len(sys.argv) > 1:
        version = sys.argv[1]
        # 형식 검증
        try:
            parts = version.split('.')
            if len(parts) != 3:
                raise ValueError("버전 형식이 올바르지 않습니다. YYYY.M.D 형식을 사용하세요.")
            year, month, day = map(int, parts)
            if not (1 <= month <= 12 and 1 <= day <= 31):
                raise ValueError("월은 1-12, 일은 1-31 사이여야 합니다.")
        except ValueError as e:
            print(f"[ERROR] {e}")
            return 1
    else:
        version = get_current_date_version()
        print(f"[INFO] 버전이 지정되지 않아 오늘 날짜를 사용합니다: {version}")
    
    # 커밋 메시지 입력 (선택사항)
    print(f"\n버전 {version} 태그를 생성합니다.")
    custom_message = input("태그 메시지를 입력하세요 (Enter로 기본 메시지 사용): ").strip()
    
    # 태그 생성
    if create_version_tag(version, custom_message if custom_message else None):
        # 현재 버전 확인
        current_version = get_version_from_git()
        print(f"\n[INFO] 현재 Git 버전: {current_version}")
        print(f"\n[SUCCESS] 버전 업데이트 완료!")
        print(f"\n다음 단계:")
        print(f"  1. 태그를 원격 저장소에 푸시: git push origin v{version}")
        print(f"  2. 버전 확인: python -c \"import setuptools_scm; print(setuptools_scm.get_version())\"")
        return 0
    else:
        return 1


if __name__ == '__main__':
    exit(main())

