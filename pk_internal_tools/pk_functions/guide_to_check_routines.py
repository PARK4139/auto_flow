def guide_to_check_routines():
    import inspect
    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    """
    예정된 routines 수행 다하면 보상을 주는 게임을 exec 할지 묻는 함수 mkmk
    """
    # 여기서 deepcopy() 를 쓴 이유
    # 원본의 len(routines) 을 알아야 하는데
    # deepcopy 를 하지않으면 step 마다  routine: str 이 줄어든 routines: [routine] 의 len 을 참조하게 되는데
    # 이는, 의도한 초기의 routines 의 len 을 참조하는 것과 다르므로, routines_deep_copied 를 만들었다
    # 여기서는 routines 를 수행된 routine을 remove하고 routine이 remove된 routines 를 관리하는데
    # 그동안 평소 구현했던 일반적으로 리스트를 순환할때와 enumerate를 통하여 cursor 를 움직이며 동작하는 것과 달리,
    # routines: [str] 에서 routine 을 하나씩 없애도록 만들었다 .
    # step= 1, routines=[ "routine1", "routine2", "routine3" ]
    # step= 2, routines=[ "routine2", "routine3" ]
    # step= 3, routines=[ "routine3" ]
    # 큐 자료구조와 일부 비슷한 부분이 있는 구조이다.
    # 자료구조적으로는 FIFO 활용
    # cursor 는 routines[0] 만 계속 가리키게 한다. routines[0]을 수행했다면 routines 에서 routines[0](리스트의 첫 원소)를 계속 빼어 버린다.

    # routines=routines
    # routines_deep_copied=copy.deepcopy(routines)

    # ment='튜토리얼을 튜토리얼합니다'
    # speak(ment=ment)

    # ensure_slept(milliseconds=50)

    # ment: str="\n".join(routines)
    # ensure_printed_as_gui(ment=ment, auto_click_positive_btn_after_seconds=10)

    # btns=[DONE, I_WANT_TO_TO_DO_NEXT_TIME, OK_I_WILL_DO_IT_NOW]
    # routines_left: str="\n".join(routines)
    # ment=f"<남은 튜토리얼목록>\n\n{routines_left}
    # '응, 아니 지금할게'
