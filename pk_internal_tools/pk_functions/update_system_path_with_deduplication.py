def update_system_path_with_deduplication(additional_path: str = None):
    import os

    current_path = os.environ.get("PATH", "")
    path_list = current_path.split(";")

    seen = set()
    cleaned_paths = []

    for path in path_list:
        path = path.strip()
        if path and path.lower() not in seen:
            seen.add(path.lower())
            cleaned_paths.append(path)

    if additional_path:
        ap = additional_path.strip()
        if ap and ap.lower() not in seen:
            cleaned_paths.append(ap)

    final_path = ";".join(cleaned_paths)

    if len(final_path) > 1024:
        print("PATH too long! setx may truncate it.")

    os.system(f'setx PATH "{final_path}"')
    print("PATH updated with deduplication.")


