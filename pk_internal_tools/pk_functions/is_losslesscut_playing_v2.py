def is_losslesscut_playing_v2(threshold=3.0, check_duration=3, second_interval=0.5, use_multiple_methods=True):
    """
    LosslessCut에서 비디오 재생 상태를 간단하게 확인하는 함수
    - 스페이스바를 누른 후 상태 변화를 통해 유추
    - CPU 사용량 측정 없이 창 제목만으로 확인
    """
    import time
    import logging
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    
    def check_window_title_status():
        """창 제목을 통해 재생 상태를 확인하는 함수"""
        try:
            titles = get_window_titles()
            for title in titles:
                if get_idle_title_of_losslesscut() in title:
                    # 로딩 중이 아닌지 확인
                    loading_patterns = ["불러오는 중", "Loading", "로딩 중", "Processing"]
                    if not any(pattern in title for pattern in loading_patterns):
                        # 파일명이 포함되어 있고 로딩 중이 아니면 재생 가능 상태로 간주
                        return True
        except Exception as e:
            logging.debug(f"창 제목 확인 오류: {str(e)}")
        return False
    
    # 창 제목으로 상태 확인
    if check_window_title_status():
        logging.debug("창 제목으로 재생 준비 상태 확인됨")
        return True
    
    # 잠시 대기 후 재확인
    logging.debug("재생 상태 확인을 위해 잠시 대기...")
    time.sleep(1)
    
    if check_window_title_status():
        logging.debug("대기 후 재생 준비 상태 확인됨")
        return True
    
    logging.debug("재생 준비 상태를 확인할 수 없습니다.")
    return False


def is_losslesscut_ready_for_playback(timeout=10, check_interval=0.5):
    """
    LosslessCut이 재생 준비가 되었는지 확인하는 함수
    """
    import time
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    import logging
    
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            titles = get_window_titles()
            for title in titles:
                if get_idle_title_of_losslesscut() in title:
                    # 로딩 중이 아닌지 확인
                    loading_patterns = ["불러오는 중", "Loading", "로딩 중", "Processing"]
                    if not any(pattern in title for pattern in loading_patterns):
                        # 파일명이 포함되어 있는지 확인 (비디오가 로드되었는지)
                        if any(char.isalnum() for char in title if char not in "LosslessCut -"):
                            logging.debug("LosslessCut이 재생 준비되었습니다.")
                            return True
            
            time.sleep(check_interval)
            
        except Exception as e:
            logging.debug(f"재생 준비 상태 확인 오류: {str(e)}")
            time.sleep(check_interval)
    
    logging.debug(f"재생 준비 대기 타임아웃 ({timeout}초)")
    return False


def get_losslesscut_status():
    """
    LosslessCut의 현재 상태를 간단하게 확인하는 함수
    """
    import logging
    from pk_internal_tools.pk_functions.get_window_titles import get_window_titles
    
    status_info = {
        "is_running": False,
        "is_loading": False,
        "is_ready": False,
        "window_titles": []
    }
    
    try:
        # 창 제목 확인
        titles = get_window_titles()
        status_info["window_titles"] = titles
        
        losslesscut_titles = [title for title in titles if get_idle_title_of_losslesscut() in title]
        if losslesscut_titles:
            status_info["is_running"] = True
            
            # 로딩 상태 확인
            loading_patterns = ["불러오는 중", "Loading", "로딩 중", "Processing"]
            status_info["is_loading"] = any(
                any(pattern in title for pattern in loading_patterns)
                for title in losslesscut_titles
            )
            
            # 준비 상태 확인
            if not status_info["is_loading"]:
                status_info["is_ready"] = True
        
        logging.debug(f"LosslessCut 상태: {status_info}")
        
    except Exception as e:
        logging.debug(f"상태 확인 오류: {str(e)}")
    
    return status_info
