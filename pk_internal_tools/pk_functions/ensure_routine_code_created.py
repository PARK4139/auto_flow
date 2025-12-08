import logging
import re
import textwrap
from pathlib import Path

from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_13_0000 import ensure_value_completed_2025_10_13_0000
from pk_internal_tools.pk_functions.get_test_file_prefix import get_test_file_prefix
from pk_internal_tools.pk_functions.get_text_cyan import get_text_cyan
from pk_internal_tools.pk_functions.get_text_from_clipboard import get_text_from_clipboard
from pk_internal_tools.pk_objects.pk_directories import d_pk_tests


# 경로 규칙 (기존 d_pk_external_tools에서 변경됨):
# - Wrapper: d_pk_wrappers (pk_external_tools/pk_wrappers/)
# - Function: D_pk_FUNCTIONS (pk_external_tools/pk_functions/)
# - System Object: D_pk_OBJECT (pk_external_tools/pk_objects/)
# - Project Root: d_pk_system (pk_system/)
# - Tests: d_pk_system/tests/ (pk_system/tests/)


def _write_template_to_file(f_template: Path, template_content: str):
    """Write template content into the given file path."""
    f_template = Path(f_template)
    f_template.write_text(template_content, encoding="utf-8")


# Function creation template
_function_creation_template = textwrap.dedent(f"""
    from pk_internal_tools.pk_functions.ensure_seconds_measured import ensure_seconds_measured
    
    @ensure_seconds_measured
    def {{func_n_to_replace}}():
        \"\"\"
            TODO: Write docstring for {{func_n_to_replace}}.
        \"\"\"
        try:
            
            return True
        except:
            from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
            import traceback
            ensure_debug_loged_verbose(traceback)
        finally:
            pass
""").lstrip("\n")

# Tests template
_tests_creation_template = textwrap.dedent(f'''
    from pk_internal_tools.pk_functions.ensure_test_log_updated import ensure_test_log_updated
    
    @ensure_test_log_updated
    def {get_test_file_prefix()}{{function_name}}():
        """
            TODO: Write docstring for {{function_name}}.
        """
        try:
            
            return True
        except:
            from pk_internal_tools.pk_functions.ensure_debug_loged_verbose import ensure_debug_loged_verbose
            import traceback
            ensure_debug_loged_verbose(traceback)
        finally:
            pass
''').lstrip("\n")

# Wrapper template (will be created AFTER function name is known)
_wrapper_creation_template = textwrap.dedent('''\
    if __name__ == "__main__":
        import traceback
        from pk_internal_tools.pk_functions.{{function_name}} import {{function_name}}
        from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
        from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
        from pk_internal_tools.pk_objects.pk_directories import d_pk_system
        from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

        ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
        try:

            {{function_name}}()

        except Exception as exception:
            ensure_exception_routine_done(traced_file=__file__,traceback=traceback, exception=exception)
        finally:
            ensure_finally_routine_done(traced_file=__file__, d_pk_system=d_pk_system)
''').lstrip("\n")


def _msg():
    from pk_internal_tools.pk_objects.pk_map_texts import PkTexts
    return PkTexts


def _ensure_unique_filename_with_dulplicated_mark(d: Path, filename: str) -> Path:
    d = Path(d)
    candidate = d / filename
    if not candidate.exists():
        return candidate
    stem, suffix = candidate.stem, candidate.suffix
    counter = 1
    while True:
        new_name = f"{stem}_DUPLICATED_{counter:03}{suffix}"
        candidate = d / new_name
        if not candidate.exists():
            return candidate
        counter += 1


