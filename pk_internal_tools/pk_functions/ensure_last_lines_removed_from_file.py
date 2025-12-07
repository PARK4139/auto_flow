def ensure_last_lines_removed_from_file(file: str, lines_to_remove_from_end: int = 48) -> None:
    # TODO : 동작학때마다 VSCODE 빨간줄 생김,
    lines_to_remove_from_end  = int(lines_to_remove_from_end)

    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 끝에서 num_lines 줄 제거
    new_lines = lines[:-lines_to_remove_from_end] if len(lines) > lines_to_remove_from_end else []

    with open(file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
