import logging


if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_gemini_cli_executed_advanced import ensure_gemini_cli_executed_advanced

    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        # ensure_gemini_cli_executed_advanced()
        res = ensure_gemini_cli_executed_advanced(
            diff_source="git",
            save_dir="D:/tmp/patches",
            debug=True,
            keep_temps=True,  # temp 파일 보존
            validate_patch=True,  # 적용 전 체크
            dry_run=False,  # 실제 적용
        )

        # BEFORE (에러)
        # logging.debug(res["ok"], res["applied"], res["rej_hints"])
        # logging.debug("patch:", res["patch_path"])

        # AFTER (둘 중 편한 방식 사용)
        logging.debug("ok=%s applied=%s rej=%s", res["ok"], res["applied"], res["rej_hints"])
        logging.debug("patch=%s", res["patch_path"])
        # 또는
        # logging.debug(f"ok={res['ok']} applied={res['applied']} rej={res['rej_hints']}")
        # logging.debug(f"patch={res['patch_path']}")

        # 단계 로그
        for s in res["steps"][-5:]:
            logging.debug(s)
        # 다이어그
        logging.debug(res["diagnostics"]["env"])
        logging.debug(res["diagnostics"]["patch_head"])

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
