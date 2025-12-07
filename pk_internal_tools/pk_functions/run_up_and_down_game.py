from pk_internal_tools.pk_functions.ensure_spoken import ensure_spoken
from pk_internal_tools.pk_functions.is_user_input_required import is_user_input_required
from pk_internal_tools.pk_objects.pk_gui import ask_user


def run_up_and_down_game():
    import random

    from pk_internal_tools.pk_functions.get_caller_name import get_caller_name
    func_n = get_caller_name()
    correct_answer: int = random.randint(1, 100)
    left_oportunity: int = 10
    ment = f"<UP AND DOWN GAME>\n\nFIND CORRECT NUMBER"
    ensure_spoken(text=ment)

    txt_clicked, function, txt_written = ask_user(
        text=ment,
        buttons=["START", "EXIT"],
        function=None,
        auto_click_negative_btn_after_milliseconds=30000,
        title=f"{func_n}()",
        input_box_mode=False,
    )
    if txt_clicked != "START":
        return

    user_input = None
    is_game_strated = False
    btn_txt_clicked = txt_clicked

    if btn_txt_clicked == "START":
        ment = f"START IS PRESSED, LETS START GAME"
        ensure_spoken(text=ment)
        while left_oportunity >= 0:
            if left_oportunity == 0:
                ment = f"LEFT CHANCE IS {left_oportunity} \nTAKE YOUR NEXT CHANCE."
                ensure_spoken(text=ment)

                txt_clicked, function, txt_written = ask_user(
                    text=ment,
                    buttons=["EXIT"],
                    function=None,
                    auto_click_negative_btn_after_milliseconds=None,
                    title=f"{func_n}()",
                    #                    input_box_mode=True,
                )
                if txt_clicked == "EXIT":
                    return

                break
            elif is_game_strated == False or user_input is None:

                ment = f"TYPE NUMBER BETWEEN 1 TO 100"
                if user_input is None:
                    ment = rf"{ment} AGAIN"
                ensure_spoken(text=ment)
                txt_clicked, function, txt_written = ask_user(
                    text=ment,
                    buttons=["SUBMIT", "EXIT"],
                    function=None,
                    auto_click_negative_btn_after_milliseconds=None,
                    title=f"{func_n}()",
                    input_box_mode=True,
                )
                if txt_clicked == "EXIT":
                    return

                user_input = is_user_input_required(txt_written)
                if user_input is not None:
                    left_oportunity = left_oportunity - 1
                is_game_strated = True
            elif user_input == correct_answer:
                ment = f"CONGRATULATIONS\n\nYOUR NUMBER IS {correct_answer}\nTHIS IS ANSWER\n\nSEE YOU AGAIN"
                ensure_spoken(text=ment)

                txt_clicked, function, txt_written = ask_user(
                    text=ment,
                    buttons=["SUBMIT", "EXIT"],
                    function=None,
                    auto_click_negative_btn_after_milliseconds=None,
                    title=f"{func_n}()",
                    input_box_mode=True,
                )
                if txt_clicked == "EXIT":
                    return

            elif correct_answer < user_input:
                ment = f"YOUR NUMBER IS {user_input}\n\nYOU NEED DOWN\n\nYOUR LEFT CHANCE IS {left_oportunity}"
                ensure_spoken(text=ment)

                txt_clicked, function, txt_written = ask_user(
                    text=ment,
                    buttons=["SUBMIT", "EXIT"],
                    function=None,
                    auto_click_negative_btn_after_milliseconds=None,
                    title=f"{func_n}()",
                    input_box_mode=True,
                )
                if txt_clicked == "EXIT":
                    return

                user_input = is_user_input_required(txt_written)
                if user_input is not None:
                    left_oportunity = left_oportunity - 1
            elif correct_answer > user_input:
                ment = f"YOUR NUMBER IS {user_input}\n\nYOU NEED UP\n\nYOUR LEFT CHANCE IS {left_oportunity}"
                ensure_spoken(text=ment)

                txt_clicked, function, txt_written = ask_user(
                    text=ment,
                    buttons=["SUBMIT", "EXIT"],
                    function=None,
                    auto_click_negative_btn_after_milliseconds=None,
                    title=f"{func_n}()",
                    input_box_mode=True,
                )
                if txt_clicked == "EXIT":
                    return

                user_input = is_user_input_required(txt_written)
                if user_input is not None:
                    left_oportunity = left_oportunity - 1
    else:
        return
