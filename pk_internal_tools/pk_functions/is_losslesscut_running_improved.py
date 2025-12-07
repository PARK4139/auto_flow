def is_media_file_controller_running_improved():
    """하이브리드 방식 - 빠른 확인 + 백업"""
    import win32gui
    import logging
    import logging
    from pk_internal_tools.pk_objects.pk_texts import PkTexts
    
    TAG_INFO = PkTexts.get_value_via_attr("INFO")
    TAG_WARN = PkTexts.get_value_via_attr("WARNING")
    
    # 1차: 윈도우 핸들로 빠른 확인
    try:
        hwnd = win32gui.FindWindow(None, get_idle_title_of_losslesscut())
        if hwnd != 0:
            logging.debug(f"윈도우 핸들로 LosslessCut 실행 확인됨")
            return True
    except Exception as e:
        logging.debug(f"{TAG_WARN} 윈도우 핸들 확인 실패: {e}")
    
    # 2차: 프로세스 목록으로 백업 확인 (psutil 사용)
    try:
        import psutil
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'LosslessCut.exe':
                logging.debug(f"프로세스 목록으로 LosslessCut 실행 확인됨")
                return True
    except ImportError:
        logging.debug(f"{TAG_WARN} psutil 모듈 없음 - 백업 확인 생략")
    except Exception as e:
        logging.debug(f"{TAG_WARN} 프로세스 목록 확인 실패: {e}")
    
    # 3차: 기존 방식으로 최종 확인 (캐시 사용)
    try:
        from pk_internal_tools.pk_functions.is_media_file_controller_running_v1 import is_media_file_controller_running_v1
        result = is_media_file_controller_running_v1()
        if result:
            logging.debug(f"기존 방식으로 LosslessCut 실행 확인됨")
        return result
    except Exception as e:
        logging.debug(f"{TAG_WARN} 기존 방식 확인 실패: {e}")
    
    return False


def is_media_file_controller_running_fast():
    """가장 빠른 방식 - 윈도우 핸들만 사용"""
    try:
        import win32gui
        hwnd = win32gui.FindWindow(None, get_idle_title_of_losslesscut())
        return hwnd != 0
    except:
        return False


def is_media_file_controller_running_reliable():
    """가장 안정적인 방식 - 모든 방법 시도"""
    return is_media_file_controller_running_improved()
