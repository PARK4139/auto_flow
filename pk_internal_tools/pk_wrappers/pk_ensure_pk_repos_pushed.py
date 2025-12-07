from pk_internal_tools.pk_functions.ensure_console_paused import ensure_console_paused

if __name__ == "__main__":
    try:
        import logging
        import traceback

        # from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed  # 사용되지 않음
        from pk_internal_tools.pk_functions.get_caller_name import get_caller_name

        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_functions.ensure_git_repo_pushed import ensure_git_repo_pushed
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
        from pk_internal_tools.pk_functions.ensure_pk_wrapper_starter_suicided import ensure_pk_wrapper_starter_suicided
        from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken


        from pk_internal_tools.pk_objects.pk_qc_mode import QC_MODE
        from pk_internal_tools.pk_objects.pk_directories import D_AUTO_FLOW_REPO
        from pk_internal_tools.pk_objects.pk_directories import d_pk_root

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)


        func_n = get_caller_name()
        # TODO:  multi_selet 이렇게 하는거 아닌가?
        # d_local_repo_options = [
        #     # D_PK_MEMO_REPO,
        #     D_AUTO_FLOW_REPO,
        #     d_pk_system,
        # ]
        # d_local_repos = ensure_values_completed(
        #     key_name="d_local_repos",
        #     options=d_local_repo_options,
        #     func_n=func_n,
        #     multi_select=True,
        #     guide_text="등록할 doskey를 멀티 선택하세요 (Tab으로 선택, Enter로 완료):",
        # )

        d_local_repos = [
            # D_PK_MEMO_REPO,
            D_AUTO_FLOW_REPO,
            d_pk_root,
        ]
        # 레포지토리 개수 확인 및 사용자 확인 질의
        repo_count = len(d_local_repos)
        if repo_count > 0:
            from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
            from pk_internal_tools.pk_objects.pk_texts import PkTexts
            from pk_internal_tools.pk_functions.get_nx import get_nx

            # 레포지토리 목록 표시
            repo_names = [get_nx(repo) for repo in d_local_repos]
            repo_list_text = ", ".join(repo_names)

            question = f"{repo_count}개의 레포지토리를 푸시하시겠습니까? ({repo_list_text})"
            logging.info(question)

            if QC_MODE:
                # QC_MODE 모드에서는 자동으로 YES 선택 (또는 사용자 입력)
                ok = ensure_value_completed_2025_10_12_0000(
                    key_name=question,
                    options=[PkTexts.YES, PkTexts.NO]
                )
            else:
                ok = ensure_value_completed_2025_10_12_0000(
                    key_name=question,
                    options=[PkTexts.YES, PkTexts.NO]
                )

            if ok != PkTexts.YES:
                logging.info("사용자가 푸시를 취소했습니다.")
                ensure_pk_wrapper_starter_suicided(__file__)
                exit(0)

        state = None
        for d_local_repo in d_local_repos:
            state = ensure_git_repo_pushed(d_local_repo=d_local_repo, ai_commit_massage_mode=False)
            # input("continue:enter")

        if state and state.get("state") == True:
            if QC_MODE:
                logging.debug("푸쉬 성공")
            else:
                ensure_spoken("푸쉬 성공")
            logging.debug(f'''state={state} ''')
            ensure_spoken(f'', wait=True)
            ensure_pk_wrapper_starter_suicided(__file__)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
