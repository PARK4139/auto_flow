import os
from pathlib import Path
import logging
from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE


def get_f_video_of_d_working_by_creation_date(d_working, ext_list_allowed, sort_by='file_name', reverse=False):
    """
    작업 디렉토리에서 허용된 확장자를 가진 비디오 파일들을 정렬하여 반환
    
    Args:
        d_working: 작업 디렉토리 경로
        ext_list_allowed: 허용된 파일 확장자 리스트 (예: ['.mp4', '.avi', '.mkv'])
        sort_by: 정렬 기준 ('file_name', 'creation_time', 'modification_time', 'access_time')
        reverse: True면 내림차순, False면 오름차순 (file_name의 경우 False가 A-Z순)
    
    Returns:
        정렬된 비디오 파일 경로 리스트 또는 None
    """
    try:
        # Path 객체로 변환
        d_working_path = Path(d_working)
        
        logging.debug(f'''d_working={d_working} extension_list_allowed={ext_list_allowed} ''')
        
        if not d_working_path.exists():
            logging.debug(f"d_working does not exists {d_working}")
            return None
            
        # 디렉토리 내 모든 파일 경로 생성
        f_list_of_d_working = [d_working_path / f for f in os.listdir(d_working_path)]
        logging.debug(f'''len(f_list_of_d_working)={len(f_list_of_d_working)}  ''')
        
        # 허용된 확장자를 가진 비디오 파일만 필터링
        media_files_allowed = []
        for f_path in f_list_of_d_working:
            if f_path.is_file():
                ext = f_path.suffix.lower()
                f_name = f_path.name.lower()
                
                # 허용된 확장자이고 seg, temp 키워드가 포함되지 않은 파일만 선택
                if (ext in ext_list_allowed and 
                    not any(keyword in f_name for keyword in ["seg", "temp"])):
                    media_files_allowed.append(f_path)
        
        logging.debug(f'''len(media_files_allowed)={len(media_files_allowed)}  ''')
        
        if not media_files_allowed:
            logging.debug("조건에 맞는 비디오 파일이 없습니다.")
            return None
        
        # 파일 정렬 함수 정의
        def get_file_time(file_path, time_type):
            """파일의 시간 정보를 가져오는 함수"""
            try:
                if time_type == 'creation_time':
                    # Windows에서는 st_ctime이 상태변경시간, Unix에서는 st_ctime이 상태변경시간
                    # 실제 파일 생성 시간을 얻기 어려우므로 수정시간을 사용하는 것이 더 정확
                    if os.name == 'nt':  # Windows
                        # Windows에서는 수정시간이 더 정확 (다운로드 시간과 일치)
                        return os.path.getmtime(file_path)
                    else:  # Unix/Linux
                        return os.path.getctime(file_path)
                elif time_type == 'modification_time':
                    return os.path.getmtime(file_path)
                elif time_type == 'access_time':
                    return os.path.getatime(file_path)
                else:
                    return os.path.getmtime(file_path)  # 기본값
            except (OSError, AttributeError):
                return 0  # 오류 시 기본값
        
        # 파일들을 지정된 기준으로 정렬
        if sort_by == 'file_name':
            # 파일명으로 정렬 (기본값)
            f_videos_sorted = sorted(
                media_files_allowed,
                key=lambda f: f.nick_name.lower(),  # 대소문자 구분 없이
                reverse=reverse
            )
        else:
            # 시간 기반 정렬
            f_videos_sorted = sorted(
                media_files_allowed,
                key=lambda f: get_file_time(f, sort_by),
                reverse=reverse
            )
        
        # 정렬 결과 로깅
        if sort_by == 'file_name':
            sort_direction = 'Z-A순' if reverse else 'A-Z순'
            logging.debug(f"비디오 파일을 파일명 기준으로 {sort_direction} 정렬했습니다.")
            for i, f_path in enumerate(f_videos_sorted[:5]):  # 상위 5개만 로깅
                logging.debug(f"{i+1}: {f_path.nick_name}")
        else:
            time_direction = '최신순' if reverse else '오래된순'
            logging.debug(f"비디오 파일을 {sort_by} 기준으로 {time_direction} 정렬했습니다.")
            for i, f_path in enumerate(f_videos_sorted[:5]):  # 상위 5개만 로깅
                time_info = get_file_time(f_path, sort_by)
                from datetime import datetime
                time_dt = datetime.fromtimestamp(time_info)
                time_str = time_dt.strftime('%Y-%m-%d %H:%M:%S')
                logging.debug(f"{i+1}: {f_path.nick_name} (시간: {time_str})")
        
        if len(f_videos_sorted) > 5:
            logging.debug(f"... 외 {len(f_videos_sorted) - 5}개 파일")
        
        return f_videos_sorted
        
    except Exception as e:
        logging.debug(f"비디오 파일 정렬 중 오류 발생: {str(e)}")
        return None


def get_latest_video_from_d_working(d_working, ext_list_allowed):
    """
    작업 디렉토리에서 가장 최근에 생성된 비디오 파일을 반환
    
    Args:
        d_working: 작업 디렉토리 경로
        ext_list_allowed: 허용된 파일 확장자 리스트
    
    Returns:
        가장 최근 비디오 파일 경로 또는 None
    """
    videos = get_f_video_of_d_working_by_creation_date(d_working, ext_list_allowed, sort_by='creation_time', reverse=True)
    if videos and len(videos) > 0:
        return videos[0]
    return None


def get_oldest_video_from_d_working(d_working, ext_list_allowed):
    """
    작업 디렉토리에서 가장 오래된 비디오 파일을 반환
    
    Args:
        d_working: 작업 디렉토리 경로
        ext_list_allowed: 허용된 파일 확장자 리스트
    
    Returns:
        가장 오래된 비디오 파일 경로 또는 None
    """
    videos = get_f_video_of_d_working_by_creation_date(d_working, ext_list_allowed, sort_by='creation_time', reverse=False)
    if videos and len(videos) > 0:
        return videos[0]
    return None


def get_videos_by_date_range(d_working, ext_list_allowed, start_date=None, end_date=None):
    """
    특정 날짜 범위 내의 비디오 파일들을 반환
    
    Args:
        d_working: 작업 디렉토리 경로
        ext_list_allowed: 허용된 파일 확장자 리스트
        start_date: 시작 날짜 (datetime 객체 또는 None)
        end_date: 종료 날짜 (datetime 객체 또는 None)
    
    Returns:
        날짜 범위 내 비디오 파일 경로 리스트
    """
    from datetime import datetime
    
    videos = get_f_video_of_d_working_by_creation_date(d_working, ext_list_allowed, sort_by='creation_time', reverse=True)
    
    if not videos:
        return []
    
    filtered_videos = []
    
    for video_path in videos:
        try:
            creation_time = os.path.getctime(video_path)
            video_date = datetime.fromtimestamp(creation_time)
            
            # 날짜 범위 체크
            if start_date and video_date < start_date:
                continue
            if end_date and video_date > end_date:
                continue
                
            filtered_videos.append(video_path)
            
        except (OSError, AttributeError):
            continue
    
    return filtered_videos
