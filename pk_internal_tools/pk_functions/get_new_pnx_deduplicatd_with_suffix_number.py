
def get_new_pnx_deduplicatd_with_suffix_number(base_pnx, target_directory, max_attempts=1000):
    """
    파일명 중복을 방지하기 위해 suffix에 숫자를 추가하여 고유한 파일명을 반환
    
    Args:
        base_pnx: 기본 파일명 (확장자 포함)
        target_directory: 대상 디렉토리 경로
        max_attempts: 최대 시도 횟수 (기본값: 1000)
        
    Returns:
        str: 중복되지 않는 파일명
        
    Raises:
        ValueError: max_attempts 초과 시
    """
    import os
    import logging
    import logging
    from pathlib import Path
    
    # 파일명과 확장자 분리
    name, ext = os.path.splitext(base_pnx)
    
    # 기본 파일명으로 시작
    final_filename = base_pnx
    target_path = os.path.join(target_directory, final_filename)
    
    # 파일이 존재하지 않으면 기본 파일명 반환
    if not os.path.exists(target_path):
        logging.debug(f"기본 파일명 사용 가능: {base_pnx}")
        return base_pnx
    
    # 파일명 충돌 해결을 위한 숫자 suffix 추가
    counter = 1
    while counter <= max_attempts:
        final_filename = f"{name}_{counter}{ext}"
        target_path = os.path.join(target_directory, final_filename)
        
        if not os.path.exists(target_path):
            logging.debug(f"중복 해결된 파일명 발견: {final_filename}")
            return final_filename
        
        logging.debug(f"파일명 충돌 해결 시도 {counter}: {final_filename} (이미 존재함)")
        counter += 1
    
    # max_attempts 초과 시 오류 발생
    error_msg = f"파일명 중복 해결 실패: {base_pnx} - {max_attempts}번 이상 시도"
    logging.error(error_msg)
    raise ValueError(error_msg)


def get_new_pnx_deduplicatd_with_suffix_number_v2(base_pnx, target_directory, max_attempts=1000):
    """
    파일명 중복을 방지하기 위해 suffix에 숫자를 추가하여 고유한 파일명을 반환 (v2)
    
    Args:
        base_pnx: 기본 파일명 (확장자 포함)
        target_directory: 대상 디렉토리 경로
        max_attempts: 최대 시도 횟수 (기본값: 1000)
        
    Returns:
        tuple: (중복되지 않는 파일명, 실제 대상 경로)
        
    Raises:
        ValueError: max_attempts 초과 시
    """
    import os
    import logging
    import logging
    from pathlib import Path
    
    # 파일명과 확장자 분리
    name, ext = os.path.splitext(base_pnx)
    
    # 기본 파일명으로 시작
    final_filename = base_pnx
    target_path = os.path.join(target_directory, final_filename)
    
    # 파일이 존재하지 않으면 기본 파일명 반환
    if not os.path.exists(target_path):
        logging.debug(f"기본 파일명 사용 가능: {base_pnx}")
        return final_filename, target_path
    
    # 파일명 충돌 해결을 위한 숫자 suffix 추가
    counter = 1
    while counter <= max_attempts:
        final_filename = f"{name}_{counter}{ext}"
        target_path = os.path.join(target_directory, final_filename)
        
        if not os.path.exists(target_path):
            logging.debug(f"중복 해결된 파일명 발견: {final_filename}")
            return final_filename, target_path
        
        logging.debug(f"파일명 충돌 해결 시도 {counter}: {final_filename} (이미 존재함)")
        counter += 1
    
    # max_attempts 초과 시 오류 발생
    error_msg = f"파일명 중복 해결 실패: {base_pnx} - {max_attempts}번 이상 시도"
    logging.error(error_msg)
    raise ValueError(error_msg)


def get_new_pnx_deduplicatd_with_suffix_number_v3(base_pnx, target_directory, max_attempts=1000):
    """
    파일명 중복을 방지하기 위해 suffix에 숫자를 추가하여 고유한 파일명을 반환 (v3)
    
    Args:
        base_pnx: 기본 파일명 (확장자 포함)
        target_directory: 대상 디렉토리 경로
        max_attempts: 최대 시도 횟수 (기본값: 1000)
        
    Returns:
        dict: {
            'filename': 중복되지 않는 파일명,
            'target_path': 실제 대상 경로,
            'was_renamed': 이름이 변경되었는지 여부,
            'attempts': 시도 횟수
        }
        
    Raises:
        ValueError: max_attempts 초과 시
    """
    import os
    import logging
    import logging
    from pathlib import Path
    
    # 파일명과 확장자 분리
    name, ext = os.path.splitext(base_pnx)
    
    # 기본 파일명으로 시작
    final_filename = base_pnx
    target_path = os.path.join(target_directory, final_filename)
    
    # 파일이 존재하지 않으면 기본 파일명 반환
    if not os.path.exists(target_path):
        logging.debug(f"기본 파일명 사용 가능: {base_pnx}")
        return {
            'filename': final_filename,
            'target_path': target_path,
            'was_renamed': False,
            'attempts': 0
        }
    
    # 파일명 충돌 해결을 위한 숫자 suffix 추가
    counter = 1
    while counter <= max_attempts:
        final_filename = f"{name}_{counter}{ext}"
        target_path = os.path.join(target_directory, final_filename)
        
        if not os.path.exists(target_path):
            logging.debug(f"중복 해결된 파일명 발견: {final_filename}")
            return {
                'filename': final_filename,
                'target_path': target_path,
                'was_renamed': True,
                'attempts': counter
            }
        
        logging.debug(f"파일명 충돌 해결 시도 {counter}: {final_filename} (이미 존재함)")
        counter += 1
    
    # max_attempts 초과 시 오류 발생
    error_msg = f"파일명 중복 해결 실패: {base_pnx} - {max_attempts}번 이상 시도"
    logging.error(error_msg)
    raise ValueError(error_msg)

