def 강의준비하다(__file__):
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done
    import traceback
    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)


def 화면출력하다(text):
    print(text)


def 말하다(text):
    from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
    ensure_spoken(text)
    print(text)


def 멈추고_계속진행여부_묻고_튜토리얼():
    keep_going_guide_msg = f"계속 진행하려면 엔터를 눌러주세요"
    말하다(keep_going_guide_msg)
    input(keep_going_guide_msg)


def _divide_contents(text):
    _line_spliter = "================="
    화면출력하다(f"{_line_spliter} {text} {_line_spliter} ")



# def _print_step():
#     TODO
# step # lecture_state.toml 에 저장
# total_step # lecture_state.toml 에 저장
# step = get_step_from_lecture_state_toml()
# total_step = get_total_step_from_lecture_state_toml()
# print(rf"[{step}/{total_step}]")
# pass
