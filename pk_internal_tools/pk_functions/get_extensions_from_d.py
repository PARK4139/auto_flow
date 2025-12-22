def get_extensions_from_d(dir_path: str) -> set[str]:
    import os
    extensions = set()
    if not os.path.isdir(dir_path):
        return extensions
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file_name)
            if ext:
                extensions.add(ext)
    return extensions
