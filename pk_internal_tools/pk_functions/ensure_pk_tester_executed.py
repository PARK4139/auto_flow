from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured


@ensure_seconds_measured
def ensure_pk_tester_executed(pk_tester_instance):
    """
        TODO: Write docstring for ensure_pk_tester_executed.
    """
    import logging

    from pk_internal_tools.pk_functions.ensure_values_completed import ensure_values_completed
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    from pk_internal_tools.pk_objects.pk_directories import D_PK_ROOT, D_PK_TESTS  # D_PK_TESTS for test file discovery

    try:
        func_n = get_caller_name()

        # Initialize PkTester
        # Create a temporary root path for PkTester for its dummy operations.
        # In this context, PkTester is used to *discover* tests, not create files.
        # So, its root_path might not be strictly needed for this specific use case,

        # 1. Discover test files
        # Assuming D_PK_TESTS is the directory containing tests
        test_files = pk_tester_instance.get_test_files(D_PK_TESTS)

        if not test_files:
            logging.warning("테스트 파일을 찾을 수 없습니다. 'pk_tests/' 디렉토리에 'test_*.py' 형식의 파일이 있는지 확인하십시오.")
            exit(1)  # Exit with an error code

        # Prepare options for FZF
        fzf_options = [str(f.relative_to(D_PK_ROOT)) for f in test_files]  # Display relative paths
        fzf_option_map = {str(f.relative_to(D_PK_ROOT)): f for f in test_files}  # Map back to full paths

        # 2. Allow multi-select of tests via FZF
        selected_display_paths = ensure_values_completed(
            key_name="테스트할 파일 선택",
            func_n=func_n,
            options=fzf_options,
            guide_text="테스트할 Python 파일을 선택하세요 (Tab: 다중 선택, Alt+A: 전체 선택, Enter: 완료):",
            
        )

        if not selected_display_paths:
            logging.info("선택된 테스트 파일이 없습니다. 작업을 종료합니다.")
            exit(0)  # Exit gracefully

        selected_test_file_paths = [fzf_option_map[dp] for dp in selected_display_paths]

        # 3. Prompt for view mode (simple/detailed)
        view_mode_options = ["simple", "detailed"]
        selected_view_mode = ensure_values_completed(
            key_name="테스트 결과 보기 모드 선택",
            func_n=func_n,
            options=view_mode_options,
            guide_text="테스트 결과 표시 모드를 선택하세요:",
            multi_select=False  # Single select for view mode
        )
        if not selected_view_mode:
            logging.info("보기 모드 선택이 취소되었습니다. 작업을 종료합니다.")
            exit(0)  # Exit gracefully

        # 4. Run selected tests
        # The run_selected_tests method in PkTester will execute and capture results
        test_results = pk_tester_instance.run_selected_tests(selected_test_file_paths, verbose=True)  # Assuming verbose for now

        # 5. Display results
        pk_tester_instance.display_results(test_results, view_mode=selected_view_mode)
        return True
    except Exception as e:
        from pk_internal_tools.pk_functions.ensure_debugged_verbose import ensure_debugged_verbose
        import traceback
        ensure_debugged_verbose(traceback, e)
    finally:
        pass