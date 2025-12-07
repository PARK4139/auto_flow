def get_extensions_from_d(dir_path: str) -> set[str]:
    import os
    extensions = set()
    if not os.path.isdir(dir_path):
        return extensions
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(filename)
            if ext:
                extensions.add(ext)
    return extensions
