if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_objects.pk_directories import D_DESKTOP
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories  import d_pk_root

    from datetime import datetime
    from datetime import datetime
    import os  
    import shutil  
    try:
        def copy_changed_files(src_dir, dest_dir, since_time):
            # Unix timestamp로 변환
            since_timestamp = since_time.timestamp()

            # 원본 디렉터리 순회
            for root, dirs, files in os.walk(src_dir):
                # 상대 경로 계산
                relative_path = os.path.relpath(root, src_dir)
                target_root = os.path.join(dest_dir, relative_path)

                # 대상 디렉터리 생성
                os.makedirs(target_root, exist_ok=True)

                for file_name in files:
                    src_file = os.path.join(root, file_name)
                    dest_file = os.path.join(target_root, file_name)

                    # 파일 수정 시간 확인
                    if os.path.getmtime(src_file) >= since_timestamp:
                        # 파일 복사
                        shutil.copy2(src_file, dest_file)
                        print(f"Copied: {src_file} -> {dest_file}")


        # 원본 및 대상 디렉터리 설정
        source_directory = rf"{d_pk_root}"
        destination_directory = rf"{D_DESKTOP}"
        since = datetime(2025, 1, 1, 15, 30)  # 기준 시점 설정 (예: 2025년 1월 1일 15:30)
        copy_changed_files(src_dir=source_directory, dest_dir=destination_directory, since_time=since)
    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
