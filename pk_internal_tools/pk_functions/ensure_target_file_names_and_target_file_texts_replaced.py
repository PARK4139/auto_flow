def ensure_target_file_names_and_target_file_texts_replaced(d_target, old_text, new_text, target_extensions, ignored_directory_names, operation_mode):
    import os
    from pathlib import Path

    from pk_internal_tools.pk_functions.ensure_target_file_name_and_file_texts_replaced import ensure_target_file_name_and_file_texts_replaced

    d_target = os.path.abspath(d_target)
    d_target = Path(d_target)
    d_target = str(d_target)
    # print(f'''d_target={d_target} ''')
    if not os.path.isdir(d_target):
        print(f"디렉토리 없음: {d_target}")
        return
    for root, dirs, files in os.walk(d_target):
        for file_name in files:
            if not any(file_name.lower().endswith(ext) for ext in target_extensions):
                continue
            file_path_old = os.path.join(root, file_name)
            ignored_detected = False
            for ignored_directory_name in ignored_directory_names:
                if ignored_directory_name in file_path_old:
                    ignored_detected = True
                    print(f"[SKIP] ignored_directory_names 중 {ignored_directory_name} 감지 in {file_path_old}")
                    continue
            if ignored_detected == True:
                continue

            ensure_target_file_name_and_file_texts_replaced(f_target=file_path_old, old_text=old_text, new_text=new_text, operation_mode=operation_mode)
