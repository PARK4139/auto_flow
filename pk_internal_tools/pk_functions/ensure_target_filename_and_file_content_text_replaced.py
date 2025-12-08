from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured

@ensure_seconds_measured
def ensure_target_filename_and_file_content_text_replaced(f_target, old_text, new_text, operation_mode):
    try:
        import os
        import traceback

        from pk_internal_tools.pk_functions.get_nx import get_nx
        from pk_internal_tools.pk_functions.get_p import get_p
        from pk_internal_tools.pk_objects.pk_system_operation_options import SetupOpsForPnxReplacement

        modified = False

        # 파일 내용 수정
        if operation_mode in [SetupOpsForPnxReplacement.FILE_CONTENTS_ONLY, SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
            try:
                with open(f_target, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                print(f"[SKIP] 바이너리 파일로 판단: {f_target}")
                return
            if old_text in content:
                new_content = content.replace(old_text, new_text)
                with open(f_target, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[FILE CONTENT MODIFIED] {f_target}")
                modified = True

        # 파일명 변경
        if operation_mode in [SetupOpsForPnxReplacement.FILE_NAMES_ONLY, SetupOpsForPnxReplacement.FILE_NAMES_AND_CONTENTS_ONLY]:
            filename = get_nx(f_target)
            root = get_p(f_target)
            if old_text in filename:
                new_filename = filename.replace(old_text, new_text)
                new_path = os.path.join(root, new_filename)
                if os.path.exists(new_path):
                    print(f"[SKIP RENAME] Target already exists: {new_path}")
                else:
                    try:
                        os.rename(f_target, new_path)
                        print(f"[FILE RENAMED] {f_target} → {new_path}")
                    except FileExistsError:
                        print(f"FileExistsError despite pre-check: {new_path}")
                        traceback.print_exc()
                modified = True

        if not modified:
            # print(f"[SKIP] 변경 없음: {file_path_old}") # pk_option
            pass
        return True
    except:
        # from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
        # import traceback
        # ensure_debug_loged_verbose(traceback)
        traceback.print_exc()
    finally:
        pass
