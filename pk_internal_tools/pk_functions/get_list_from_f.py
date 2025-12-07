def get_list_from_f(f):
    from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    import logging
    from pathlib import Path

    import os
    import traceback

    f = Path(f)
    logging.debug(f'''f={f}''')

    if f is None:
        return []

    try:
        if os.path.exists(f):
            # 수정: 디렉토리인지 체크 추가
            if os.path.isdir(f):
                logging.debug(f'''경고: {f}는 디렉토리입니다. 파일이 아닙니다.  ''')
                return []
            
            # 먼저 UTF-8로 시도
            try:
                with open(file=f, mode='r', encoding=PkEncoding.UTF8.value, errors='ignore') as f_obj:
                    lines = f_obj.readlines()
                    if lines is None:
                        return []
                    return lines
            except UnicodeDecodeError:
                # UTF-8 실패 시 UTF-16으로 시도
                try:
                    with open(file=f, mode='r', encoding='utf-16', errors='ignore') as f_obj:
                        lines = f_obj.readlines()
                        if lines is None:
                            return []
                        return lines
                except UnicodeDecodeError:
                    # UTF-16도 실패 시 cp949로 시도
                    with open(file=f, mode='r', encoding='cp949', errors='ignore') as f_obj:
                        lines = f_obj.readlines()
                        if lines is None:
                            return []
                        return lines
        else:
            logging.debug(f'''파일이 존재하지 않습니다: {f}  ''')
            return []
    except:
        logging.debug(f'''{traceback.format_exc()}  " ''')
        return []
