def ensure_everything_exe_database_reindex():
    """Everything DB 재구축 함수"""
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
    
    def optimize_everything_settings():
        """Everything 설정 최적화"""
        try:
            everything_ini = os.path.expanduser(r"~\AppData\Roaming\Everything\Everything.ini")
            if not os.path.exists(everything_ini):
                logging.debug("Everything 설정 파일을 찾을 수 없습니다.")
                return False
            
            # 설정 파일 읽기
            with open(everything_ini, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 필요한 설정 추가
            settings_to_add = [
                "index_folders=1",
                "index_files=1",
                "include_folder=C:\\",
                "include_folder=D:\\",
                "include_folder=E:\\",
                "include_folder=F:\\",
                "include_folder=G:\\",
                "include_folder=H:\\"
            ]
            
            modified = False
            for setting in settings_to_add:
                if setting not in content:
                    content += f"\n{setting}"
                    modified = True
            
            # 설정 파일 업데이트
            if modified:
                with open(everything_ini, 'w', encoding='utf-8') as f:
                    f.write(content)
                logging.debug("Everything 설정이 최적화되었습니다.")
                return True
            else:
                logging.debug("Everything 설정이 이미 최적화되어 있습니다.")
                return True
                
        except Exception as e:
            logging.debug(f"Everything 설정 최적화 실패: {e}")
            return False
    
    # Everything 설치 확인
    everything_exe = check_everything_available()
    if not everything_exe:
        logging.debug("Everything이 설치되어 있지 않습니다.")
        return False
    
    # Everything 설정 최적화
    if not optimize_everything_settings():
        return False
    
    # Everything DB 재구축 명령 실행
    try:
        logging.debug("Everything DB 재구축을 시작합니다...")
        rebuild_cmd = f'"{everything_exe}" -reindex'
        result = subprocess.run(
            rebuild_cmd,
            capture_output=True,
            text=True,
            timeout=120,  # DB 재구축은 시간이 오래 걸릴 수 있음
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        
        if result.returncode == 0:
            logging.debug("Everything DB 재구축이 완료되었습니다.")
            return True
        else:
            logging.debug(f"Everything DB 재구축 실패: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logging.debug("Everything DB 재구축 시간 초과")
        return False
    except Exception as e:
        logging.debug(f"Everything DB 재구축 중 오류: {e}")
        return False 