from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
import logging


def get_str_from_f(f):
    import os
    import traceback
    import inspect

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    logging.debug(f'''f={f}''')

    if f is None:
        return ""

    try:
        if os.path.exists(f):
            # f 읽기
            with open(file=f, mode='r', encoding=PkEncoding.UTF8.value, errors='ignore') as f:
                content = f.read()  # f 내용을 문자열로 읽기
                if content is None:
                    return ""
                return content
    except Exception as e:
        logging.debug(f'''{traceback.format_exc()}  " ''')
        return ""
