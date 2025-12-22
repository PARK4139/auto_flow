def ensure_everything_db_optimized():
    """Everything DB 캐싱 최적화 확인 및 설정"""
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
    
    def check_windows_search_service():
        """Windows Search 서비스 상태 확인"""
        try:
            result = subprocess.run(
                ['sc', 'query', 'WSearch'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and "RUNNING" in result.stdout:
                return True
            return False
        except Exception as e:
            return False
    
    def check_everything_database():
        """Everything 데이터베이스 상태 확인"""
        try:
            # Everything 설정 파일 경로
            everything_ini = os.path.expanduser(r"~\AppData\Roaming\Everything\Everything.ini")
            if os.path.exists(everything_ini):
                with open(everything_ini, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 설정이 있으면 True 반환
                    if "index_folders=1" in content and "index_files=1" in content:
                        return True
                    # 설정이 없으면 자동으로 추가
                    else:
                        logging.debug("Everything 설정을 자동으로 최적화합니다...")
                        from pk_internal_tools.pk_functions.ensure_everything_exe_database_reindex import ensure_everything_exe_database_reindex
                        if ensure_everything_exe_database_reindex():
                            return True
            return False
        except Exception as e:
            logging.debug(f"Everything 데이터베이스 확인 중 오류: {e}")
            return False
    
    # Everything 설치 확인
    everything_exe = check_everything_available()
    if not everything_exe:
        logging.debug("Everything이 설치되어 있지 않습니다.")
        return False
    
    # Windows Search 서비스 확인
    if not check_windows_search_service():
        logging.debug("Windows Search 서비스가 실행되지 않고 있습니다.")
        logging.debug("Everything이 DB 캐싱을 제대로 활용하지 못할 수 있습니다.")
    
    # Everything 데이터베이스 설정 확인 및 자동 최적화
    if not check_everything_database():
        logging.debug("Everything 데이터베이스 설정이 최적화되지 않았습니다.")
        logging.debug("자동으로 설정을 최적화합니다...")
        from pk_internal_tools.pk_functions.ensure_everything_exe_database_reindex import ensure_everything_exe_database_reindex
        if ensure_everything_exe_database_reindex():
            logging.debug("Everything 설정 최적화가 완료되었습니다.")
        else:
            logging.debug("Everything 설정 최적화가 실패했습니다.")
    
    # Everything 경로 변경 감지 및 DB 업데이트
    try:
        from pk_internal_tools.pk_functions.ensure_everything_path_changed import ensure_everything_path_changed
        return ensure_everything_path_changed()
    except ImportError:
        logging.debug("Everything 경로 변경 감지 함수를 찾을 수 없습니다.")
        return True 