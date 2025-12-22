def get_sanitized_file_path(name):
    import re
    return re.sub(r'[^a-zA-Z0-9_]', '_', name)
