def ensure_everything_ssd_optimized():
    """SSD에서 Everything 검색 성능 최적화"""
    import os
    import subprocess
    import logging
    
    def check_ssd_optimization():
        """SSD 최적화 설정 확인"""
        try:
            # Windows Search 서비스 상태 확인
            result = subprocess.run(
                ['sc', 'query', 'WSearch'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0 and "RUNNING" in result.stdout:
                logging.debug("Windows Search 서비스가 정상 실행 중입니다.")
            else:
                logging.debug("Windows Search 서비스가 비활성화되어 있습니다.")
                logging.debug("SSD에서 Everything 성능이 저하될 수 있습니다.")
                return False
            
            # Windows Search Index 상태 확인
            try:
                index_result = subprocess.run(
                    ['powershell', '-Command', 'Get-WmiObject -Class "Win32_Volume" | Where-Object {$_.DriveLetter -eq "C:"} | Select-Object IndexingEnabled'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if "True" in index_result.stdout:
                    logging.debug("Windows Search Index가 활성화되어 있습니다.")
                else:
                    logging.debug("Windows Search Index가 비활성화되어 있습니다.")
                    logging.debug("SSD에서 Everything 성능이 크게 저하될 수 있습니다.")
                    return False
            except:
                logging.debug("Windows Search Index 상태를 확인할 수 없습니다.")
            
            # Everything.ini SSD 최적화 설정 확인
            everything_ini = os.path.expanduser(r"~\AppData\Roaming\Everything\Everything.ini")
            if os.path.exists(everything_ini):
                with open(everything_ini, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # SSD 최적화 설정들 (중복 제거)
                    ssd_settings = [
                        "index_folders=1",
                        "index_files=1", 
                        "fast_sort=1",
                        "fast_size_sort=1",
                        "fast_date_sort=1",
                        "fast_date_modified_sort=1",
                        "fast_date_created_sort=1",
                        "fast_date_accessed_sort=1",
                        "fast_attributes_sort=1",
                        "fast_path_sort=1",
                        "fast_name_sort=1",
                        "fast_extension_sort=1",
                        "usn_log=1",  # USN Journal 활성화
                        "ntfs_volume_guid=1",  # NTFS 볼륨 GUID 사용
                        "include_folder=C:\\",  # C 드라이브 포함
                        "include_folder=D:\\",  # D 드라이브 포함
                        "include_folder=E:\\",  # E 드라이브 포함
                        "include_folder=F:\\",  # F 드라이브 포함
                        "include_folder=G:\\",  # G 드라이브 포함
                        "include_folder=H:\\"   # H 드라이브 포함
                    ]
                    
                    missing_settings = []
                    for setting in ssd_settings:
                        if setting not in content:
                            missing_settings.append(setting)
                    
                    if missing_settings:
                        logging.debug("SSD 최적화 설정이 누락되었습니다.")
                        logging.debug("자동으로 SSD 최적화 설정을 추가합니다...")
                        
                        # 누락된 설정 추가
                        with open(everything_ini, 'a', encoding='utf-8') as f:
                            f.write("\n# SSD 최적화 설정\n")
                            for setting in missing_settings:
                                f.write(f"{setting}\n")
                        
                        logging.debug("SSD 최적화 설정이 추가되었습니다.")
                        return True
                    else:
                        logging.debug("SSD 최적화 설정이 이미 적용되어 있습니다.")
                        return True
            
            return True
            
        except Exception as e:
            logging.debug(f"SSD 최적화 확인 중 오류: {e}")
            return False
    
    def optimize_windows_search_for_ssd():
        """Windows Search를 SSD에 최적화"""
        try:
            # Windows Search 서비스 재시작
            logging.debug("Windows Search 서비스를 SSD에 최적화합니다...")
            
            subprocess.run(['net', 'stop', 'WSearch'], capture_output=True, timeout=30)
            subprocess.run(['net', 'start', 'WSearch'], capture_output=True, timeout=30)
            
            # Windows Search Index 재구축
            logging.debug("Windows Search Index를 재구축합니다...")
            subprocess.run([
                'powershell', '-Command', 
                'Get-WmiObject -Class "Win32_Volume" | Where-Object {$_.DriveLetter -eq "C:"} | ForEach-Object {$_.Reindex()}'
            ], capture_output=True, timeout=60)
            
            logging.debug("Windows Search 서비스가 재시작되었습니다.")
            return True
            
        except Exception as e:
            logging.debug(f"Windows Search 최적화 중 오류: {e}")
            return False
    
    def check_ntfs_usn_journal():
        """NTFS USN Journal 상태 확인"""
        try:
            # USN Journal 상태 확인
            result = subprocess.run([
                'fsutil', 'usn', 'queryjournal', 'C:'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                logging.debug("NTFS USN Journal이 정상 작동 중입니다.")
                return True
            else:
                logging.debug("NTFS USN Journal에 문제가 있을 수 있습니다.")
                return False
                
        except Exception as e:
            logging.debug(f"NTFS USN Journal 확인 중 오류: {e}")
            return False
    
    # NTFS USN Journal 확인
    check_ntfs_usn_journal()
    
    # SSD 최적화 확인 및 적용
    if check_ssd_optimization():
        logging.debug("SSD 최적화 설정이 확인되었습니다.")
    else:
        logging.debug("SSD 최적화 설정을 적용합니다...")
        optimize_windows_search_for_ssd()
    
    return True 