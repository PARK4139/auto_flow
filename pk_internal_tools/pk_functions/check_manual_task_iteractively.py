def check_manual_task_iteractively(question, ignore_uppercase_word_list=None):
    try:

        from colorama import init as pk_colorama_init

        import traceback

        import sys

        ensure_pk_colorama_initialized_once()

        if ignore_uppercase_word_list is None:
            ignore_uppercase_word_list = []

        question = question.upper()

        for word in ignore_uppercase_word_list:
            question = question.replace(word.upper(), word)

        # [OPTION]
        # line_feed_cnt = 6
        line_feed_cnt = 3
        line_feed_char = ''
        for _, __ in enumerate(get_list_from_integer_range(1, line_feed_cnt)):
            # print(f'''{__}''')
            print(f'''{line_feed_char}''')

        logging.debug(question)

        while 1:
            answer = input(rf"{get_colorful_text_working_with_stamp_enviromnet(func_n=func_n)} >").strip().lower()
            if answer is not None:
                if answer != '':
                    logging.debug(rf"ANSWER='{answer}'")
                break
            else:
                logging.debug("INVALID INPUT. PLEASE PRESS ENTER TO CONTINUE.")
    except KeyboardInterrupt:
        raise
    except:
        traceback.print_exc()
        import sys
        traceback.print_exc(file=sys.stdout)
