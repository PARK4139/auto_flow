#!/usr/bin/env python3
"""
테스트 DB들을 D_PK_LOGS 디렉토리 내부에서 생성하도록 관리하는 유틸리티
"""

import sys
from pathlib import Path

from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE

# Import D_PK_LOGS
sys.path.append(str(Path(__file__).parent.parent))
from pk_internal_tools.pk_objects.pk_directories import D_PK_LOGS


def get_test_db_path(db_name: str) -> Path:
    """
    테스트 DB 경로를 D_PK_LOGS 내부에서 반환합니다.
    
    Args:
        db_name: 테스트 DB 이름 (예: 'tomorrow_war', 'volumes_db')
    
    Returns:
        Path: D_PK_LOGS 내부의 테스트 DB 경로
    """
    # D_PK_LOGS 디렉토리가 None인 경우 기본값 설정
    logs_dir = D_PK_LOGS

    # D_PK_LOGS 디렉토리 생성
    logs_dir.mkdir(parents=True, exist_ok=True)

    # 테스트 DB 경로 반환
    test_db_path = logs_dir / f"test_db_{db_name}"
    return test_db_path


def migrate_existing_test_dbs():
    """
    기존의 테스트 DB들을 D_PK_LOGS로 이동합니다.
    """
    import shutil
    import logging

    # 현재 디렉토리에서 찾을 테스트 DB들
    current_dir = Path.cwd()
    test_dbs_to_migrate = [
        "pk_cache"
    ]

    migrated_count = 0

    for db_name in test_dbs_to_migrate:
        old_path = current_dir / db_name

        if old_path.exists():
            # 새 경로 생성
            if db_name.startswith("test_db_"):
                new_name = db_name[8:]  # "test_db_" 제거
            elif db_name.startswith("test_"):
                new_name = db_name[5:]  # "test_" 제거
            else:
                new_name = db_name

            new_path = get_test_db_path(new_name)

            try:
                if new_path.exists():
                    print(f"⚠️  대상 경로가 이미 존재합니다: {new_path}")
                    print(f"   기존 경로 유지: {old_path}")
                else:
                    # 디렉토리 이동
                    shutil.move(str(old_path), str(new_path))
                    print(f"✅ 이동 완료: {old_path} → {new_path}")
                    migrated_count += 1

            except Exception as e:
                print(f"❌ 이동 실패: {old_path} → {new_path}")
                print(f"   오류: {e}")
                logging.error(f"Failed to migrate {old_path}: {e}")

    if migrated_count > 0:
        print(f"\n🎯 총 {migrated_count}개의 테스트 DB가 D_PK_LOGS로 이동되었습니다.")
        print(f"📁 D_PK_LOGS 경로: {D_PK_LOGS}")
    else:
        print("📋 이동할 테스트 DB가 없습니다.")


def create_test_db_example():
    """
    테스트 DB 생성 예제를 보여줍니다.
    """
    print("📝 테스트 DB 생성 예제:")
    print(PK_UNDERLINE)

    examples = [
        ("tomorrow_war", "투모로우 워 영화 검색 테스트"),
        ("volumes_db", "볼륨 레지스트리 테스트"),
        ("file_search", "파일 검색 성능 테스트"),
        ("integration", "통합 테스트")
    ]

    for db_name, description in examples:
        test_path = get_test_db_path(db_name)
        print(f"• {description}")
        print(f"  경로: {test_path}")
        print(f"  사용법: ensure_target_file_found_renewal.py scan --db-root {test_path}")
        print()


def cleanup_old_test_files():
    """
    프로젝트 루트의 오래된 테스트 파일들을 정리합니다.
    """
    import re

    current_dir = Path.cwd()

    # 테스트 리포트 파일 패턴
    test_report_patterns = [
        r"test_report_.*\.txt$",
        r"detailed_test_report_.*\.txt$",
        r".*_test_.*\.txt$"
    ]

    moved_files = []

    for file_path in current_dir.glob("*.txt"):
        for pattern in test_report_patterns:
            if re.match(pattern, file_path.name):
                # D_PK_LOGS로 이동
                new_path = D_PK_LOGS / file_path.name

                try:
                    if not new_path.exists():
                        file_path.rename(new_path)
                        moved_files.append((file_path.name, new_path))
                        print(f"📄 이동: {file_path.name} → {new_path}")
                except Exception as e:
                    print(f"❌ 파일 이동 실패: {file_path.name} - {e}")
                break

    if moved_files:
        print(f"\n✅ {len(moved_files)}개의 테스트 리포트 파일이 D_PK_LOGS로 이동되었습니다.")
    else:
        print("📋 이동할 테스트 리포트 파일이 없습니다.")


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(description="테스트 DB 관리 유틸리티")
    parser.add_argument("--migrate", action="store_true", help="기존 테스트 DB들을 D_PK_LOGS로 이동")
    parser.add_argument("--cleanup", action="store_true", help="오래된 테스트 파일들을 D_PK_LOGS로 이동")
    parser.add_argument("--example", action="store_true", help="테스트 DB 생성 예제 보기")
    parser.add_argument("--get-path", type=str, help="특정 테스트 DB 경로 가져오기")

    args = parser.parse_args()

    print("🔧 테스트 DB 관리 유틸리티")
    print(PK_UNDERLINE)
    print(f"📁 D_PK_LOGS 경로: {D_PK_LOGS}")
    print()

    if args.migrate:
        migrate_existing_test_dbs()

    if args.cleanup:
        cleanup_old_test_files()

    if args.example:
        create_test_db_example()

    if args.get_path:
        test_path = get_test_db_path(args.get_path)
        print(f"📍 테스트 DB 경로: {test_path}")

    if not any([args.migrate, args.cleanup, args.example, args.get_path]):
        parser.print_help()


if __name__ == "__main__":
    main()
