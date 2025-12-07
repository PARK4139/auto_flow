def ensure_everything_fast_search():
    """Everything 빠른 검색 최적화"""
    import os
    import subprocess
    import logging
    
    def check_everything_available():
        """Everything이 설치되어 있는지 확인"""
        everything_paths = [
            r"C:\Program Files\Everything\Everything.exe",
            r"C:\Program Files (x86)\Everything\Everything.exe"
        ]
        for path in everything_paths:
            if os.path.exists(path):
                return path
        return None
    
    def optimize_everything_for_speed():
        """Everything을 빠른 검색을 위해 최적화"""
        try:
            everything_ini = os.path.expanduser(r"~\AppData\Roaming\Everything\Everything.ini")
            if not os.path.exists(everything_ini):
                return False
            
            # 설정 파일 읽기
            with open(everything_ini, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 빠른 검색을 위한 설정 추가
            speed_settings = [
                "fast_sort=1",
                "fast_size_sort=1",
                "fast_date_sort=1",
                "fast_attributes_sort=1",
                "fast_recent_sort=1",
                "fast_run_count_sort=1",
                "fast_date_created_sort=1",
                "fast_date_modified_sort=1",
                "fast_date_accessed_sort=1",
                "fast_path_sort=1",
                "fast_name_sort=1",
                "fast_ext_sort=1",
                "fast_size_format_sort=1",
                "fast_attributes_format_sort=1",
                "fast_date_format_sort=1",
                "fast_recent_format_sort=1",
                "fast_run_count_format_sort=1",
                "fast_date_created_format_sort=1",
                "fast_date_modified_format_sort=1",
                "fast_date_accessed_format_sort=1",
                "fast_path_format_sort=1",
                "fast_name_format_sort=1",
                "fast_ext_format_sort=1"
            ]
            
            modified = False
            for setting in speed_settings:
                if setting not in content:
                    content += f"\n{setting}"
                    modified = True
            
            # 설정 파일 업데이트
            if modified:
                with open(everything_ini, 'w', encoding='utf-8') as f:
                    f.write(content)
                logging.debug("Everything 빠른 검색 설정이 적용되었습니다.")
                return True
            else:
                logging.debug("Everything 빠른 검색 설정이 이미 적용되어 있습니다.")
                return True
                
        except Exception as e:
            logging.debug(f"Everything 빠른 검색 설정 실패: {e}")
            return False
    
    # Everything 설치 확인
    everything_exe = check_everything_available()
    if not everything_exe:
        logging.debug("Everything이 설치되어 있지 않습니다.")
        return False
    
    # Everything 빠른 검색 최적화
    if optimize_everything_for_speed():
        logging.debug("Everything 빠른 검색 최적화가 완료되었습니다.")
        return True
    else:
        logging.debug("Everything 빠른 검색 최적화가 실패했습니다.")
        return False 