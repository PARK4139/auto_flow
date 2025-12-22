from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
from pk_internal_tools.pk_objects.pk_texts import PK_UNDERLINE


@ensure_seconds_measured
def get_last_selected(history_file):
    import os

    # The delimiter must be exactly the same as in ensure_list_written_to_f.py
    delimiter = f"\n{PK_UNDERLINE}\n"

    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Split the content by the delimiter to get all entries
            entries = content.split(delimiter)
            # The first entry is the most recent one
            if entries:
                return entries[0].strip()
    
    # Return an empty string if the file doesn't exist or is empty
    return ""
