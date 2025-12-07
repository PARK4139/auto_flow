def ensure_list_written_to_f(working_list, f, mode, encoding=None, line_feed_mode=1, head_line_mode=True):
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pathlib import Path
    from enum import Enum
    encoding: Enum
    encoding = encoding or PkEncoding.UTF8
    f = Path(f)
    with open(file=f, mode=mode, encoding=encoding.value) as f_tmp:
        if head_line_mode == True:
            f_tmp.write(f"\n")
        for text in working_list:
            if line_feed_mode == 1:
                f_tmp.write(f"{text}\n")
            else:
                f_tmp.write(f"{text}")
