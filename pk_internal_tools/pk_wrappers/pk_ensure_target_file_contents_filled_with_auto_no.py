if __name__ == '__main__':
    import logging

    try:

        # , d_pk_system
        #  import pk_ensure_target_file_contents_filled_with_auto_no_option2

        # from pk_internal_tools.pk_objects.static_logic import d_pk_system, UNDERLINE, '{PkTexts.TRY_GUIDE}', '[ DEBUGGING NOTE ]', '[ EXCEPTION DISCOVERED ]', UNDERLINE, '{PkTexts.TRY_GUIDE}', '[ DEBUGGING NOTE ]', '[ EXCEPTION DISCOVERED ]', d_pk_external_tools
        # , pk_deprecated_get_d_current_n_like_human, get_list_from_f, does_pnx_exist, get_str_from_list, print_highlighted
        #
        import traceback

        # from pk_internal_tools.pk_objects.500_live_logic import get_str_from_f, pk_input_validated

        # todo
        #   chore : rename f_n with suffix as _converted

        # [OPTION]
        # f = input_validated(prompt='f=')
        # f = rf'{pk_external_tools}/'

        # [OPTION]
        # template_str = get_str_f_temp() # todo    with open     f_obj    notepad.exe
        # template_str = get_list_f_temp() # todo
        # template_str = get_str_from_f(f=f)

        logging.debug(rf'''{PK_UNDERLINE} %%%FOO%%%''')
        result = pk_ensure_target_file_contents_filled_with_auto_no_option2(template_str=template_str, word_monitored='%%%FOO%%%', auto_cnt_starting_no=0)
        logging.debug(result)
        logging.debug(rf'''{PK_UNDERLINE} %%%FOO%%%''')


    except:
        logging.debug("202312071431")
