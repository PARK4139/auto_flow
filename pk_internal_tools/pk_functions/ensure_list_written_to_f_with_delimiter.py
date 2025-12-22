from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


def ensure_list_written_to_f_with_delimiter(working_list, f, mode, encoding=None):
    from pk_internal_tools.pk_objects.pk_encodings import PkEncoding
    from pathlib import Path
    from enum import Enum
    encoding: Enum
    encoding = encoding or PkEncoding.UTF8
    f = Path(f)
    
    # Define the delimiter
    delimiter = f"\n{PK_UNDERLINE}\n"

    with open(file=f, mode=mode, encoding=encoding.value) as f_tmp:
        # Join the list with the delimiter and write once. This is more efficient.
        content_to_write = delimiter.join(map(str, working_list))
        f_tmp.write(content_to_write)

