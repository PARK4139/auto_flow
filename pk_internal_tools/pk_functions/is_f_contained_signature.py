from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
import logging


def is_f_contained_signature(signature, d_pnx, expected_extension=None):
    """
    주어진 디렉토리(d_pnx)에서 signature을 포함하고 expected_extension으로 끝나는 파일이 있는지 확인합니다.
    yt-dlp의 임시 파일(.fXXX.mp4)은 무시합니다.
    """
    import os
    import re

    if not os.path.exists(d_pnx):
        logging.debug(f'''Directory does not exist: {d_pnx}  ''')
        return False

    for file_name in os.listdir(d_pnx):
        if signature in file_name:
            if expected_extension:
                # 임시 파일 패턴 (예: .f401.mp4)을 제외
                if expected_extension == ".mp4" and re.search(r"\.f\d{3}\.mp4$", file_name):
                    logging.debug(f"임시 파일로 판단되어 무시: {file_name}")
                    continue
                if file_name.endswith(expected_extension):
                    return True
            else:
                # expected_extension이 없으면 signature만으로 판단 (기존 로직)
                return True
    return False
