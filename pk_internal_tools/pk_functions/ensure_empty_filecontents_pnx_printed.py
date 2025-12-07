def ensure_empty_filecontents_pnx_printed(
        root_dir: str,
        allowed_extensions: tuple = (".py", ".txt", ".md", ".json", ".csv"),
        max_filesize_bytes: int = 1024 * 1024  # 1MB
) -> list:
    """
    Traverse directory and return list of files with empty 'meaningful' content.

    Args:
        root_dir (str): Root directory to scan.
        allowed_extensions (tuple): File extensions to include.
        max_filesize_bytes (int): Ignore files larger than this size.

    Returns:
        list[str]: List of paths to files with no meaningful content.
    """
    import os

    empty_files = []

    for current_dir, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(current_dir, file)
            _, ext = os.path.splitext(file)
            if ext.lower() not in allowed_extensions:
                continue

            try:
                if os.path.getsize(file_path) > max_filesize_bytes:
                    continue

                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()

                stripped_lines = [line.strip() for line in lines if line.strip()]
                if not stripped_lines:
                    empty_files.append(file_path)

            except Exception:
                # 권한 문제 등은 무시
                continue

    return empty_files
