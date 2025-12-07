import re
import logging

def ensure_clipboard_value_sanitized(value: str) -> str:
    """
    Cleans a string retrieved from the clipboard by removing quotes and fzf hash prefixes.
    """
    if not isinstance(value, str):
        return ""

    # 1. Strip whitespace
    cleaned_value = value.strip()
    
    # 2. Remove surrounding quotes (single or double)
    if (cleaned_value.startswith('"') and cleaned_value.endswith('"')) or \
       (cleaned_value.startswith("'" ) and cleaned_value.endswith("'" )):
        cleaned_value = cleaned_value[1:-1]

    # 3. Remove "[hash]" prefix, which might be present after quote removal
    # The original get_str_removed_bracket_hashed_prefix can be used here,
    # but we replicate the logic for clarity and self-containment.
    cleaned_value = re.sub(r'^[[a-f0-9]+]\]\s*', '', cleaned_value).strip()
    
    logging.debug(f"Sanitized clipboard value: '{value}' -> '{cleaned_value}'")
    return cleaned_value
