import textwrap

if __name__ == "__main__":
    import traceback
    from pk_internal_tools.pk_functions.ensure_answered_via_chatgpt import ensure_answered_via_chatgpt
    from pk_internal_tools.pk_functions.ensure_exception_routine_done import ensure_exception_routine_done
    from pk_internal_tools.pk_functions.ensure_finally_routine_done import ensure_finally_routine_done
    from pk_internal_tools.pk_objects.pk_directories import d_pk_root
    from pk_internal_tools.pk_functions.ensure_pk_starting_routine_done import ensure_pk_starting_routine_done

    ensure_pk_starting_routine_done(traced_file=__file__, traceback=traceback)
    try:

        question = textwrap.dedent(rf'''
            지금까지 대화한내용인 prompts_new/prompts.history 숙지요청

            각 모듈은 파일 단위 관리요청

            테스트는 내가수행할게. 이 점 기억요청

            테스트결과 로그 logs/pk_system.log 확인요청, 논리적으로 이상한 부분 수정제안 요청

            테스트결과 로그 logs/pk_system.log 확인요청, ensure_slept 가 18분 정도가 진행이 되던데 그 원인 분석

            분석결과대로 코드 수정요청

            ensure_pk_scenario_executed(__file__) 함수를 실행해서 시나리오를 테스트요청

            해당 내용 .cursor/rules,  GEMINI.md 에 규칙추가 요청

            지금까지 대화한내용을 prompts_new/prompts.history 에 프롬프트 작성요청
            지금까지 대화한내용을 prompts_new/prompts.history 에 프롬프트 최신내용으로 업데이트요청

            계속 진행요청
        ''').strip()


        # question = textwrap.dedent(rf'''
        #     TODO STT
        # ''').strip()
        ensure_answered_via_chatgpt(prompt=question)

    except Exception as exception:
        ensure_exception_routine_done(traced_file=__file__, traceback=traceback, exception=exception)
    finally:
        ensure_finally_routine_done(traced_file=__file__, d_pk_root=d_pk_root)
