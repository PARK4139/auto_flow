import os
import winreg
import subprocess
import sys

def ensure_os_env_path_deduplicated():
    """OS PATH 환경변수에서 중복된 경로를 제거하는 함수"""
    try:
        # Lazy import to avoid circular dependency
        try:
            import logging
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
        except ImportError:
            print = lambda msg, **kwargs: print(msg)
            PkTexts = type('PkTexts', (), {
                'OS_PATH_USER_CLEANED': '사용자 PATH 환경변수가 정리되었습니다',
                'OS_PATH_CLEAN_FAILED': '환경변수 정리 실패',
                'OS_PATH_CHANGE_NOTIFICATION_SENT': '환경변수 변경 알림이 전송되었습니다',
                'OS_PATH_CHANGE_NOTIFICATION_FAILED': '환경변수 변경 알림 전송 실패',
                'OS_PATH_CHANGE_NOTIFICATION_ERROR': '환경변수 변경 알림 실패'
            })()

        import os
        import platform
        import subprocess
        
        # 현재 PATH 가져오기
        current_path = os.environ.get('PATH', '')
        
        if not current_path:
            print("PATH 환경변수가 비어있습니다.")
            return False
        
        # PATH를 경로별로 분리
        path_list = current_path.split(os.pathsep)
        
        # 중복 제거 (순서 유지)
        unique_paths = []
        seen = set()
        
        for path in path_list:
            normalized_path = os.path.normpath(path)
            if normalized_path not in seen:
                unique_paths.append(path)
                seen.add(normalized_path)
        
        # 변경사항 확인
        if len(unique_paths) == len(path_list):
            print("중복된 PATH가 없습니다.")
            return True
        
        # 새로운 PATH 생성
        new_path = os.pathsep.join(unique_paths)
        
        # 환경변수 업데이트
        try:
            os.environ['PATH'] = new_path
            
            # 운영체제별 영구 설정
            os_type = platform.system()
            
            if os_type == "Windows":
                # Windows 레지스트리 업데이트
                try:
                    import winreg
                    
                    # 사용자 환경변수 업데이트
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_WRITE)
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    winreg.CloseKey(key)
                    
                    print(f"[{PkTexts.OS_PATH_USER_CLEANED}] {PK_ANSI_COLOR_MAP['CYAN']}제거된중복={len(path_list) - len(unique_paths)}개 {PK_ANSI_COLOR_MAP['RESET']}")
                    
                    # 환경변수 변경 알림
                    try:
                        subprocess.run(["setx", "PATH", new_path], check=True)
                        print(f"[{PkTexts.OS_PATH_CHANGE_NOTIFICATION_SENT}] {PK_ANSI_COLOR_MAP['CYAN']}상태=성공 {PK_ANSI_COLOR_MAP['RESET']}")
                    except subprocess.CalledProcessError:
                        print(f"[{PkTexts.OS_PATH_CHANGE_NOTIFICATION_FAILED}] {PK_ANSI_COLOR_MAP['YELLOW']}상태=실패 {PK_ANSI_COLOR_MAP['RESET']}")
                        
                except Exception as e:
                    print(f"[{PkTexts.OS_PATH_CHANGE_NOTIFICATION_ERROR}] {PK_ANSI_COLOR_MAP['RED']}오류={e} {PK_ANSI_COLOR_MAP['RESET']}")
                    
            elif os_type in ["Linux", "Darwin"]:
                # Linux/macOS 설정 파일 업데이트
                shell_configs = [
                    os.path.expanduser("~/.bashrc"),
                    os.path.expanduser("~/.zshrc"),
                    os.path.expanduser("~/.profile")
                ]
                
                for config_file in shell_configs:
                    if os.path.exists(config_file):
                        try:
                            # 기존 PATH 설정 제거
                            with open(config_file, 'r') as f:
                                lines = f.readlines()
                            
                            # PATH 설정 라인 제거
                            filtered_lines = []
                            for line in lines:
                                if not line.strip().startswith('export PATH='):
                                    filtered_lines.append(line)
                            
                            # 새로운 PATH 설정 추가
                            filtered_lines.append(f'export PATH="{new_path}"\n')
                            
                            # 파일 업데이트
                            with open(config_file, 'w') as f:
                                f.writelines(filtered_lines)
                            
                            print(f"[{PkTexts.OS_PATH_USER_CLEANED}] {PK_ANSI_COLOR_MAP['CYAN']}설정파일={config_file} {PK_ANSI_COLOR_MAP['RESET']}")
                            break
                            
                        except Exception as e:
                            print(f"[{PkTexts.OS_PATH_CHANGE_NOTIFICATION_ERROR}] {PK_ANSI_COLOR_MAP['RED']}파일={config_file} 오류={e} {PK_ANSI_COLOR_MAP['RESET']}")
            
            return True
            
        except Exception as e:
            print(f"[{PkTexts.OS_PATH_CLEAN_FAILED}] {PK_ANSI_COLOR_MAP['RED']}오류={e} {PK_ANSI_COLOR_MAP['RESET']}")
            return False
            
    except Exception as e:
        print(f"[{PkTexts.OS_PATH_CLEAN_FAILED}] {PK_ANSI_COLOR_MAP['RED']}오류={e} {PK_ANSI_COLOR_MAP['RESET']}")
        return False

def get_system_path():
    """시스템 환경변수 PATH 가져오기"""
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                           r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 
                           0, winreg.KEY_READ) as key:
            try:
                system_path, _ = winreg.QueryValueEx(key, "Path")
                return system_path
            except FileNotFoundError:
                return ""
    except Exception:
        return ""

def get_user_path():
    """사용자 환경변수 PATH 가져오기"""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ) as key:
            try:
                user_path, _ = winreg.QueryValueEx(key, "Path")
                return user_path
            except FileNotFoundError:
                return ""
    except Exception:
        return ""

def broadcast_environment_change():
    """환경변수 변경을 시스템에 알림"""
    try:
        # WM_SETTINGCHANGE 메시지 브로드캐스트
        import ctypes
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        result = ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 
            SMTO_ABORTIFHUNG, 5000, ctypes.byref(ctypes.c_ulong())
        )
        if result:
            print("환경변수 변경 알림이 전송되었습니다.")
        else:
            print("️ 환경변수 변경 알림 전송 실패")
    except Exception as e:
        print(f"️ 환경변수 변경 알림 실패: {e}")

if __name__ == "__main__":
    ensure_os_env_path_deduplicated()
