from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_target_file_name_and_file_texts_replaced(f_target, old_text, new_text, operation_mode):
    import traceback
    try:
        import os

        from pk_internal_tools.pk_functions.get_nx import get_nx
        from pk_internal_tools.pk_functions.get_p import get_p
        from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
        from pk_internal_tools.pk_objects.pk_modes import PkModesForEnsureTargetFilenameAndFileContentTextReplaced

        modified = False

        # file content text
        if operation_mode in [PkModesForEnsureTargetFilenameAndFileContentTextReplaced.ONLY_FILE_CONTENT_TEXT, PkModesForEnsureTargetFilenameAndFileContentTextReplaced.FILENAME_AND_FILECONTENT]:
            try:
                with open(f_target, "r", encoding="utf-8") as f:
                    content = f.read()
            except UnicodeDecodeError:
                # print(f"[SKIP] 바이너리 파일로 판단: {f_target}")
                pass
                return
            if old_text in content:
                new_content = content.replace(old_text, new_text)
                with open(f_target, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"[FILE CONTENT MODIFIED] {f_target}")
                modified = True

        # file name
        if operation_mode in [PkModesForEnsureTargetFilenameAndFileContentTextReplaced.ONLY_FILENAME, PkModesForEnsureTargetFilenameAndFileContentTextReplaced.FILENAME_AND_FILECONTENT]:
            file_name = get_nx(f_target)
            root = get_p(f_target)
            if old_text in file_name:
                new_file_name = file_name.replace(old_text, new_text)
                new_path = os.path.join(root, new_file_name)
                if os.path.exists(new_path):
                    # print(f"[FILE RENAMING SKIPPED] Target already exists: {new_path}")
                    pass
                else:
                    try:
                        os.rename(f_target, new_path)
                        print(f"[FILE RENAMED] {f_target} → {new_path}")
                    except FileExistsError:
                        # print(f"FileExistsError despite pre-check: {new_path}")
                        traceback.print_exc()
                        pass
                modified = True

        if not modified:
            # print(f"[SKIP] 변경 없음: {file_path_old}") # pk_option
            pass
        return True
    except Exception as e:
        traceback.print_exc()
    finally:
        pass
