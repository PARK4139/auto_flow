#!/usr/bin/env python3
"""
클립보드 보존 기능 (v2) - 더 안정적인 버전
"""

import time
import subprocess
from pathlib import Path
import logging
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


class ClipboardPreserverV2:
    """클립보드 내용을 보존하는 개선된 클래스 (v2)"""
    
    def __init__(self):
        self.original_content = None
        self.is_preserved = False
        self.clipboard_working = False
    
    def _test_clipboard_access(self):
        """클립보드 접근 가능 여부 테스트"""
        try:
            test_content = "clipboard_test_12345"
            self._copy_to_clipboard(test_content)
            time.sleep(0.1)  # 잠시 대기
            retrieved = self._get_from_clipboard()
            self.clipboard_working = (test_content in retrieved)
            
            if self.clipboard_working:
                logging.debug("클립보드 접근 테스트 성공")
            else:
                logging.debug("클립보드 접근 테스트 실패")
                
            return self.clipboard_working
        except Exception as e:
            logging.debug(f"클립보드 테스트 중 오류: {str(e)}")
            self.clipboard_working = False
            return False
    
    def _copy_to_clipboard(self, text):
        """클립보드에 텍스트 복사 (개선된 버전)"""
        try:
            from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
            from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
            
            if is_os_wsl_linux():
                # WSL에서 더 안정적인 방법 사용
                try:
                    # echo 명령어로 텍스트를 클립보드에 복사
                    cmd = f'echo "{text}" | clip.exe'
                    subprocess.run(cmd, shell=True, check=True, capture_output=True)
                    return True
                except:
                    try:
                        # PowerShell 사용 (더 안정적)
                        ps_cmd = f'Set-Clipboard -Value "{text}"'
                        subprocess.run(['powershell.exe', '-Command', ps_cmd], 
                                     check=True, capture_output=True)
                        return True
                    except:
                        return False
            elif is_os_windows():
                try:
                    import clipboard
                    clipboard.copy(text)
                    return True
                except ImportError:
                    # clipboard 모듈이 없으면 cmd 사용
                    cmd = f'echo {text} | clip'
                    subprocess.run(cmd, shell=True, check=True, capture_output=True)
                    return True
            else:
                # Linux/macOS
                try:
                    subprocess.run(['xclip', '-selection', 'clipboard'], 
                                 input=text.encode(), check=True, capture_output=True)
                    return True
                except:
                    try:
                        subprocess.run(['pbcopy'], input=text.encode(), 
                                     check=True, capture_output=True)
                        return True
                    except:
                        return False
        except Exception as e:
            logging.debug(f"클립보드 복사 실패: {str(e)}")
            return False
    
    def _get_from_clipboard(self):
        """클립보드에서 텍스트 가져오기 (개선된 버전)"""
        try:
            from pk_internal_tools.pk_functions.is_os_wsl_linux import is_os_wsl_linux
            from pk_internal_tools.pk_functions.is_os_windows import is_os_windows
            
            if is_os_wsl_linux():
                try:
                    # clip.exe 사용 (더 안정적)
                    result = subprocess.run(['clip.exe'], capture_output=True, text=True)
                    if result.returncode == 0:
                        return result.stdout.strip()
                except:
                    try:
                        # PowerShell 사용
                        result = subprocess.run(['powershell.exe', '-Command', 'Get-Clipboard'], 
                                             capture_output=True, text=True)
                        if result.returncode == 0:
                            return result.stdout.strip()
                    except:
                        pass
                return ""
            elif is_os_windows():
                try:
                    import clipboard
                    return clipboard.paste()
                except ImportError:
                    # clipboard 모듈이 없으면 빈 문자열 반환
                    return ""
            else:
                # Linux/macOS
                try:
                    result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                         capture_output=True, text=True)
                    if result.returncode == 0:
                        return result.stdout.strip()
                except:
                    try:
                        result = subprocess.run(['pbpaste'], capture_output=True, text=True)
                        if result.returncode == 0:
                            return result.stdout.strip()
                    except:
                        pass
                return ""
        except Exception as e:
            logging.debug(f"클립보드 읽기 실패: {str(e)}")
            return ""
    
    def preserve(self):
        """현재 클립보드 내용을 보존"""
        try:
            # 클립보드 접근 가능 여부 먼저 테스트
            if not self._test_clipboard_access():
                logging.debug("클립보드 접근 불가 - 보존 건너뜀")
                self.original_content = ""
                self.is_preserved = True
                return True
            
            # 현재 클립보드 내용 가져오기
            self.original_content = self._get_from_clipboard()
            
            # None이나 빈 문자열인 경우도 처리
            if self.original_content is None:
                self.original_content = ""
            
            self.is_preserved = True
            content_preview = str(self.original_content)[:50] if self.original_content else "(빈 클립보드)"
            logging.debug(f"클립보드 내용을 보존했습니다: {content_preview}")
            return True
            
        except Exception as e:
            logging.debug(f"클립보드 보존 실패: {str(e)}")
            self.original_content = ""
            self.is_preserved = True
            return True
    
    def restore(self):
        """보존된 클립보드 내용을 복원"""
        if not self.is_preserved or self.original_content is None:
            logging.debug("보존된 클립보드 내용이 없습니다.")
            return False
        
        try:
            if not self.clipboard_working:
                logging.debug("클립보드 접근 불가 - 복원 건너뜀")
                return False
            
            # 클립보드에 내용 복원
            success = self._copy_to_clipboard(self.original_content)
            
            if success:
                logging.debug("클립보드 내용을 복원했습니다.")
                # 복원 후 검증
                time.sleep(0.1)
                restored_content = self._get_from_clipboard()
                if self.original_content in restored_content:
                    logging.debug("클립보드 복원 검증 성공")
                else:
                    logging.debug("클립보드 복원 검증 실패")
                return True
            else:
                logging.debug("클립보드 복원 실패")
                return False
                
        except Exception as e:
            logging.debug(f"클립보드 복원 실패: {str(e)}")
            return False
    
    def get_original_content(self):
        """보존된 원본 내용 반환"""
        return self.original_content
    
    def is_clipboard_working(self):
        """클립보드가 정상 작동하는지 확인"""
        return self.clipboard_working


