def split_by_top_level_def(d_working, filepath, prefix=None, preview=False):
    import logging
    import logging
    from pk_internal_tools.pk_functions.get_unique_filename import get_unique_filename
    import os.path
    import re
    from collections import defaultdict

    from pk_internal_tools.pk_objects.pk_texts import PkTexts

    from pk_internal_tools.pk_functions.get_sanitized_file_path import get_sanitized_file_path

    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    chunks = []
    chunk_names = []
    current_chunk = []
    collecting = False
    base_indent = None
    current_func_name = None
    global_chunk = []
    name_counter = defaultdict(int)

    for line in lines:
        def_match = re.match(r'^(\s*)def\s+(\w+)\(', line)
        if def_match and len(def_match.group(1)) == 0:
            if current_chunk:
                chunks.append(current_chunk)
                chunk_names.append(current_func_name or f'unknown_{len(chunks)}')
            current_func_name = get_sanitized_file_path(def_match.group(2))
            name_counter[current_func_name] += 1
            current_chunk = [line]
            collecting = True
            base_indent = None
        elif collecting:
            if base_indent is None and line.strip():
                base_indent = len(line) - len(line.lstrip())
            if line.strip() == '' or (len(line) - len(line.lstrip()) >= base_indent):
                current_chunk.append(line)
            else:
                chunks.append(current_chunk)
                chunk_names.append(current_func_name or f'unknown_{len(chunks)}')
                current_chunk = []
                collecting = False
                current_func_name = None
        else:
            if not chunks and not current_chunk:
                global_chunk.append(line)

    if current_chunk:
        chunks.append(current_chunk)
        chunk_names.append(current_func_name or f'unknown_{len(chunks)}')

    # Reset counter for consistent naming
    file_name_counter = defaultdict(int)

    if preview:
        logging.debug(f"[{PkTexts.PREVIEW_HEADER}] {os.path.basename(filepath)}")
        if global_chunk:
            logging.debug(f"[{PkTexts.SPLIT_PLAN}] global scope will be included in first chunk")

        # 중복 카운터 초기화
        duplicated_name_counter = defaultdict(int)

        for i, name in enumerate(chunk_names):
            index = i + 1
            id_prefix = f"{index:03d}" if prefix else ""
            base = f"{prefix}_{id_prefix}_{name}" if prefix else name

            duplicated_name_counter[name] += 1
            suffix = "" if duplicated_name_counter[name] == 1 else f"_DUPLICATED_{duplicated_name_counter[name] - 1}"
            filename = f"{base}{suffix}.py"

            color_start = "\033[91m" if duplicated_name_counter[name] > 1 else ""
            color_end = "\033[0m" if duplicated_name_counter[name] > 1 else ""

            logging.debug(f"{color_start}[{PkTexts.SPLIT_PLAN}] def {name}() → [{PkTexts.WILL_SAVE_AS}] {filename}{color_end}")

        logging.debug(f"[{PkTexts.PREVIEW_SUMMARY}] total={len(chunk_names)}")
        for name, count in name_counter.items():
            if count > 1:
                logging.debug(f"[{PkTexts.DUPLICATE_FUNCTION}] {name} appeared {count} times")
        logging.debug(f"[{PkTexts.PREVIEW_END}] done")
        return

    for i, (chunk, name) in enumerate(zip(chunks, chunk_names)):
        index = i + 1
        id_prefix = f"{index:03d}" if prefix else ""
        base = f"{prefix}_{id_prefix}_{name}" if prefix else name

        file_name_counter[base] += 1
        suffix = "" if file_name_counter[base] == 1 else f"_DUPLICATED_{file_name_counter[base] - 1}"
        filename = f"{base}{suffix}.py"
        filename = get_unique_filename(filename.replace('.py', ''), d_working)
        output_path = os.path.join(d_working, filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            if i == 0 and global_chunk:
                f.writelines(global_chunk)
                f.write('\n')
            f.writelines(chunk)

        logging.debug(f"[{PkTexts.WRITE_DONE}] {filename}")

    logging.debug(f"[{PkTexts.SPLIT_SUMMARY}] total={len(chunk_names)}")
    for name, count in name_counter.items():
        if count > 1:
            logging.debug(f"[{PkTexts.DUPLICATE_FUNCTION}] {name} appeared {count} times")
