import logging


def pk_ensure_target_file_contents_filled_with_auto_no_option(____text_A, ____text_B, ____text_C, _____and):
    import inspect

    func_n = get_caller_name()
    foo_foo = "{{kono foo wa sekai de uituna mono ni motomo chikai desu}}"
    text_special = "{{no}}"
    text_B_cnt = ____text_A.count(____text_B)
    foo_list = []
    foo_str = ""
    foo_cmt = 0
    if ____text_C == "":
        ____text_A = ____text_A.replace(____text_B, ____text_C)
    elif text_special in ____text_C:
        logging.debug("text_A 에서 " + ____text_B + " 를 총" + str(text_B_cnt) + "개 발견하였습니다")
        foo_list = ____text_A.split(____text_B)
        if ____text_B in ____text_C:
            foo_cmt = 0
            for j in foo_list:
                if j == foo_list[-1]:
                    pass
                else:
                    foo_str = foo_str + j + ____text_C.split(text_special)[0] + str(foo_cmt)
                foo_cmt = foo_cmt + 1
            ____text_A = ""
            ____text_A = foo_str
        else:
            foo_cmt = 0
            for j in foo_list:
                if j == foo_list[-1]:
                    pass
                else:
                    foo_str = foo_str + j + ____text_C.split(text_special)[0] + str(foo_cmt)
                foo_cmt = foo_cmt + 1
            ____text_A = ""
            ____text_A = foo_str
    else:
        ____text_A = ____text_A.replace(____text_C, foo_foo)
        ____text_A = ____text_A.replace(____text_B, ____text_C)
        ____text_A = ____text_A.replace(foo_foo, ____text_B)