def ensure_function_only_created(func_n: str) -> tuple[str, str]:
    """Create only the function file in pk_functions (and open it)."""
    pk_msg = _msg()

    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    from pk_internal_tools.pk_objects.pk_directories import D_pk_FUNCTIONS
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made

    d_working: Path = Path(D_pk_FUNCTIONS)

    text = get_text_from_clipboard()
    texts = text.split("\n")
    if 2 <= len(texts):
        options = ["ensure_", "get_", "set_", "is_", "has_", "can_"]
    else:
        options = [text, "ensure_", "get_", "set_", "is_", "has_", "can_"]

    key_name = "function_name"
    selected = ensure_value_completed_2025_10_12_0000(key_name=key_name, options=options)
    function_name = selected

    file_base_name = function_name

    extension = ".py"
    filename_with_ext = file_base_name if file_base_name.endswith(extension) else f"{file_base_name}{extension}"

    file_pnx_to_made = _ensure_unique_filename_with_dulplicated_mark(d_working, filename_with_ext)
    logging.debug(f"file_pnx_to_made={file_pnx_to_made}")
    ensure_pnx_made(pnx=str(file_pnx_to_made), mode="f")
    logging.debug(f"[{pk_msg.CREATED}] {file_pnx_to_made}")

    template_content = _function_creation_template.replace("{func_n_to_replace}", function_name)
    logging.debug("생성된 템플릿 내용:")
    logging.debug(get_text_cyan(template_content))
    _write_template_to_file(file_pnx_to_made, template_content)
    if file_pnx_to_made.exists():
        logging.debug(f"[{pk_msg.COPIED}] template copied → {file_pnx_to_made}")
        logging.debug(f'[{pk_msg.SUCCESS}] Function file created!')
        logging.debug(f'Function name={function_name}')
        logging.debug(f'file_pnx_to_made.name={file_pnx_to_made.name}')
        logging.debug(f'file_pnx_to_made={file_pnx_to_made}')

    ensure_pnx_opened_by_ext(pnx=str(file_pnx_to_made))
    return str(file_pnx_to_made), function_name


def ensure_tests_code_created(function_name: str) -> str:
    """Create tests/test_{function_name}.py and open it."""
    PkTexts = _msg()

    prefix_to_remove = "test_"
    # prefix_to_remove = "test_scenario_"
    # prefix_to_remove = "test_testcases_of_"
    if function_name.startswith(prefix_to_remove):
        function_name = function_name.removeprefix(prefix_to_remove)

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext

    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    import logging

    d_project: Path = Path(d_pk_root)
    d_tests: Path = d_pk_tests

    # 디렉토리 정보 로깅 (Path 객체를 문자열로 변환하여 로깅)
    logging.debug(f"d_pk_system: {d_pk_root}")
    logging.debug(f"d_project: {str(d_project)}")
    logging.debug(f"d_tests: {str(d_tests)}")

    # prefix = "test_"
    prefix = get_test_file_prefix()
    logging.debug(f"테스트 파일 접두사: {prefix}")

    # 테스트 디렉토리 확인 및 생성
    if not d_tests.is_dir():
        logging.debug(f"테스트 디렉토리가 존재하지 않음, 생성 시작")
        try:
            d_tests.mkdir(parents=True, exist_ok=True)
            logging.debug(f"[{PkTexts.DIRECTORY_CREATED}] {d_tests}")
        except Exception as e:
            logging.error(f"[{PkTexts.DIRECTORY_CREATION_FAILED}] {d_tests} -> {e}")
            raise
    else:
        logging.debug(f"테스트 디렉토리 이미 존재: {d_tests}")

    try:
        # 안전한 파일명 생성
        logging.debug(f"안전한 파일명 생성 시작")
        safe_name = re.sub(r"[^A-Za-z0-9_]+", "_", (function_name or "unnamed").strip())
        logging.debug(f"원본 함수명: '{function_name}' → 안전한 이름: '{safe_name}'")

        extension = ".py"
        base_filename = f"{prefix}{safe_name}{extension}"
        logging.debug(f"기본 파일명: {base_filename}")

        # 고유 파일명 생성
        f_test = _ensure_unique_filename_with_dulplicated_mark(d_tests, base_filename)
        logging.debug(f"고유 파일명: {f_test}")

        # 템플릿 내용 생성
        logging.debug(f"테스트 템플릿 내용 생성 시작")
        template_content = _tests_creation_template.replace("{function_name}", safe_name)
        logging.debug(f"템플릿 내용 길이: {len(template_content)}")

        # 파일 생성 및 템플릿 적용
        logging.debug(f"테스트 파일 생성 시작: {f_test}")
        ensure_pnx_made(pnx=str(f_test), mode="f")
        logging.debug(f"테스트 파일 생성 완료")

        _write_template_to_file(f_test, template_content)
        logging.debug(f"[{PkTexts.COPIED}] template copied → {f_test}")

        # 성공 메시지 출력
        logging.debug(f'[{PkTexts.SUCCEEDED}] Test file created!')
        logging.debug(f'Test file: {f_test.name}')
        logging.debug(f'Path: {f_test}')

        # 파일 열기
        logging.debug(f"테스트 파일 열기 시작: {f_test}")
        ensure_pnx_opened_by_ext(pnx=str(f_test))
        logging.debug(f"테스트 파일 열기 완료")

        # 결과 반환
        logging.debug(f"함수 완료 - 반환값: {str(f_test)}")
        return str(f_test)

    except Exception as e:
        logging.error(f"예외 발생: {e}")
        import traceback
        logging.error(f"스택 트레이스: {traceback.format_exc()}")
        raise