def ensure_clipboard_preserved_v2(func):
    """클립보드 보존 데코레이터 (v2)"""
    def wrapper(*args, **kwargs):
        preserver = ClipboardPreserverV2()
        
        # 함수 실행 전 클립보드 보존
        if preserver.preserve():
            try:
                # 원본 함수 실행
                result = func(*args, **kwargs)
                return result
            finally:
                # 함수 실행 후 클립보드 복원
                preserver.restore()
        else:
            # 보존 실패 시 원본 함수만 실행
            return func(*args, **kwargs)
    
    return wrapper


def with_clipboard_preservation_v2(func):
    """클립보드 보존 컨텍스트 매니저 (v2)"""
    def wrapper(*args, **kwargs):
        preserver = ClipboardPreserverV2()
        
        # 함수 실행 전 클립보드 보존
        if preserver.preserve():
            try:
                # 원본 함수 실행
                result = func(*args, **kwargs)
                return result
            finally:
                # 함수 실행 후 클립보드 복원
                preserver.restore()
        else:
            # 보존 실패 시 원본 함수만 실행
            return func(*args, **kwargs)
    
    return wrapper


def test_clipboard_functionality():
    """클립보드 기능 테스트"""
    preserver = ClipboardPreserverV2()
    
    print("=== 클립보드 기능 테스트")
    
    # n. 클립보드 접근 테스트
    print("1. 클립보드 접근 테스트...")
    if preserver._test_clipboard_access():
        print(" 클립보드 접근 성공")
    else:
        print(" 클립보드 접근 실패")
        return False
    
    # n. 복사 테스트
    print("2. 클립보드 복사 테스트...")
    test_text = "테스트 텍스트 12345"
    if preserver._copy_to_clipboard(test_text):
        print(" 클립보드 복사 성공")
    else:
        print(" 클립보드 복사 실패")
        return False
    
    # n. 읽기 테스트
    print("3. 클립보드 읽기 테스트...")
    time.sleep(0.1)
    retrieved = preserver._get_from_clipboard()
    if test_text in retrieved:
        print(" 클립보드 읽기 성공")
    else:
        print(" 클립보드 읽기 실패")
        return False
    
    # n. 보존/복원 테스트
    print("4. 클립보드 보존/복원 테스트...")
    if preserver.preserve():
        print(" 클립보드 보존 성공")
        
        # 다른 내용으로 변경
        preserver._copy_to_clipboard("변경된 내용")
        time.sleep(0.1)
        
        # 원본 내용 복원
        if preserver.restore():
            print(" 클립보드 복원 성공")
            
            # 복원 확인
            final_content = preserver._get_from_clipboard()
            if test_text in final_content:
                print(" 클립보드 복원 검증 성공")
                return True
            else:
                print(" 클립보드 복원 검증 실패")
                return False
        else:
            print(" 클립보드 복원 실패")
            return False
    else:
        print(" 클립보드 보존 실패")
        return False


if __name__ == "__main__":
    # 클립보드 기능 테스트 실행
    test_clipboard_functionality()