def ensure_routine_code_created_in_dir(d_working: str | Path, func_n: str) -> tuple[str, str | None]:
    PkTexts = _msg()
    from pk_internal_tools.pk_functions.get_f_historical import get_history_file_path
    from pk_internal_tools.pk_functions.save_to_history import save_to_history
    from pk_internal_tools.pk_functions.get_file_id import get_file_id
    from pk_internal_tools.pk_objects.pk_directories import D_pk_OBJECTS, D_pk_FUNCTIONS, d_pk_wrappers
    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext
    import logging
    from pathlib import Path

    # 모든 디렉토리 경로를 Path 객체로 변환
    d_wrappers = Path(d_pk_wrappers)
    d_pk_functions = Path(D_pk_FUNCTIONS)
    d_system_object = Path(D_pk_OBJECTS)
    d_working_p = Path(d_working)

    # 디렉토리 경로 정보 로깅 (Path 객체를 문자열로 변환하여 로깅)
    logging.debug(f"d_wrappers: {str(d_wrappers)}")
    logging.debug(f"d_pk_functions: {str(d_pk_functions)}")
    logging.debug(f"d_system_object: {str(d_system_object)}")
    logging.debug(f"d_working_p: {str(d_working_p)}")

    if not d_working_p.is_dir():
        logging.warning(f"[{PkTexts.PATH_NOT_FOUND}] {d_working_p}")

    editable = False
    value = None

    try:
        # 디렉토리별 처리 로직
        if d_working_p == d_wrappers:
            logging.debug(f"WRAPPERS 디렉토리 처리 시작")
            key_name = 'pk_python_file_name'
            file_id = get_file_id(key_name, func_n)
            logging.debug(f"key_name: {key_name}, file_id: {file_id}")

            init_options = ["ensure_"]
            logging.debug(f"init_options: {init_options}")

            selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=init_options, editable=editable)
            value = selected

            save_to_history(value, history_file=get_history_file_path(file_id=file_id))
            logging.debug(f"히스토리에 저장됨")

        elif d_working_p == d_pk_functions:
            logging.debug(f"pk_FUNCTIONS 디렉토리 처리 시작")
            key_name = 'pk_python_file_name'
            file_id = get_file_id(key_name, func_n)
            logging.debug(f"key_name: {key_name}, file_id: {file_id}")

            init_options = ["ensure_"]
            logging.debug(f"init_options: {init_options}")

            selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=init_options, editable=editable)
            value = selected

        elif d_working_p == d_system_object:
            logging.debug(f"SYSTEM_OBJECT 디렉토리 처리 시작")
            key_name = 'python_system_object_file_name'
            file_id = get_file_id(key_name, func_n)
            logging.debug(f"key_name: {key_name}, file_id: {file_id}")

            init_options = []
            logging.debug(f"init_options: {init_options}")

            selected = ensure_value_completed_2025_10_13_0000(key_name=key_name, func_n=func_n, options=init_options, editable=editable)
            value = selected


        else:
            logging.warning(f"[{PkTexts.SKIPPED}] Unknown working dir: {d_working_p}")
            return None, None

        # 파일명 생성 과정 로깅
        logging.debug(f"선택된 값: {value}")
        f_n = (value or "").strip()
        logging.debug(f"정리된 값: '{f_n}'")

        extension = ".py"
        filename_with_ext = f_n if f_n.endswith(extension) else f"{f_n}{extension}"
        file_name = filename_with_ext
        logging.debug(f"최종 파일명: {file_name}")
        logging.debug(f'file_name={file_name}')

        # 고유 파일명 생성
        file_pnx_to_made = _ensure_unique_filename_with_dulplicated_mark(d_working_p, file_name)
        logging.debug(f"file_pnx_to_made={file_pnx_to_made}")

        produced_function_name = None

        # 파일 생성
        logging.debug(f"파일 생성 시작: {file_pnx_to_made}")
        ensure_pnx_made(pnx=str(file_pnx_to_made), mode="f")
        logging.debug(f"[{PkTexts.CREATED}] {file_pnx_to_made}")

        # 디렉토리별 템플릿 적용
        if d_working_p == d_wrappers:
            logging.debug(f"래퍼 템플릿 적용 시작")
            # Wrapper 파일 생성 (pk_wrappers 디렉토리)
            # This _in_dir variant will NOT insert the function name into wrapper.
            # The name-aware wrapper is created by ensure_wrapper_created_with_function_name().
            _write_template_to_file(file_pnx_to_made, _wrapper_creation_template)
            logging.debug(f"[{PkTexts.COPIED}] wrapper template copied → {file_pnx_to_made}")

        elif d_working_p == d_pk_functions:
            logging.debug(f"함수 템플릿 적용 시작")
            # Function 파일 생성 (pk_functions 디렉토리)
            func_n_template = f_n[:-3] if f_n.endswith(extension) else f_n
            produced_function_name = func_n_template
            logging.debug(f"함수명: {produced_function_name}")

            template_content = _function_creation_template.replace("{func_n_to_replace}", func_n_template)
            logging.debug(f"템플릿 내용 길이: {len(template_content)}")
            logging.debug(f'template_content={template_content}')

            _write_template_to_file(file_pnx_to_made, template_content)
            logging.debug(f"[{PkTexts.COPIED}] function template copied → {file_pnx_to_made}")

        elif d_working_p == d_system_object:
            logging.debug(f"시스템 객체 템플릿 적용 시작")
            # System Object 파일 생성 (pk_objects 디렉토리)
            _write_template_to_file(file_pnx_to_made, "class ")
            logging.debug(f"[{PkTexts.COPIED}] system_object template copied → {file_pnx_to_made}")

        # 파일 열기
        logging.debug(f"파일 열기 시작: {file_pnx_to_made}")
        ensure_pnx_opened_by_ext(pnx=str(file_pnx_to_made))
        logging.debug(f"파일 열기 완료")

        # 결과 반환
        logging.debug(f"함수 완료 - 반환값: ({str(file_pnx_to_made)}, {produced_function_name})")
        return str(file_pnx_to_made), produced_function_name

    except Exception as e:
        logging.error(f"예외 발생: {e}")
        import traceback
        logging.error(f"스택 트레이스: {traceback.format_exc()}")
        raise


def ensure_wrapper_created(function_name: str) -> str:
    """
    Create wrapper in d_pk_wrappers (기존 d_pk_external_tools에서 변경됨)
    with {{function_name}} already replaced, then open it.
    """
    PkTexts = _msg()

    from pk_internal_tools.pk_functions.ensure_pnx_made import ensure_pnx_made
    from pk_internal_tools.pk_functions.ensure_pnx_opened_by_ext import ensure_pnx_opened_by_ext

    from pk_internal_tools.pk_objects.pk_directories import d_pk_wrappers
    from pk_internal_tools.pk_objects.pk_not_organized import pk_
    import logging

    prefix = pk_
    d_working: Path = Path(d_pk_wrappers)

    # 디렉토리 정보 로깅 (Path 객체를 문자열로 변환하여 로깅)
    logging.debug(f"d_pk_wrappers: {d_pk_wrappers}")
    logging.debug(f"d_working: {str(d_working)}")
    logging.debug(f"prefix: {prefix}")

    filename_with_ext = f"{prefix}{function_name}.py"
    logging.debug(f"기본 파일명: {filename_with_ext}")

    file_pnx_to_made = _ensure_unique_filename_with_dulplicated_mark(d_working, filename_with_ext)
    logging.debug(f"고유 파일명: {file_pnx_to_made}")

    try:
        # 파일 생성
        logging.debug(f"파일 생성 시작: {file_pnx_to_made}")
        ensure_pnx_made(pnx=str(file_pnx_to_made), mode="f")
        logging.debug(f"[{PkTexts.CREATED}] {file_pnx_to_made}")

        # 템플릿 내용 생성 및 적용
        logging.debug(f"템플릿 내용 생성 시작")
        template_content = _wrapper_creation_template.replace("{{function_name}}", function_name)
        logging.debug(f"템플릿 내용 길이: {len(template_content)}")

        _write_template_to_file(file_pnx_to_made, template_content)
        logging.debug(f"[{PkTexts.COPIED}] wrapper template copied → {file_pnx_to_made}")

        # 파일 열기
        logging.debug(f"파일 열기 시작: {file_pnx_to_made}")
        ensure_pnx_opened_by_ext(pnx=str(file_pnx_to_made))
        logging.debug(f"파일 열기 완료")

        # 결과 반환
        logging.debug(f"함수 완료 - 반환값: {str(file_pnx_to_made)}")
        return str(file_pnx_to_made)

    except Exception as e:
        logging.error(f"예외 발생: {e}")
        import traceback
        logging.error(f"스택 트레이스: {traceback.format_exc()}")
        raise


def ensure_routine_code_created_once():
    from pk_internal_tools.pk_objects.pk_directories import D_pk_FUNCTIONS, D_pk_OBJECTS
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept
    from pk_internal_tools.pk_functions.ensure_value_completed_2025_10_12_0000 import ensure_value_completed_2025_10_12_0000
    import logging
    from pathlib import Path

    # 함수명 가져오기
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()

    # 함수 시작 로깅
    logging.debug(f"시작")
    logging.debug(f"호출자: {func_n}")

    # 사용 가능한 모드 목록 (문자열만 포함)
    available_modes = [
        "FUNCTION_ONLY",
        "WRAPPER_ONLY",
        "SYSTEM_OBJECT",
        "TEST_ONLY",
        "WRAPPER_AND_FUNCTION_TEST_CODE",
    ]
    logging.debug(f"모드: {available_modes}")

    # 모드 선택 과정 로깅
    logging.debug(f"모드 선택...")
    # available_modes는 이미 문자열 리스트이므로 안전함
    mode = ensure_value_completed_2025_10_12_0000(key_name='mode', options=available_modes)
    logging.debug(f"선택: {mode}")

    # 모드 검증
    if mode not in available_modes:
        logging.error(f"잘못된 모드: {mode}")
        logging.debug(f"사용 가능한 모드: {available_modes}")
        raise ValueError(f"잘못된 모드: {mode}. 사용 가능한 모드: {available_modes}")

    logging.debug(f"모드 검증 완료: {mode}")

    # 디렉토리 경로를 Path 객체로 변환
    d_functions_split = Path(D_pk_FUNCTIONS)
    d_system_object = Path(D_pk_OBJECTS)

    # 디렉토리 경로 정보 로깅 (Path 객체를 문자열로 변환하여 로깅)
    logging.debug(f"pk_FUNCTIONS: {str(d_functions_split)}")
    logging.debug(f"SYSTEM_OBJECT: {str(d_system_object)}")

    try:
        if mode == "WRAPPER_AND_FUNCTION_TEST_CODE":
            logging.info(f"WRAPPER_AND_FUNCTION_TEST_CODE 실행")

            # 1단계: 함수 파일 생성
            logging.debug(f"1단계: 함수 파일 생성")
            _func_file, wrapper_file_name = ensure_routine_code_created_in_dir(d_functions_split, func_n)
            logging.debug(f"결과: {_func_file}, 함수명: {wrapper_file_name}")
            ensure_slept(milliseconds=77)
            logging.debug(f"대기 완료")

            if wrapper_file_name:
                logging.debug(f"2단계: 래퍼 생성")
                if wrapper_file_name.startswith("pk_"):
                    wrapper_file_name = wrapper_file_name.removeprefix("pk_")
                wrapper_file = ensure_wrapper_created(wrapper_file_name)
                logging.debug(f"래퍼 완료: {wrapper_file}")
                ensure_slept(milliseconds=77)
                logging.debug(f"대기 완료")

                # logging.debug(f"3단계: 테스트 코드 생성")
                # test_file = ensure_tests_code_created(wrapper_file_name)
                # logging.debug(f"테스트 완료: {test_file}")
                logging.info(f"WRAPPER_AND_FUNCTION_TEST_CODE 완료")
            else:
                logging.warning(f"함수명 없음 - 래퍼/테스트 건너뜀")

        elif mode == "SYSTEM_OBJECT":
            logging.info(f"SYSTEM_OBJECT 실행")
            result = ensure_routine_code_created_in_dir(d_system_object, func_n)
            logging.debug(f"결과: {result}")

        elif mode == "FUNCTION_ONLY":
            logging.info(f"FUNCTION_ONLY 실행")
            _file_created, _function_name = ensure_function_only_created(func_n)
            logging.debug(f"결과: 파일={_file_created}, 함수명={_function_name}")

        elif mode == "WRAPPER_ONLY":
            logging.info(f"WRAPPER_ONLY 실행")
            logging.debug(f"함수명 입력 대기...")
            wrapper_file_name = input("wrapper_file_name=")
            if wrapper_file_name.startswith("pk_"):
                wrapper_file_name = wrapper_file_name.removeprefix("pk_")
            logging.debug(f"입력: {wrapper_file_name}")

            if wrapper_file_name:
                logging.debug(f"래퍼 생성")
                wrapper_file = ensure_wrapper_created(wrapper_file_name)
                logging.debug(f"래퍼 완료: {wrapper_file}")
            else:
                logging.warning(f"함수명 없음 - 래퍼 건너뜀")

        elif mode == "TEST_ONLY":
            logging.info(f"TEST_ONLY 실행")

            logging.debug(f"80ms 대기")
            ensure_slept(milliseconds=77)
            logging.debug(f"대기 완료")

            logging.debug(f"함수명 입력 대기...")
            wrapper_file_name = input("wrapper_file_name=")
            logging.debug(f"입력: {wrapper_file_name}")

            if wrapper_file_name:
                logging.debug(f"테스트 생성")
                test_file = ensure_tests_code_created(wrapper_file_name)
                logging.debug(f"테스트 완료: {test_file}")
            else:
                logging.warning(f"함수명 없음 - 테스트 건너뜀")

        else:
            logging.error(f"알 수 없는 모드: {mode}")
            logging.debug(f"사용 가능: {available_modes}")

    except Exception as e:
        logging.error(f"예외: {e}")
        import traceback
        logging.error(f"스택: {traceback.format_exc()}")
        raise

    # 함수 종료 로깅
    logging.debug(f"종료 - 모드: {mode}")


def ensure_routine_code_created():
    from pk_internal_tools.pk_functions.ensure_slept import ensure_slept

    while True:
        ensure_routine_code_created_once()
        ensure_slept(milliseconds=100)
